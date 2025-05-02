from abc import ABC, abstractmethod


class Serializer(ABC):
    @abstractmethod
    def serialize(self, data, path: str) -> None: ...

    @abstractmethod
    def deserialize(self, path: str): ...