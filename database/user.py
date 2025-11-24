"""
User model for login details.
"""

import bcrypt
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    """Represents a user with login credentials."""
    
    id: Optional[int]
    username: str
    email: str
    password_hash: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt.
        
        Args:
            password: The plain text password to hash.
            
        Returns:
            The hashed password as a string.
        """
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """Verify a password against a hash.
        
        Args:
            password: The plain text password to verify.
            password_hash: The hashed password to check against.
            
        Returns:
            True if the password matches, False otherwise.
        """
        return bcrypt.checkpw(
            password.encode('utf-8'),
            password_hash.encode('utf-8')
        )
    
    @classmethod
    def create(cls, username: str, email: str, password: str) -> 'User':
        """Create a new user with a hashed password.
        
        Args:
            username: The username for the new user.
            email: The email address for the new user.
            password: The plain text password to hash.
            
        Returns:
            A new User instance with the hashed password.
        """
        password_hash = cls.hash_password(password)
        return cls(
            id=None,
            username=username,
            email=email,
            password_hash=password_hash
        )
