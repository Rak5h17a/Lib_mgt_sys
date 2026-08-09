from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_member_service
from app.services.member_service import MemberService
from app.schemas.member import StudentCreate, FacultyCreate, MemberResponse

router = APIRouter(prefix="/members", tags=["members"])

def _to_response(member, member_id: str) -> MemberResponse:
    return MemberResponse(
        id= member_id,
        type = type(member).__name__.lower().replace("member",""),
        name=member.name,
        member_id=member.member_id,
        current_loan_count= member.current_loan_count,
        max_loans= member.max_loans(),
    )

@router.post("/students",response_model= dict, status_code=status.HTTP_201_CREATED )
async def add_student(payload: StudentCreate, service: MemberService = Depends(get_member_service)):
    record_id= await service.add_student(payload.name,payload.member_id)
    return {"id": record_id}


@router.post("/faculty",response_model=dict, status_code=status.HTTP_201_CREATED)
async def add_faculty(payload: FacultyCreate, service: MemberService = Depends(get_member_service)):
    record_id=await service.add_faculty(payload.name, payload.member_id)
    return {"id": record_id}

@router.get("/{record_id}", response_model=MemberResponse)
async def get_member(record_id: str, service : MemberService = Depends(get_member_service)):
    member= await service.get_member(record_id)
    if member is None:
        raise HTTPException(status_code= 404, detail="Member not found")
    return _to_response(member, record_id)

@router.delete("/{record_id}", response_model= dict)
async def remove_member(record_id: str, service: MemberService= Depends(get_member_service)):
    deleted= await service.remove_member(record_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Member not found")
    return {"deleted": True}
