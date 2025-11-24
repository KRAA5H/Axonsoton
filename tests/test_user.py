"""
Tests for the User model.
"""

import unittest
from database.user import User


class TestUser(unittest.TestCase):
    """Test cases for User model."""
    
    def test_hash_password(self):
        """Test password hashing."""
        password = "securepassword123"
        hashed = User.hash_password(password)
        
        # Hash should be different from original
        self.assertNotEqual(password, hashed)
        # Hash should be a string
        self.assertIsInstance(hashed, str)
        # Bcrypt hashes start with $2
        self.assertTrue(hashed.startswith('$2'))
    
    def test_verify_password_correct(self):
        """Test password verification with correct password."""
        password = "securepassword123"
        hashed = User.hash_password(password)
        
        self.assertTrue(User.verify_password(password, hashed))
    
    def test_verify_password_incorrect(self):
        """Test password verification with incorrect password."""
        password = "securepassword123"
        wrong_password = "wrongpassword"
        hashed = User.hash_password(password)
        
        self.assertFalse(User.verify_password(wrong_password, hashed))
    
    def test_create_user(self):
        """Test creating a user with hashed password."""
        user = User.create(
            username="testuser",
            email="test@example.com",
            password="securepassword123"
        )
        
        self.assertIsNone(user.id)
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        # Password should be hashed
        self.assertNotEqual(user.password_hash, "securepassword123")
        self.assertTrue(user.password_hash.startswith('$2'))
    
    def test_user_password_verification(self):
        """Test that created user password can be verified."""
        password = "securepassword123"
        user = User.create(
            username="testuser",
            email="test@example.com",
            password=password
        )
        
        self.assertTrue(User.verify_password(password, user.password_hash))
        self.assertFalse(User.verify_password("wrongpassword", user.password_hash))


if __name__ == '__main__':
    unittest.main()
