from pydantic import BaseModel, Field

#-------------REQUEST------------------

class BookCreate(BaseModel):
    title: str = Field(..., min_length=1)
    total_copies: int = Field(..., gt=0)
    author: str =Field(..., min_length=1)
    isbn: str = Field(..., min_length=1)


class MagazineCreate(BaseModel):
    title: str = Field(..., min_length=1)
    total_copies: int = Field(..., gt=0)
    issue_number: int = Field(..., gt=0)

class DVDCreate(BaseModel):
    title: str = Field(..., min_length=1)
    total_copies: int = Field(..., gt=0)
    runtime_minutes : int= Field(..., gt=0)

#------------RESPONSE--------------------
class ItemResponse(BaseModel):
    id: str
    type: str
    title: str 
    total_copies: int 
    available_copies: int