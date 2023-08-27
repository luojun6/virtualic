from abc import ABC, abstractmethod

from utils.loggers import Logger, logging_handler
import logging

_logger = Logger(logger_name=__file__,
                 log_handler=logging_handler,
                 logging_level=logging.DEBUG)


class Command(ABC):

    def __init__(self, receiver) -> None:
        self.__receiver = receiver

    @abstractmethod
    def execute(self):
        _logger.debug(f"Executing command: {self.__class__.__name__}.")

    @property
    def receiver(self):
        return self.__receiver
