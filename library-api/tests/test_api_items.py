import pytest 
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.api.deps import get_item_service
from app.services.item_service import ItemService

#fake repository
class FakeItemRepository:
    def __init__(self):
        self._store={}
        self._counter=0

    async def create(self,data):
        self._counter += 1
        item_id=f"fake-{self._counter}"
        self._store[item_id] = dict(data)
        return item_id

    async def get_by_id(self, record_id):
        doc =  self._store.get(record_id)
        if doc is None:
            return None
        result= dict(doc)
        result["id"]= record_id
        return result

    async def get_all(self):
        return [{**doc, "id": rid} for rid, doc in self._store.items()]

    async def update(self, record_id, data):
        if record_id not in self._storeL:
            return False
        self._store[record_id].update(data)
        return True

    async def delete(self, record_id):
        return self._store.pop(record_id, None) is not None


# Override to tell fastapi to use fake backend service in test

def get_fake_item_service():
    return ItemService(FakeItemRepository())

app.dependency_overrides[get_item_service] = get_fake_item_service


#api tests
@pytest.mark.asyncio
async def test_add_book_returns_id():
    transport =  ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/items/books", json={
            "title":"Clean Code", "total_copies":3,
            "author":"Martin", "isbn":"123-43564645",
        })
    assert response.status_code == 201
    assert "id" in response.json()

@pytest.mark.asyncio
async def test_add_book_rejects_invalid_input():
    transport= ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response= await client.post("/items/books", json={
            "title":"", "total_copies":-1,
            "author":"X", "isbn":"Y",
        })
    assert response.status_code==422

@pytest.mark.asyncio
async def test_get_nonexistent_item_returns_404():
    transport= ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response=await client.get("/items/docs-non-exist")
    assert response.status_code == 404
