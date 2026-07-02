from abc import ABC, abstractmethod
from datetime import date,timedelta 

class LibraryItem(ABC):
    def __init__(self, title:str, total_copies:int) -> None:
        self._title=title
        self._total_copies=total_copies
        self._available_copies=total_copies #all copies are initially available


    @property
    def title(self) -> str:
        return self._title 
    
    @property
    def available_copies(self) -> int:
        return self._available_copies 
    
    @property
    def is_available(self) ->bool:
        return self._available_copies>0
    
    @abstractmethod 
    def late_fee_per_day(self) ->float:
        ...

    @abstractmethod
    def loan_period_days(self) ->int:
        ...
    
    #shared behavior
    def due_date(self, borrowed_on:date) -> date:
        return borrowed_on + timedelta(days=self.loan_period_days())
    
    def borrow_one(self) -> None:
        if not self.is_available:
            raise ValueError(f"'{self.title}' has no available copies")
        self._available_copies -= 1

    def return_one(self) -> None:
        if self._available_copies >= self._total_copies:
            raise ValueError(f"Cannot return more than what exists for '{self._title}'")
        self._available_copies += 1

    
    