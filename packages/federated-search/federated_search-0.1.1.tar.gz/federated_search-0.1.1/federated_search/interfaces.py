from abc import ABC, abstractmethod

class Injestion(ABC):
    @abstractmethod
    def inject(self, **args):
        pass

class Retrieval(ABC):
    @abstractmethod
    def retrieve(self, **args):
        pass
