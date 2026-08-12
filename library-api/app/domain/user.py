from app.schemas.user import UserRole

class User:
    def __init__(self, username: str, hashed_password: str, role, UserRole) -> None:
        self._username = username
        self._hashed_password = hashed_password
        self._role = role

    @property
    def username(self) -> str:
        return self._username

    @property
    def hashed_password(self) -> str:
        return self._hashed_password

    @property
    def role(self) -> UserRole:
        return self._role

    @property
    def is_admin(self) -> bool:
        return self._role == UserRole.ADMIN

    def to_dict(self) -> dict:
        return {
            "username": self._username,
            "hashed_password": self._hashed_password,
            "role": self._role.value,
        } 