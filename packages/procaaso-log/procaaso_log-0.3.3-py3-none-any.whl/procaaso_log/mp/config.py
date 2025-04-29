from __future__ import annotations
from typing import (
    Any,
    Dict,
    Optional,
    Union,
    Tuple,
    Iterable,
)
import inspect
import logging.config

from procaaso_log.enum import Level, Mode, Env
from procaaso_log.settings import Settings
from procaaso_log.config import Config
from procaaso_log.processor import get_sequence
from procaaso_log.std.configure import configure
from procaaso_log.std.dict_config import LoggerDefinition, build_dict_config
from procaaso_log.util import merge_dict_configs

from .queue import LogQueue
from .listener import LogProcess


def producer_dict_config(
    settings: Settings,
    loggers: Iterable[str],
) -> Dict[str, Any]:
    handlers = {"default": {"()": "procaaso_log.mp.QueueHandler"}}
    logger_defs = {
        l: LoggerDefinition(
            name=l, handlers=["default"], level=settings.level, propagate=False
        )
        for l in loggers
    }
    return build_dict_config(
        disable_existing_loggers=True,
        handlers=handlers,
        loggers=list(logger_defs.values()),
        root_handlers=["default"],
        settings=settings,
    )


def consumer_dict_config(
    settings: Settings,
    loggers: Iterable[str],
) -> Dict[str, Any]:
    handlers = {
        "default": {
            "class": "logging.StreamHandler",
            "stream": f"ext://sys.{settings.output.lower()}",
        }
    }
    logger_defs = {
        l: LoggerDefinition(
            name=l, handlers=["default"], level=settings.level, propagate=False
        )
        for l in loggers
    }
    return build_dict_config(
        disable_existing_loggers=True,
        handlers=handlers,
        loggers=list(logger_defs.values()),
        root_handlers=["default"],
        settings=settings,
    )


def multiprocessing_config(
    queue: LogQueue,
    *loggers: str,
    level: Union[None, str, Level] = None,
    env: Union[None, str, Env] = None,
    consumer_overrides: Optional[Dict[str, Any]] = None,
    producer_overrides: Optional[Dict[str, Any]] = None,
    **format_kwargs: Any,
) -> Tuple[LogProcess, Config]:
    """Main process multiprocessing config.

    Cretes a log process ready to be started and a config object to be passed to other log-producing subprocesses.

    Args:
        queue (LogQueue): The log queue to utilize for communication between processes.
        level (Union[None, str, Level], optional): Log level output filter. Defaults to None.

    Returns:
        Tuple[LogProcess, Config]: A log process object ready to be started and a config reference object.
    """
    producer_overrides = producer_overrides or {}
    consumer_overrides = consumer_overrides or {}
    if len(loggers) == 0:
        # Get the calling frame module if no logger names supplied
        try:
            frame = inspect.stack()[1]
            module = inspect.getmodule(frame[0])
            assert module, "No module"
            loggers = (module.__name__,)
        finally:
            del frame
    logger_set = set(loggers)

    override_env_kwargs = {}
    if level:
        override_env_kwargs["level"] = level
    if env:
        override_env_kwargs["env"] = env

    settings = Settings(
        **override_env_kwargs,
        **format_kwargs,
    )

    prod_dc = merge_dict_configs(
        producer_dict_config(settings, logger_set),
        producer_overrides,
    )
    processors = get_sequence(settings.env, Mode.MP)
    prod_config = Config(settings=settings, processors=processors, dict_config=prod_dc)

    cons_dc = merge_dict_configs(
        consumer_dict_config(settings, logger_set),
        consumer_overrides,
    )
    cons_config = Config(settings=settings, processors=(), dict_config=cons_dc)
    log_proc = LogProcess(queue, cons_config)

    return log_proc, prod_config


def install_multiprocessing_config(config: Config) -> None:
    """Subprocess log configurer for log-producers.

    Args:
        config (Config): The config object returned from `multiprocessing_config`
    """
    configure(processors=config.processors)
    logging.config.dictConfig(config.dict_config)
