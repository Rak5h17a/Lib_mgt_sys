from pydantic import BaseModel, Field 

class StudentCreate(BaseModel):
    name: str = Field(..., min_length=1)
    member_id: str= Field(..., min_length=1)

class FacultyCreate(BaseModel):
    name: str= Field(..., min_length=1)
    member_id:str = Field(..., min_length=1)

class MemberResponse(BaseModel):
    id:str 
    type: str 
    name: str
    member_id : str
    current_loan_count : int
    max_loans: int