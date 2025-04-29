from __future__ import annotations
from typing import Optional
import logging.config
from logging.handlers import QueueListener
from multiprocessing import Process, Event

from procaaso_log.config import Config
from procaaso_log.std.configure import configure

from .queue import LogQueue


class LogProcess(Process):
    """Process which listens to the default logging queue

    Overloads multiprocessing.Process methods: run, join.

    This process must be started before other sub-processes start that expect to send logs.
    """

    def __init__(
        self,
        queue: LogQueue,
        config: Config,
    ) -> None:
        super().__init__(name="procaaso_log.mp.LogProcess")
        self.queue = queue
        self.config = config
        self.on_stop = Event()

    def run(self) -> None:
        configure(processors=self.config.processors)
        logging.config.dictConfig(self.config.dict_config)
        handlers = logging.getLogger().handlers
        listener = QueueListener(self.queue, *handlers)
        listener.start()
        self.on_stop.wait()
        listener.stop()

    def join(self, timeout: Optional[float] = None) -> None:
        """Join the logging process after program completion.

        Args:
            timeout (Optional[float], optional): Timeout it seconds to wait for process exit. Defaults to None.

        Notes:
            Best practice is to call `.start()` on this process first, then `.join()` on it last as the program is shutting down.
        """
        self.on_stop.set()
        self.queue.close()
        self.queue.join_thread()
        super().join(timeout=timeout)
