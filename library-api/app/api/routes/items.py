from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_item_service
from app.services.item_service import ItemService
from app.schemas.item import BookCreate, MagazineCreate,DVDCreate,ItemResponse

router =  APIRouter(prefix="/items", tags=["items"])

def _to_response(item, item_id: str) -> ItemResponse:
    return ItemResponse(
        id=item_id,
        type=type(item).__name__.lower(),
        title=item.title,
        total_copies=item.total_copies,
        available_copies=item.available_copies,
    )

@router.post("/books", response_model= dict, status_code=status.HTTP_201_CREATED)
async def add_book(payload: BookCreate, service: ItemService = Depends(get_item_service)):
    item_id= await service.add_book(payload.title, payload.total_copies, payload.author, payload.isbn)
    return {"id": item_id}

@router.post("/magazines", response_model= dict, status_code=status.HTTP_201_CREATED)
async def add_magazine(payload: MagazineCreate, service: ItemService = Depends(get_item_service)):
    item_id= await service.add_magazine(payload.title, payload.total_copies, payload.issue_number)
    return {"id": item_id}

@router.post("/dvds", response_model= dict, status_code= status.HTTP_201_CREATED)
async def add_dvd(payload: DVDCreate, service: ItemService = Depends(get_item_service)):
    item_id= await service.add_dvd(payload.title, payload.total_copies, payload.runtime_minutes)
    return {"id": item_id}

@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(item_id: str, service : ItemService= Depends(get_item_service)):
    item= await service.get_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return _to_response(item, item_id)

@router.get("/", response_model=list[ItemResponse])
async def list_items(service: ItemService = Depends(get_item_service)):
    items= await service.list_items()
    return [
        ItemResponse(
            id="",
            type=type(i).__name__.lower(),
            title=i.title,
            total_copies=i.total_copies,
            available_copies=i.available_copies,
        )
        for i in items
    ]