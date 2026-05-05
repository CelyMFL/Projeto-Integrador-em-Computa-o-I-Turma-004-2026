from app.models import User, RoleEnum
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
import re


class UserService:
    """Service for user management with validation and error handling."""

    @staticmethod
    def validate_email(email):
        """Validate email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @staticmethod
    def validate_password(password):
        """Validate password strength (min 6 chars)."""
        return len(password) >= 6

    @staticmethod
    def create_user(nome, email, senha, role=RoleEnum.PROFESSOR):
        """
        Create a new user with validation.
        
        Args:
            nome: User name
            email: User email (must be unique and valid)
            senha: Password (min 6 chars)
            role: User role (default: PROFESSOR)
            
        Returns:
            User object or raises ValueError
        """
        # Validation
        if not nome or not nome.strip():
            raise ValueError("Nome cannot be empty")
        
        if not email or not email.strip():
            raise ValueError("Email cannot be empty")
            
        if not UserService.validate_email(email):
            raise ValueError("Invalid email format")
        
        if not UserService.validate_password(senha):
            raise ValueError("Password must be at least 6 characters")
        
        # Check if email already exists
        existing_user = User.query.filter_by(email=email.lower()).first()
        if existing_user:
            raise ValueError(f"Email '{email}' already registered")
        
        # Check role validity
        if not isinstance(role, RoleEnum):
            raise ValueError(f"Invalid role: {role}")
        
        try:
            user = User(
                nome=nome.strip(),
                email=email.lower().strip(),
                senha=generate_password_hash(senha),
                role=role
            )
            db.session.add(user)
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Error creating user: {str(e)}")

    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID."""
        return User.query.get(user_id)

    @staticmethod
    def get_user_by_email(email):
        """Get user by email."""
        return User.query.filter_by(email=email.lower().strip()).first()

    @staticmethod
    def list_users_by_role(role):
        """List all users with specific role."""
        if not isinstance(role, RoleEnum):
            raise ValueError(f"Invalid role: {role}")
        return User.query.filter_by(role=role).all()

    @staticmethod
    def update_user_role(user_id, new_role):
        """
        Update user role.
        
        Args:
            user_id: User ID
            new_role: New role (RoleEnum)
            
        Returns:
            Updated User object or raises ValueError
        """
        if not isinstance(new_role, RoleEnum):
            raise ValueError(f"Invalid role: {new_role}")
        
        user = UserService.get_user_by_id(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")
        
        try:
            user.role = new_role
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Error updating user role: {str(e)}")

    @staticmethod
    def list_all_users():
        """Get all users."""
        return User.query.all()

    @staticmethod
    def delete_user(user_id):
        """Delete user by ID."""
        user = UserService.get_user_by_id(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")
        
        try:
            db.session.delete(user)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Error deleting user: {str(e)}")