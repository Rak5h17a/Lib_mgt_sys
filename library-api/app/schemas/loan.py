from pydantic import BaseModel, Field

class BorrowRequest(BaseModel):
    member_id: str= Field(..., min_length=1)
    item_id: str = Field(..., min_length=1)

class ReturnResponse(BaseModel):
    loan_id: str
    late_fee: float
    message: str 

class LoanResponse(BaseModel):
    id: str 
    member_id: str
    item_id: str
    borrowed_on: str
    due_on: str
    returned_on: str|None