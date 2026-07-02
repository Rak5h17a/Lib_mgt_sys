from abc import ABC, abstractmethod

class Member(ABC):
    def __init__(self,name: str, member_id: str) -> None:
        self._name=name
        self._member_id=member_id
        self._borrowed_item_ids: list[str]=[]

    @property
    def name(self) -> str:
        return self._name
    
    @property
    def member_id(self) -> str:
        return self._member_id

    @property 
    def borrowed_item_ids(self) -> list[str]:
        return list(self._borrowed_item_ids)
    
    @property
    def current_loan_count(self) -> int:
        return len(self._borrowed_item_ids)
    
    @abstractmethod
    def max_loans(self) -> int:
        ...

    @abstractmethod
    def loan_period_bonus_days(self) -> int:
        ...

    #-------------------------shared behavior-----------------------------------
    def can_borrow(self) -> bool:
        return len(self._borrowed_item_ids)< self.max_loans()
    
    def record_borrow(self, item_id: str) -> None:
        if not self.can_borrow():
            raise ValueError(f"{self._name} has reached the borrowing limit of {self.max_loans()}")
        self._borrowed_item_ids.append(item_id)

    def record_return(self,item_id: str) -> None:
        if item_id not in self._borrowed_item_ids:
            raise ValueError(f"{self._name} has not borrowed {item_id}")
        self._borrowed_item_ids.remove(item_id)

class StudentMember(Member):
    def max_loans(self) -> int:
        return 3
    
    def loan_period_bonus_days(self):
        return 0
    
class FacultyMember(Member):
    def max_loans(self):
        return 10
    
    def loan_period_bonus_days(self):
        return 14