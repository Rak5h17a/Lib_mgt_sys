from datetime import date 
from app.domain.items import Book, Magazine, DVD

def test_book_has_correct_loan_period():
    book=Book("Clean Code", 3 , "Robert Martin", "234-8765755")
    assert book.loan_period_days()==21
    assert book.late_fee_per_day() ==1.0

def test_dvd_has_shorter_loan_and_steeper_fee():
    dvd= DVD("Inception", 2, 140)
    assert dvd.loan_period_days() ==3
    assert dvd.late_fee_per_day() ==5

def test_new_item_starts_fully_available():
    book= Book("Test",5,"Author","123")
    assert book.available_copies == 5
    assert book.is_available == True 

def test_borrowing_decrements_available_copies():
    book= Book("Test", 3, "Author", "123")
    book.borrow_one()
    assert book.available_copies ==2

def test_borrowing_when_empty_raises_error():
    book= Book("Test", 1, "Author","123")
    book.borrow_one()
    try:
        book.borrow_one()
        assert False, "Excepted a ValueError but none was raised"
    except ValueError:
        pass 

def test_due_date_uses_polymorphic_loan_period():
    borrowed =  date(2025,1,1)
    book= Book("B",1,"A","1")
    dvd= DVD("D",1,100)
    assert book.due_date(borrowed) == date(2025,1,22)
    assert dvd.due_date(borrowed) == date(2025,1,4)