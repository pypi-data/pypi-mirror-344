from typing import Dict, Any, NamedTuple, Tuple

from structlog.types import Processor

from procaaso_log.settings import Settings


class Config(NamedTuple):
    settings: Settings
    processors: Tuple[Processor, ...]
    dict_config: Dict[str, Any]
