import structlog.stdlib

from procaaso_log.enum import Mode
from procaaso_log.settings import Settings
from procaaso_log.processor import get_sequence, get_renderer, remove_processors_meta


class Formatter(structlog.stdlib.ProcessorFormatter):
    def __init__(
        self,
        mode: Mode = Mode.STD,
    ) -> None:
        settings = Settings()
        processors = get_sequence(settings.env, mode=mode)
        renderer = get_renderer(settings.format)

        super().__init__(
            foreign_pre_chain=processors,
            processors=[
                remove_processors_meta,
                renderer,
            ],
        )
