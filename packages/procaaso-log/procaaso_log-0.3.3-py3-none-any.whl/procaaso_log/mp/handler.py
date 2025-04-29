from __future__ import annotations
from typing import Any
from logging import LogRecord
from logging.handlers import QueueHandler as _QueueHandler
import importlib

from procaaso_log.enum import Mode
from procaaso_log.formatter import Formatter


QUEUE_IMPORT_MODULE = "procaaso_log.mp.queue"
QUEUE_IMPORT_ATTR = "_queue"


class QueueHandler(_QueueHandler):
    """Thin wrapper of logging.handlers.QueueHandler which imports the default log queue.

    Also sets the formatter of the handlers to the default procaaso_log.Formatter in multiprocessing mode.
    """

    def __init__(self) -> None:
        # Import the singleton queue
        mod = importlib.import_module(QUEUE_IMPORT_MODULE)
        queue = getattr(mod, QUEUE_IMPORT_ATTR)

        super().__init__(queue)

        # Bake in the formatter
        self.setFormatter(Formatter(mode=Mode.MP))

    def prepare(self, record: LogRecord) -> Any:
        record = super().prepare(record)
        record._logger = None  # type: ignore
        return record
