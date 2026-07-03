from datetime import date, timedelta

from app.domain.items import LibraryItem
from app.domain.members import Member

class Loan:
    def __init__(self,member: Member, item: LibraryItem, borrowed_on: date) -> None:
        self._member=member 
        self._item=item 
        self._borrowed_on=borrowed_on
        self._returned_on: date |None= None

        base_period=item.loan_period_days()
        bonus=member.loan_period_bonus_days()
        self._due_on=borrowed_on + timedelta(days=base_period+bonus)

    @property
    def member(self) -> Member:
        return self._member
    
    @property
    def item(self) -> LibraryItem:
        return self._item
    
    @property
    def borrowed_on(self) -> date:
        return self._borrowed_on
    
    @property
    def due_on(self) -> date:
        return self._due_on
    
    @property
    def returned_on(self) -> date| None:
        return self._returned_on
    
    @property
    def is_returned(self) -> bool:
        return self._returned_on is not None
    

    #-----------------behavior-----------------------------
    def is_overdue(self, as_of: date) ->bool:
        if self.is_returned:
            return False
        return as_of> self._due_on
    
    def days_overdue(self, as_of: date) -> int:
        if not self.is_overdue(as_of):
            return 0
        return (as_of - self._due_on).days
        
    def calculate_late_fee(self, as_of: date) -> float:
        return self.days_overdue(as_of) * self._item.late_fee_per_day()
    
    def mark_returned(self, returned_on: date) -> None:
        if self.is_returned:
            raise ValueError("This loan has already been returned")
        self._returned_on=returned_on