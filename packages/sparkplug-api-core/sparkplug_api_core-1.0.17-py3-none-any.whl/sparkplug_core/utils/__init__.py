from django.conf import settings

from walrus import Database

from .asdict_exclude_none import asdict_exclude_none
from .build_cache_key import build_cache_key
from .enforce_auth import enforce_auth
from .enforce_permission import enforce_permission
from .get_bool import get_bool
from .get_paginated_response import get_paginated_response
from .get_pagination_start_end import get_pagination_start_end
from .get_query_param import get_query_param
from .get_timezones import get_timezones, TIMEZONE_CHOICES
from .get_validated_dataclass import get_validated_dataclass
from .send_admin_action import send_admin_action
from .send_client_action import send_client_action
from .socket_send import socket_send


redis_db = Database(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
)

__all__ = [
    "asdict_exclude_none",
    "build_cache_key",
    "enforce_auth",
    "enforce_permission",
    "get_validated_dataclass",
    "get_bool",
    "get_paginated_response",
    "get_pagination_start_end",
    "get_query_param",
    "get_timezones",
    "send_admin_action",
    "send_client_action",
    "socket_send",
    "TIMEZONE_CHOICES",
]
