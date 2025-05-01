from typing import Dict
from django.db.models import QuerySet

DEFAULT_ID_FIELD = 'id'
DEFAULT_TIME_FIELD = 'created_at'
DIRECTION_ASC = 'ASC'
DIRECTION_DESC = 'DESC'
DIRECTIONS = {DIRECTION_ASC, DIRECTION_DESC}


class InvalidOrderDirectionException(Exception):
    """Excepción lanzada cuando la dirección de ordenamiento es inválida."""

    def __init__(self, order_direction: str):
        allowed_directions_str = ', '.join(sorted(DIRECTIONS))
        super().__init__(f'La dirección de ordenamiento "{order_direction}" es inválida. '
                         f'Debe ser uno de: {allowed_directions_str}.')


class InvalidOrderFieldException(Exception):
    """Excepción lanzada cuando el campo de ordenamiento es inválido."""

    def __init__(self, field_name: str, allowed_fields: set):
        allowed_fields_str = ', '.join(sorted(allowed_fields))
        super().__init__(f'El campo de ordenamiento "{field_name}" es inválido. '
                         f'Campos permitidos: {allowed_fields_str}.')


class QueryOrderMixin:
    """
    Mixin para manejar el ordenamiento de querysets de manera consistente.
    Atributos:
        default_order_by (str): Campo por defecto para ordenar.
        default_order_direction (str): Dirección por defecto del ordenamiento.
        default_field_time (str): Campo temporal por defecto.
        allowed_fields_order (set): Conjunto de campos permitidos para ordenar.
    """
    default_order_by: str = DEFAULT_ID_FIELD
    default_order_direction: str = DIRECTION_DESC
    default_field_time: str = DEFAULT_TIME_FIELD
    allowed_fields_order: set = {DEFAULT_ID_FIELD, DEFAULT_TIME_FIELD}

    def init_order_defaults(self):
        self.applied_order = self.validate_order_params(self.default_order_by, self.default_order_direction)

    def validate_order_params(self, order_by_field: str, order_direction: str) -> Dict[str, str]:
        """
        Valida los parámetros de ordenamiento y construye la configuración de orden.

        Args:
            order_by_field (str): Campo por el cual se ordenará.
            order_direction (str): Dirección del ordenamiento ("ASC" o "DESC").

        Returns:
            Dict[str, str]: Un diccionario con los detalles del ordenamiento.

        Raises:
            InvalidOrderFieldException: Si el campo de ordenamiento no es válido.
            InvalidOrderDirectionException: Si la dirección de ordenamiento no es válida.
        """
        if order_direction not in DIRECTIONS:
            raise InvalidOrderDirectionException(order_direction)
        if order_by_field not in self.allowed_fields_order:
            raise InvalidOrderFieldException(order_by_field, self.allowed_fields_order)

        order_by = f"-{order_by_field}" if order_direction == DIRECTION_DESC else order_by_field
        return {
            'order_by': order_by,
            'by': order_by_field,
            'direction': order_direction
        }

    def apply_order_to_queryset(self, queryset: QuerySet, order_params: dict) -> QuerySet:
        order_by_field = order_params.get('order_by', self.default_order_by)
        order_direction = order_params.get('order_direction', self.default_order_direction)
        if order_direction == '':
            order_direction = self.default_order_direction
        if order_by_field == '':
            order_by_field = self.default_order_by
        self.applied_order = self.validate_order_params(order_by_field, order_direction)
        return queryset.order_by(self.applied_order['order_by'])
