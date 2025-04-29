from typing import Optional, Sequence, Any

from structlog.types import Processor
import structlog.stdlib
from structlog import configure as _configure

from procaaso_log.logger import Logger


def configure(
    processors: Optional[Sequence[Processor]] = None,
    **kwargs: Any,
) -> None:
    processors = processors or []
    config_kwargs = kwargs or {
        "processors": [
            structlog.stdlib.filter_by_level,
            *processors,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        "logger_factory": structlog.stdlib.LoggerFactory(),
        "wrapper_class": Logger,
        "cache_logger_on_first_use": True,
    }
    _configure(**config_kwargs)
