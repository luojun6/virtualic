from abc import ABC, abstractmethod


class AbstractStrategy(ABC):
    
    @abstractmethod
    def execute(self, context):
        pass


class AbstractOnClickStrategy(ABC):
    
    @abstractmethod
    def execute(self, context, button):
        pass

class AbstractOnChangeStrategy(ABC):
    
    @abstractmethod
    def execute(self, context, change):
        pass