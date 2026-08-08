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

    @property 
    def total_copies(self) -> int:
        return self._total_copies
    
    @abstractmethod 
    def late_fee_per_day(self) ->float:
        ...

    @abstractmethod
    def loan_period_days(self) ->int:
        ...

    def to_dict(self)->dict:
        return{
            "title": self._title,
            "total_copies":self._total_copies,
            "available_copies":self._available_copies

        }
    
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

    
### ----------------Items: Books, Magazines, DVD's--------------
class Book(LibraryItem):
    def __init__(self, title : str ,total_copies: int, author: str, isbn: str) -> None:
        super().__init__(title, total_copies)
        self._author=author
        self._isbn=isbn

    @property
    def author(self) -> str:
        return self._author
    
    @property
    def isbn(self) -> str:
        return self._isbn

    def to_dict(self) ->dict:
        data= super().to_dict()
        data["type"]="book"
        data["author"]=self._author
        data["isbn"]=self._isbn
        return data

    def late_fee_per_day(self) -> float:
        return 1.0
    
    def loan_period_days(self) -> int:
        return 21
    
class Magazine(LibraryItem):
    def __init__(self, title: str, total_copies: int, issue_number: int) -> None:
        super().__init__(title,total_copies)
        self._issue_number=issue_number

    @property
    def issue_number(self) -> int:
        return self._issue_number

    def to_dict(self) ->dict:
        data= super().to_dict()
        data["type"]="magazine"
        data["issue_number"]=self._issue_number
        return data
    
    def late_fee_per_day(self) -> float:
        return 0.5
    
    def loan_period_days(self) -> int:
        return 7
        
class DVD(LibraryItem):
    def __init__(self, title: str, total_copies: int, runtime_minutes: int) -> None:
        super().__init__(title,total_copies)
        self._runtime_minutes=runtime_minutes

    @property
    def runtime_minutes(self):
        return self._runtime_minutes

    def to_dict(self):
        data= super().to_dict()
        data["type"]="dvd"
        data["runtime_minutes"]=self._runtime_minutes
        return data    
    def late_fee_per_day(self):
        return 5.0
    
    def loan_period_days(self):
        return 3