from typing import Any, Dict, Optional, Tuple, List
from abc import abstractmethod
from django.views import View
from django.core.paginator import Paginator, Page
from django.shortcuts import render
from .mixins import (
    QueryFilterOrderMixin,
    InvalidQueryFilterException,
    InvalidOrderDirectionException,
    InvalidOrderFieldException
)


class MessageType:
    WARNING = 'warning'
    DANGER = 'danger'


DEFAULT_MESSAGE_ICONS = {
    MessageType.WARNING: 'bi bi-exclamation-octagon-fill text-warning',
    MessageType.DANGER: 'bi bi-exclamation-triangle text-danger'
}
DEFAULT_MESSAGE_ICON = 'bi bi-info-circle text-primary'


class InvalidPageNumberException(Exception):
    def __init__(self, current_page: int, max_page: int):
        super().__init__(
            f'El número de página {current_page} es inválido, '
            f'el rango permitido es de 1 a {max_page}'
        )


class PaginatorView(View, QueryFilterOrderMixin):

    default_page: int = 1
    default_per_page: int = 5
    default_on_each_side: int = 2
    default_on_ends: int = 0
    max_per_page: int = 100
    export_url: Optional[str] = None
    import_url: Optional[str] = None
    message_icons: Dict[str, str] = DEFAULT_MESSAGE_ICONS
    default_message_icon: str = DEFAULT_MESSAGE_ICON

    @property
    @abstractmethod
    def template_name(self) -> str:
        """Nombre de la plantilla a renderizar."""
        pass

    def get_integer_query_param(
        self,
        name: str,
        default_value: int,
        max_value: Optional[int] = None,
        min_value: Optional[int] = None
    ) -> int:
        """
        Obtiene un parámetro entero de la consulta GET con validación.
        Si el parámetro no existe o es inválido, se devuelve el valor por defecto.
        Args:
            name: Nombre del parámetro
            default_value: Valor por defecto si no existe o es inválido
            max_value: Valor máximo permitido (inclusive)
            min_value: Valor mínimo permitido (inclusive)
        Returns:
            El valor del parámetro validado
        """
        try:
            value = int(self.request.GET.get(name, default_value))
        except (ValueError, TypeError):
            return default_value
        if max_value is not None:
            value = min(value, max_value)
        if min_value is not None:
            value = max(value, min_value)
        return value

    def get_page_obj(self, query) -> Tuple[Page, List]:
        """
        Crea un objeto de paginación para la consulta dada.
        Args:
            query: QuerySet o lista a paginar
        Returns:
            Tupla con (page_obj, pages)
        Raises:
            InvalidPageNumberException: Si el número de página está fuera de rango
        """
        per_page = self.get_integer_query_param(
            'per_page',
            self.default_per_page,
            max_value=self.max_per_page,
            min_value=1
        )
        page_number = self.get_integer_query_param(
            'page',
            self.default_page,
            min_value=1
        )
        paginator = Paginator(query, per_page)
        if page_number > paginator.num_pages:
            raise InvalidPageNumberException(page_number, paginator.num_pages)
        page_obj = paginator.get_page(page_number)
        pages = paginator.get_elided_page_range(
            number=page_number,
            on_each_side=self.default_on_each_side,
            on_ends=self.default_on_ends
        )
        return page_obj, pages

    def get_message_icon(self, message_type: str) -> str:
        """
        Obtiene el icono correspondiente al tipo de mensaje.
        Args:
            message_type: Tipo de mensaje (warning/danger)
        Returns:
            String de clase de icono correspondiente al tipo de mensaje
        """
        return self.message_icons.get(message_type, self.default_message_icon)

    def get_context_error(self, exception: Exception, message_type: str) -> Dict[str, str]:
        """
        Crea un diccionario de contexto para mostrar errores.
        Args:
            exception: Excepción ocurrida
            message_type: Tipo de mensaje (warning/danger)
        Returns:
            Diccionario con los datos del error
        """
        return {
            'type': message_type,
            'icon': self.get_message_icon(message_type),
            'message': str(exception)
        }

    def build_context(self, request) -> Dict[str, Any]:
        """
        Construye el contexto para la plantilla.
        Args:
            request: Objeto HttpRequest
        Returns:
            Diccionario con todo el contexto necesario
        """
        context = {
            'page_error': None,
            'page_obj': None,
            'pages': [],
            'filterset': None,
            'filters': {},
            'filters_errors': [],
            'order': {},
            'defaults': self.get_defaults(),
            'export_url': self.export_url,
            'import_url': self.import_url
        }
        try:
            queryset = self.get_queryset()
            try:
                queryset = self.apply_filterset_to_queryset(queryset, request.GET)
            except InvalidQueryFilterException as e:
                context['page_error'] = self.get_context_error(e, MessageType.WARNING)
                context['filters_errors'] = getattr(self, 'filters_errors', [])
            try:
                queryset = self.apply_order_to_queryset(queryset, request.GET)
            except (InvalidOrderDirectionException, InvalidOrderFieldException) as e:
                if not context['page_error']:
                    context['page_error'] = self.get_context_error(e, MessageType.WARNING)
            context['filterset'] = getattr(self, 'filterset', None)
            context['filters'] = getattr(self, 'applied_filters', {})
            context['order'] = getattr(self, 'applied_order', {})
            page_obj, pages = self.get_page_obj(queryset)
            context['page_obj'] = page_obj
            context['pages'] = pages
        except InvalidPageNumberException as e:
            context['page_error'] = self.get_context_error(e, MessageType.DANGER)
        return context

    def get(self, request, *args, **kwargs):
        """
        Maneja las solicitudes GET.
        """
        context = self.build_context(request)
        return render(request, self.template_name, context)
