import re
from typing import Optional


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


class RegisterDTO:
    def __init__(self, register_firstname: Optional[str] = None,
                 register_lastname: Optional[str] = None,
                 register_gender: Optional[int] = None,
                 register_email: Optional[str] = None,
                 register_username: Optional[str] = None,
                 register_password: Optional[str] = None):

        self.register_firstname = register_firstname
        self.register_lastname = register_lastname
        self.register_gender = register_gender
        self.register_email = register_email
        self.register_username = register_username
        self.register_password = register_password

    def validate(self):
        if not all([self.register_firstname, self.register_lastname,
                    self.register_gender, self.register_email,
                    self.register_username,
                    self.register_password]):
            raise ValidationError("All fields must be filled and valid.")

        password_pattern = re.compile(
            r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')
        if not password_pattern.match(self.register_password):
            raise ValidationError(
                "Password must be at least 8 characters long, include an uppercase letter, "
                "a lowercase letter, a number, and a special character.")

        return self
