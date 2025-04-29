import contextvars
from enum import Enum


class ContentVarKey(Enum):
    """上下文变量key枚举"""
    TRACE_ID_KEY =  "trace-id" # 链路id

trace_id_context = contextvars.ContextVar(ContentVarKey.TRACE_ID_KEY.value, default="-")
trace_id_context.set("-")
