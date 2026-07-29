from app.domain.members import StudentMember,FacultyMember,Member
from app.domain.member_factory import member_from_dict
from app.repositories.member_repository import MemberRepository

class MemberService:

    def __init__(self, repository: MemberRepository) -> None:
        self._repository= repository

    async def add_student(self, name: str, member_id: str) -> str:
        student= StudentMember(name,member_id)
        return await self._repository.create(student.to_dict())

    async def add_faculty(self, name:str, member_id: str) -> str:
        faculty =  FacultyMember(name, member_id)
        return await self._repository.create(faculty.to_dict())

    async def get_member(self, record_id: str)-> Member:
        # sourcery skip: assign-if-exp, reintroduce-else
        data= await self._repository.get_by_id(record_id)
        if data is None:
            return None
        return member_from_dict(data)

    async def list_members(self) -> list[Member]:
        documents= await self._repository.get_all()
        return [member_from_dict(doc) for doc in documents]

    async def remove_member(self, record_id:str) -> bool:
        return await self._repository.delete(record_id)