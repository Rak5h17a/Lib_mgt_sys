from datetime import date 

from app.domain.loan import Loan 
from app.domain.items import Book, DVD, Magazine
from app.domain.members import StudentMember, FacultyMember

def test_student_due_date_uses_item_period_only():
    book= Book("B",1,"A",1)
    student= StudentMember("Ray","S001")
    loan= Loan(student, book, date(2026,1,1))
    assert loan.due_on == date(2026,1,22)

def test_faculty_due_date():
    book= Book("B",1,"A",1)
    faculty= FacultyMember("Yan","F001")
    loan= Loan(faculty,book,date(2026,1,1))
    assert loan.due_on == date(2026,2,5)

def test_loan_not_overdue_before_due_date():
    dvd= DVD("D",1,100)
    student=StudentMember("Alice","S001")
    loan= Loan(student,dvd,date(2026,1,1))
    assert loan.is_overdue(date(2026,1,3)) is False

def test_overdue_dvd_late_fee():
    dvd= DVD("D",1,100)
    student=StudentMember("Alice","S001")
    loan= Loan(student,dvd,date(2026,1,1))
    check= date(2026,1,10)
    assert loan.days_overdue(check) == 6
    assert loan.calculate_late_fee(check) ==30.0

def test_returned_loan_is_not_overdue():
    book = Book("B", 1, "A", "1")
    student = StudentMember("Alice", "S001")
    loan = Loan(student, book, date(2025, 1, 1))
    loan.mark_returned(date(2025,2,1))
    assert loan.is_overdue(date(2025,3,1)) == False


    
    