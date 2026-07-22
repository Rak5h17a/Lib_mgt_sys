from abc import ABC,abstractmethod
from typing import Any

class BaseRepository(ABC):

    @abstractmethod
    async def create(self, data: dict[str, Any]) -> str:
        ... 

    @abstractmethod
    async def get_by_id(self, record_id: str) -> dict[str, Any] |None:
        ...

    async def get_all(self) ->list[dict[str, Any]]:
        ...

    @abstractmethod
    async def update(self, record_id: str, data: dict[str, Any]) -> bool:
        ...

    @abstractmethod
    async def delete(self, record_id: str) -> bool:
        ... 