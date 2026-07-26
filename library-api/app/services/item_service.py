from app.domain.items import Book,DVD, LibraryItem,Magazine
from app.domain.item_factory import item_from_dict
from app.repositories.item_repository import ItemRepository

class ItemService:

    def __init__(self,repository: ItemRepository) -> None:
        self._repository=repository

    async def add_book(self, title:str, total_copies:int, author: str, isbn:str ) -> str:
        # create and store new book
        book=Book(title,total_copies,author,isbn)
        return await self._repository.create(book.to_dict())

    async def add_magazine(self, title:str, total_copies: int, issue_number:int)-> str:
        magazine=Magazine(title,total_copies,issue_number)
        return await self._repository.create(magazine.to_dict())

    async def add_dvd(self, title:str, total_copies:int, runtime_minutes: int) ->str:
        dvd=DVD(title,total_copies,runtime_minutes)
        return await self._repository.create(dvd.to_dict())

    async def get_item(self, item_id:str)-> LibraryItem | None:
        # sourcery skip: assign-if-exp, reintroduce-else
        # fetch one item as a live domain object
        data= await self._repository.get_by_id(item_id)
        if data is None:
            return None
        return item_from_dict(data)

    async def list_items(self)-> list[LibraryItem]:
        #fetch all objects as live domain objects
        documents= await self._repository.get_all()
        return [item_from_dict(doc) for doc in documents]

    async def borrow_item(self,item_id: str)-> bool:
        data= await self._repository.get_by_id(item_id)
        if data is None:
            raise ValueError(f"No item found with id: {item_id}")
        item=item_from_dict(data)
        item.borrow_one()
        return await self._repository.update(item_id, {"available_copies": item.available_copies})

    async def return_item(self,item_id:str)-> bool:
        data = await self._repository.get_by_id(item_id)
        if data is None:
            raise ValueError(f"No item found with id: {item_id}")
        item=item_from_dict(data)
        item.return_one()
        return await self._repository.update(item_id,{"available_copies":item.available_copies})

    async def remove_item(self,item_id:str)-> bool:
        return await self._repository.delete(item_id)