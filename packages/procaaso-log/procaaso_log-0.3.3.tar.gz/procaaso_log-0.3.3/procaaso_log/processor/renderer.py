from typing import Any, Dict, Protocol
from functools import lru_cache

import structlog.processors
import structlog.dev
from structlog.types import Processor

from procaaso_log.enum import Format


class ProcessorFactory(Protocol):
    def __call__(self, *args: Any, **kwds: Any) -> Processor: ...


@lru_cache
def json_renderer_factory(
    *args: Any, **kwargs: Any
) -> structlog.processors.JSONRenderer:
    return structlog.processors.JSONRenderer(*args, **kwargs)


@lru_cache
def key_value_renderer_factory(
    *args: Any, **kwargs: Any
) -> structlog.processors.KeyValueRenderer:
    return structlog.processors.KeyValueRenderer(*args, **kwargs)


@lru_cache
def console_renderer_factory(
    *args: Any, **kwargs: Any
) -> structlog.dev.ConsoleRenderer:
    return structlog.dev.ConsoleRenderer(*args, **kwargs)


FORMAT_RENDERER_MAP: Dict[Format, ProcessorFactory] = {
    Format.JSON: json_renderer_factory,
    Format.KEY_VALUE: key_value_renderer_factory,
    Format.CONSOLE: console_renderer_factory,
}


def get_renderer(format: Format, *args: Any, **kwargs: Any) -> Processor:
    return FORMAT_RENDERER_MAP[format](*args, **kwargs)
