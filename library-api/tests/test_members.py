from pickle import TRUE

from app.domain.members import StudentMember,FacultyMember

def test_student_max_loan_is_three():
    student=StudentMember("Alice","S001")
    assert student.max_loans() == 3
    assert student.loan_period_bonus_days() ==0

def test_faculty_has_higher_limit_and_bonus():
    faculty=FacultyMember("Dr. Bose","F001")
    assert faculty.max_loans() == 10
    assert faculty.loan_period_bonus_days()== 14

def test_new_member_has_no_loans():
    student= StudentMember("Ray","S001")
    assert student.current_loan_count== 0
    assert student.can_borrow() is True

def test_recording_borrows_increases_count():
    student= StudentMember("Yan","S001")
    student.record_borrow("item-1")
    student.record_borrow("ïtem-2")
    assert student.current_loan_count==2

def test_borrowing_past_limit_is_blocked():
    student= StudentMember("Yan","S001")
    student.record_borrow("item-1")
    student.record_borrow("ïtem-2")
    student.record_borrow("ïtem-3")
    assert student.can_borrow() == False

    import pytest 
    with pytest.raises(ValueError):
        student.record_borrow("item-4")

def test_returning_removes_from_borrow_list():
    student = StudentMember("Alice", "S001")
    student.record_borrow("item-1")
    student.record_return("item-1")
    assert student.current_loan_count ==0
