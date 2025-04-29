from enum import Enum
import logging


class Level(str, Enum):
    FATAL = logging.getLevelName(logging.CRITICAL)
    CRITICAL = logging.getLevelName(logging.CRITICAL)
    """NOTE:  Alias of FATAL, rendered as 'fatal'"""
    ERROR = logging.getLevelName(logging.ERROR)
    WARNING = logging.getLevelName(logging.WARNING)
    INFO = logging.getLevelName(logging.INFO)
    DEBUG = logging.getLevelName(logging.DEBUG)

    @property
    def int(self) -> int:
        try:
            return logging._nameToLevel[self.value]
        except KeyError:
            return 0

    @property
    def str(self) -> str:
        return self.value.lower()  # type: ignore


class Env(str, Enum):
    PROD = "PROD"
    """Production environment"""
    DEV = "DEV"
    """Development environment"""


class Format(str, Enum):
    AUTO = "AUTO"
    """Automatic format"""
    JSON = "JSON"
    KEY_VALUE = "KEY_VALUE"
    CONSOLE = "CONSOLE"


class Mode(str, Enum):
    STD = "STD"
    """Standard mode"""
    MP = "MP"
    """Multiprocessing mode"""
