from rest_framework import pagination, status
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import _positive_int


class LimitOffsetPagination(pagination.LimitOffsetPagination):
    default_limit = 30
    max_limit = 1000

    limit_query_param = 'limit'
    offset_query_param = 'offset'

    def _validate_limit(self, request):
        value = _positive_int(request.query_params[self.limit_query_param], strict=True)

        if value > self.max_limit:
            raise ValueError
        return value

    def _validate_offset(self, request):
        try:
            value = _positive_int(
                request.query_params[self.offset_query_param],
            )
        except (KeyError, ValueError):
            return 0

    def get_limit(self, request):
        if self.limit_query_param:
            try:
                return self._validate_limit(request)
            except KeyError:
                pass
            except ValueError:
                raise ValidationError(
                    {'detail': f'Limit parameter must be in range (1, {self.max_limit})'},
                    code=status.HTTP_400_BAD_REQUEST
                )

        return self.default_limit

    def get_offset(self, request):
        try:
            return _positive_int(request.query_params[self.offset_query_param])
        except KeyError:
            return 0
        except ValueError:
            raise ValidationError(
                {'detail': f'Offset parameter must be >= 0'},
                code=status.HTTP_400_BAD_REQUEST
            )