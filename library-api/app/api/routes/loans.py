from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_loan_service
from app.domain.user import User
from app.api.auth_deps import get_current_user
from app.services.loan_service import LoanService
from app.schemas.loan import BorrowRequest, ReturnResponse, LoanResponse

router = APIRouter(prefix="/loans", tags=["loans"])

@router.post("/borrow", response_model=dict, status_code=status.HTTP_201_CREATED)
async def borrow(payload: BorrowRequest, 
                 service: LoanService =  Depends(get_loan_service),
                 current_user: User = Depends(get_current_user)):
    try:
        loan_id= await service.borrow(payload.member_id, payload.item_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"loan_id": loan_id}

@router.post("/{loan_id}/return", response_model= ReturnResponse)
async def return_loan(loan_id: str,
                    service: LoanService = Depends(get_loan_service),
                    current_user : User = Depends(get_current_user)):
    try:
        late_fee= await service.return_loan(loan_id)
    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e))
    return ReturnResponse(
        loan_id=loan_id,
        late_fee=late_fee,
        message= "Returned Successfully" if late_fee ==0 else f"Returned with late fee {late_fee}"
    )

@router.get("/", response_model=list[LoanResponse])
async def list_loan(service: LoanService = Depends(get_loan_service),
                    current_user: User = Depends(get_current_user)):
    loans = await service.list_loans()
    return [
        LoanResponse(
            id= loan["id"],
            member_id=loan["member_id"],
            item_id=loan["item_id"],
            borrowed_on=loan["borrowed_on"],
            due_on=loan["due_on"],
            returned_on=loan.get("returned_on"), 
        )
        for loan in loans
    ]