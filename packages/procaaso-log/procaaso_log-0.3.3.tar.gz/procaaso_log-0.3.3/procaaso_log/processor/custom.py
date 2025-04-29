from typing import Dict, Any
import logging
import platform
import os

from structlog.types import EventDict


def add_process_parameters(
    logger: logging.Logger, method_name: str, event_dict: EventDict
) -> EventDict:
    """
    Add the subprocess name and pid to the event dict.
    """
    try:
        import multiprocessing as mp

        p = mp.current_process()
        event_dict["subprocess_name"] = p.name
    except Exception:
        pass
    return event_dict


def add_node_info(
    logger: logging.Logger, method_name: str, event_dict: EventDict
) -> EventDict:
    """
    Add os and pid information under "node" key
    """
    node = event_dict.get("node", {})
    node["os"] = platform.platform()
    node["pid"] = os.getpid()
    event_dict["node"] = node
    return event_dict


def add_runtime_info(
    logger: logging.Logger, method_name: str, event_dict: EventDict
) -> EventDict:
    """
    Add runtime language information under "runtime" key
    """
    runtime = event_dict.get("runtime", {})
    runtime["lang"] = "python"
    runtime["lang_ver"] = platform.python_version()
    event_dict["runtime"] = runtime
    return event_dict


CALLSITE_KEY_MAP = {
    "pathname": "file_path",
    "func_name": "func_name",
    "lineno": "line_no",
}


def nest_callsite_under_source(
    logger: logging.Logger, method_name: str, event_dict: EventDict
) -> EventDict:
    """
    Nest "pathname", "func_name", and "lineno" from callsite params
    underneath the "source", key
    """
    source: Dict[str, Any] = event_dict.get("source", {})
    for key, nest_key in CALLSITE_KEY_MAP.items():
        if key in event_dict:
            o = event_dict.pop(key)
            source[nest_key] = o

    event_dict["source"] = source
    return event_dict


TOP_LEVEL_KEYS = (
    "time",
    "message",
    "level",
    "source",
    "node",
    "context",
    "logger",
    "runtime",
    "error",
    "http",
    "auth",
    "control_task",
    "correlation_id",
)


def nest_context_under_key(
    logger: logging.Logger, method_name: str, event_dict: EventDict
) -> EventDict:
    """
    Move keys not in standard top-level key set underneath "context" key

    NOTE: Needs to be near (or as close as possible) to the last processor in the chain
    """
    nest_keys = tuple(
        k
        for k in event_dict.keys()
        if k not in TOP_LEVEL_KEYS and not k.startswith("_")
    )
    context = {k: event_dict.pop(k) for k in nest_keys}
    event_dict["context"] = context
    return event_dict


def rename_critical_level_fatal(
    logger: logging.Logger, method_name: str, event_dict: EventDict
) -> EventDict:
    """
    If the level is 'critical' rename it 'fatal'
    """
    if "level" in event_dict and event_dict["level"] == "critical":
        event_dict["level"] = "fatal"

    return event_dict


def nest_exc_info_under_error(
    logger: logging.Logger, method_name: str, event_dict: EventDict
) -> EventDict:
    """
    If 'exception' key exists, move it under error.trace
    """
    exc_key = "exception"
    if exc_key in event_dict:
        error = event_dict.get("error", {})
        error["trace"] = event_dict.pop(exc_key)
        event_dict["error"] = error
    return event_dict


def remove_processors_meta(
    logger: logging.Logger, method_name: str, event_dict: EventDict
) -> EventDict:
    """
    Remove ``_record`` and ``_from_structlog`` from *event_dict*.

    These keys are added to the event dictionary, before
    `procaaso_log.Formatter`'s *processors* are run.
    """
    if "_record" in event_dict:
        del event_dict["_record"]
    if "_from_structlog" in event_dict:
        del event_dict["_from_structlog"]

    return event_dict
