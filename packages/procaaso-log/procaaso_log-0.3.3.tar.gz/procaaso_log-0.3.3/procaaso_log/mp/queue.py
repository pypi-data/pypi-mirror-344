from __future__ import annotations
from typing import NewType
from multiprocessing import Queue
from typing import (
    Optional,
)
from logging import LogRecord  # noqa

LogQueue = NewType("LogQueue", "Queue[LogRecord]")
"""Pre-typed multiprocessing.Queue for logging.LogRecord"""

_queue: Optional[LogQueue] = None


def get_queue() -> LogQueue:
    """Get or create the default logging queue."""
    global _queue
    if _queue is None:
        _queue = Queue()  # type: ignore
    return _queue  # type: ignore


def set_queue(q: LogQueue) -> None:
    """Set the default logging queue, if already exists raises error.

    Args:
        q (LogQueue): The queue to set as default

    Raises:
        ValueError: If default queue is already set
    """
    global _queue
    if _queue is not None:
        raise ValueError("The queue has already been set, use get_queue()")
    _queue = q
