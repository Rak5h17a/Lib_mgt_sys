from app.core.database import get_database

from app.repositories.item_repository import ItemRepository
from app.repositories.member_repository import MemberRepository
from app.repositories.loan_repository import LoanRepository

from app.services.item_service import ItemService
from app.services.member_service import MemberService
from app.services.loan_service import LoanService

def get_item_service() -> ItemService:
    db = get_database()
    return ItemService(ItemRepository(db))

def get_member_service() -> MemberService:
    db = get_database()
    return MemberService(MemberRepository(db))

def get_loan_service() -> LoanService:
    db = get_database()
    return LoanService(LoanRepository(db), ItemRepository(db), MemberRepository(db)) 