from abc import ABC, abstractmethod


class BasePipe(ABC):
    @abstractmethod
    def start(self, *args, **kwargs) -> None:
        raise NotImplementedError
