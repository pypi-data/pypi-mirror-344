from structlog.processors import EventRenamer, TimeStamper, ExceptionRenderer
from structlog.tracebacks import ExceptionDictTransformer


event_key_rename_message = EventRenamer("message")
timestamper = TimeStamper(fmt="iso", utc=True, key="time")
format_exc_info = ExceptionRenderer(ExceptionDictTransformer())
