from typing import Optional
from xml.dom import ValidationErr


class LoginDTO:
    def __init__(self, login_username: Optional[str] = None,
                 login_password: Optional[str] = None):
        self.login_username = login_username
        self.login_password = login_password

    def validate(self):
        if not all([self.login_username, self.login_password]):
            raise ValidationErr("Username and password are required.")
        return self

    def __repr__(self):
        return f"LoginDTO(username={self.login_username!r}, password={self.login_password!r})"
