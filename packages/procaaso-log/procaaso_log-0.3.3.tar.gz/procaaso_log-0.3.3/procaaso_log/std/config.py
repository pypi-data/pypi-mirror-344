from typing import Optional, Dict, Any, Union
import inspect
import logging.config

from procaaso_log.settings import Settings
from procaaso_log.enum import Level, Mode, Env
from procaaso_log.config import Config
from procaaso_log.processor import get_sequence
from procaaso_log.util import merge_dict_configs

from .dict_config import LoggerDefinition, build_dict_config
from .configure import configure


def standard_dict_config(
    *loggers: str, settings: Optional[Settings] = None
) -> Dict[str, Any]:
    """Generate the standard configuration dict object.

    Returned object is compatible with `logging.config.dictConfig`

    Args:
        settings (Optional[Settings], optional): Settings environment object. Defaults to None.

    Returns:
        Dict[str, Any]: Dictionary compatible with logging.config.dictConfig
    """
    settings = settings or Settings()
    formatters = {
        "default": {
            "()": "procaaso_log.Formatter",
        }
    }
    handlers = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": f"ext://sys.{settings.output.lower()}",
        },
    }
    logger_defs = {
        l: LoggerDefinition(name=l, handlers=["default"], level=settings.level)
        for l in loggers
    }
    return build_dict_config(
        disable_existing_loggers=False,
        formatters=formatters,
        handlers=handlers,
        loggers=list(logger_defs.values()),
        root_handlers=["default"],
        settings=settings,
    )


def standard_config(
    *loggers: str,
    level: Union[None, str, Level] = None,
    env: Union[None, str, Env] = None,
    overrides: Optional[Dict[str, Any]] = None,
    **format_kwargs: Any,
) -> Config:
    """Install the standard configuration with the given loggers.

    Args:
        level (Union[None, str, Level], optional): Log level filter.

    Returns:
        Config: A config reference object.
    """
    overrides = overrides or {}
    if len(loggers) == 0:
        # Get the calling frame module if no logger names supplied
        try:
            frame = inspect.stack()[1]
            module = inspect.getmodule(frame[0])
            assert module, "No module"
            loggers = (module.__name__,)
        finally:
            del frame
    logger_names = set(loggers)

    override_env_kwargs = {}
    if level:
        override_env_kwargs["level"] = level
    if env:
        override_env_kwargs["env"] = env
    settings = Settings(
        **override_env_kwargs,
        **format_kwargs,
    )

    processors = get_sequence(env=settings.env, mode=Mode.STD)
    configure(processors=processors)

    dict_config = merge_dict_configs(
        standard_dict_config(*logger_names, settings=settings),
        overrides,
    )
    logging.config.dictConfig(dict_config)

    return Config(
        settings=settings,
        processors=processors,
        dict_config=dict_config,
    )
