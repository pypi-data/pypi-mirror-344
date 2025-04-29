from typing import Any, Dict, List, NamedTuple, Optional

from procaaso_log.enum import Level
from procaaso_log.settings import Settings


class LoggerDefinition(NamedTuple):
    name: str
    handlers: Optional[List[str]] = None
    level: Optional[Level] = None
    propagate: Optional[bool] = None


def build_root_logger_dict(handlers: List[str], level: Level) -> Dict[str, Any]:
    assert (
        len(handlers) > 0
    ), "Must provide at least one handler to build root logger dict"
    return {
        "handlers": handlers,
        "level": level.value,
    }


def build_logger_dict(
    logger_defs: List[LoggerDefinition],
    level: Level,
    propagate: bool = False,
) -> Dict[str, Any]:
    loggers = {}
    for logger_def in logger_defs:
        loggers[logger_def.name] = {
            "handlers": logger_def.handlers or [],
            "level": (logger_def.level or level).value,
            "propagate": logger_def.propagate or propagate,
        }
    return loggers


def build_dict_config(
    disable_existing_loggers: bool = False,
    formatters: Optional[Dict[str, Dict[str, Any]]] = None,
    handlers: Optional[Dict[str, Dict[str, Any]]] = None,
    loggers: Optional[List[LoggerDefinition]] = None,
    default_logger_propagate: bool = False,
    root_handlers: List[str] = ["default"],
    settings: Optional[Settings] = None,
) -> Dict[str, Any]:
    settings = settings or Settings()
    formatters = formatters or {}
    handlers = handlers or {}
    loggers = loggers or []

    loggers_dict = build_logger_dict(
        loggers, settings.level, propagate=default_logger_propagate
    )
    for root_handler in root_handlers:
        assert (
            root_handler in handlers
        ), f"The root_handler key={root_handler} is not present within the handlers dict"
    root_logger = build_root_logger_dict(root_handlers, settings.root_level)
    dict_config = {
        "version": 1,
        "disable_existing_loggers": disable_existing_loggers,
        "formatters": formatters,
        "handlers": handlers,
        "loggers": loggers_dict,
        "root": root_logger,
    }
    return dict_config
