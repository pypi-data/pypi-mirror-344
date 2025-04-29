from __future__ import annotations
from typing import Any

import structlog
from structlog.stdlib import BoundLogger


class Logger(BoundLogger):
    """The procaaso_log standard logger

    A thin wrapper around structlog.stdlib.BoundLogger.
    """

    def bind(self, **new_values: Any) -> Logger:
        """
        Return a new logger with *new_values* added to the existing ones.
        """
        return self.__class__(
            self._logger,
            self._processors,
            self._context.__class__(self._context, **new_values),
        )

    def unbind(self, *keys: str) -> Logger:
        """
        Return a new logger with *keys* removed from the context.

        :raises KeyError: If the key is not part of the context.
        """
        bl = self.bind()
        for key in keys:
            del bl._context[key]

        return bl

    def try_unbind(self, *keys: str) -> Logger:
        """
        Like :meth:`unbind`, but best effort: missing keys are ignored.
        """
        bl = self.bind()
        for key in keys:
            bl._context.pop(key, None)

        return bl

    def new(self, **new_values: Any) -> Logger:
        """
        Clear context and binds *initial_values* using `bind`.

        Only necessary with dict implementations that keep global state like
        those wrapped by `structlog.threadlocal.wrap_dict` when threads
        are re-used.
        """
        self._context.clear()

        return self.bind(**new_values)


def get_logger(name: str, **initial_values: Any) -> Logger:
    """Create a new logger

    Best practice:  Use `__name__` for the `name` parameter

    Args:
        name (str): Name of the logger.  Period delimited.

    Returns:
        Logger: The named, contextual logger instance
    """
    logger: Logger = structlog.get_logger(name, **initial_values)
    return logger
