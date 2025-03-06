from base import db
from base.com.vo.login_vo import LoginVO
from base.utils.my_logger import get_logger

logger = get_logger()


class LoginDao:
    """Data access object for login related database operations."""

    @staticmethod
    def insert_login(login_vo):
        """Insert new login record into database.
        
        Args:
            login_vo: LoginVO object containing login details
            
        Returns:
            int: ID of inserted login record
        """
        db.session.add(login_vo)
        db.session.commit()
        logger.info(f"Inserted login with ID: {login_vo.login_id}")
        return login_vo.login_id

    @staticmethod
    def validate_login(username, password):
        """Validate user login credentials.
        
        Args:
            username: User's username
            password: User's password
            
        Returns:
            LoginVO: User object if credentials are valid, None otherwise
        """
        user = LoginVO.query.filter_by(login_username=username).first()
        # print("User found:", user)
        logger.info(f"Query Result for username {username}: {user}")

        if user and user.login_status == 0  :
            if user.login_password == password:
                logger.info(f"User {username} validated successfully.")
                # print("User validated successfully.")
                return user
            else:
                logger.warning(f"Invalid password for user: {username}")
        else:
            if not user:
                logger.warning(f"User not found: {username}")
            else:
                logger.warning(f"User account is not active: {username}")

        return None
