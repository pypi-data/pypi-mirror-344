from contextvars import ContextVar
from typing import Any, Dict, List

auth_id_type_config_cache: ContextVar[Dict[str, Any]] = ContextVar(
    "auth_id_type_config_cache", default={}
)

partner_fields_cache: ContextVar[List[str]] = ContextVar(
    "partner_fields_cache", default=[]
)
