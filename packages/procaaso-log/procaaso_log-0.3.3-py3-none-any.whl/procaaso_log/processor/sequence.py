from typing import (
    Iterable,
    List,
    Tuple,
)
from functools import reduce

import structlog.stdlib
import structlog.processors
from structlog.contextvars import merge_contextvars
from structlog.types import Processor

from procaaso_log.enum import Env, Mode

from .standard import (
    event_key_rename_message,
    timestamper,
    format_exc_info,
)
from .custom import (
    add_runtime_info,
    nest_callsite_under_source,
    nest_context_under_key,
    add_process_parameters,
    rename_critical_level_fatal,
    nest_exc_info_under_error,
)

pre_processors = (
    structlog.stdlib.PositionalArgumentsFormatter(),
    structlog.stdlib.add_logger_name,
    structlog.stdlib.add_log_level,
    merge_contextvars,
)

prod_processors: List[Processor] = [
    timestamper,
    add_runtime_info,
    structlog.processors.StackInfoRenderer(),
    format_exc_info,
    nest_exc_info_under_error,
    structlog.processors.UnicodeDecoder(),
    structlog.processors.CallsiteParameterAdder(
        parameters=(
            structlog.processors.CallsiteParameter.PATHNAME,
            structlog.processors.CallsiteParameter.FUNC_NAME,
            structlog.processors.CallsiteParameter.LINENO,
        )
    ),
    nest_callsite_under_source,
    event_key_rename_message,
    rename_critical_level_fatal,
    nest_context_under_key,
]

dev_processors: List[Processor] = [
    structlog.processors.TimeStamper("iso", utc=False),
]

mp_processors: List[Processor] = [add_process_parameters]


def get_sequence(
    env: Env,
    mode: Mode,
    *extra_processors: Processor,
) -> Tuple[Processor, ...]:
    processors: List[Iterable[Processor]] = [pre_processors]

    if mode is Mode.MP:
        processors.append(mp_processors)

    if extra_processors:
        processors.append(extra_processors)

    if env is Env.DEV:
        processors.append(dev_processors)
    elif env is Env.PROD:
        processors.append(prod_processors)

    return tuple(reduce(lambda t, s: [*t, *s], processors))
