from datetime import date

from app.domain.loan import Loan
from app.domain.item_factory import item_from_dict
from app.domain.member_factory import member_from_dict
from app.repositories.item_repository import ItemRepository
from app.repositories.member_repository import MemberRepository
from app.repositories.loan_repository import LoanRepository

class LoanService:
    def __init__(self, loan_repo: LoanRepository, item_repo: ItemRepository, member_repo: MemberRepository) -> None:
        self._loans=loan_repo
        self._items=item_repo
        self._members=member_repo

    async def borrow(self, member_id: str, item_id: str)-> str:
        member_data= await self._members.get_by_id(member_id)
        if member_data is None:
            raise ValueError(f"Non member with id: {member_id}")

        item_data=await self._items.get_by_id(item_id)
        if item_data is None:
            raise ValueError(f"No item with itd: {item_id}")

        member = member_from_dict(member_data)
        item = item_from_dict(item_data)

        member.record_borrow(item_id)
        item.borrow_one()

        loan= Loan(member, item, date.today())

        loan_id= await self._loans.create({
            "member_id":member_id,
            "item_id":item_id,
            "borrowed_on": loan.borrowed_on.isoformat(),
            "due_on":loan.due_on.isoformat(),
            "returned_on": None,
        })

        await self._items.update(item_id, {"available_copies": item.available_copies})
        await self._members.update(member_id, {"borrowed_item_ids": member.borrowed_item_ids})

        return loan_id

    async def return_loan(self, loan_id: str, as_of: date | None = None) -> float:
        as_of=as_of or date.today()

        loan_data= await self._loans.get_by_id(loan_id)
        if loan_data is None:
            raise ValueError(f"No loan with id : {loan_id}")
        if loan_data.get("returned_on") is not None:
            raise ValueError("This loan was already returned")

        #rebuilding the item and member involved
        item_data= await self._items.get_by_id(loan_data["item_id"])
        member_data= await self._members.get_by_id(loan_data["member_id"])

        item = item_from_dict(item_data)
        member= member_from_dict(member_data)

        #compute late fee
        due_on=date.fromisoformat(loan_data["due_on"])
        days_late=max(0, (as_of -due_on).days)
        late_fee= days_late * item.late_fee_per_day()

        #update state
        item.return_one()
        member.record_return(loan_data["item_id"])
        await self._items.update(loan_data["item_id"], {"available_copies": item.available_copies})
        await self._members.update(loan_data["member_id"], {"borrowed_item_ids": member.borrowed_item_ids})
        await self._loans.update(loan_id, {"returned_on": as_of.isoformat()})

        return late_fee


    async def list_loans(self) -> list[dict]:
        return await self._loans.get_all()

            