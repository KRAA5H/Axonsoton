"""
Tests for the Database class.
"""

import os
import sqlite3
import tempfile
import unittest
from database.db import Database
from database.user import User


class TestDatabase(unittest.TestCase):
    """Test cases for Database operations."""
    
    def setUp(self):
        """Set up test database."""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_users.db")
        self.db = Database(self.db_path)
    
    def tearDown(self):
        """Clean up test database."""
        self.db.close()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        os.rmdir(self.temp_dir)
    
    def test_create_user(self):
        """Test creating a new user."""
        user = User.create(
            username="testuser",
            email="test@example.com",
            password="securepassword123"
        )
        
        created_user = self.db.create_user(user)
        
        self.assertIsNotNone(created_user.id)
        self.assertEqual(created_user.username, "testuser")
        self.assertEqual(created_user.email, "test@example.com")
        self.assertIsNotNone(created_user.created_at)
        self.assertIsNotNone(created_user.updated_at)
    
    def test_create_duplicate_username(self):
        """Test that duplicate username raises an error."""
        user1 = User.create(
            username="testuser",
            email="test1@example.com",
            password="password1"
        )
        self.db.create_user(user1)
        
        user2 = User.create(
            username="testuser",  # Same username
            email="test2@example.com",
            password="password2"
        )
        
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.create_user(user2)
    
    def test_create_duplicate_email(self):
        """Test that duplicate email raises an error."""
        user1 = User.create(
            username="testuser1",
            email="test@example.com",
            password="password1"
        )
        self.db.create_user(user1)
        
        user2 = User.create(
            username="testuser2",
            email="test@example.com",  # Same email
            password="password2"
        )
        
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.create_user(user2)
    
    def test_get_user_by_id(self):
        """Test retrieving a user by ID."""
        user = User.create(
            username="testuser",
            email="test@example.com",
            password="securepassword123"
        )
        created_user = self.db.create_user(user)
        
        retrieved_user = self.db.get_user_by_id(created_user.id)
        
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.id, created_user.id)
        self.assertEqual(retrieved_user.username, "testuser")
        self.assertEqual(retrieved_user.email, "test@example.com")
    
    def test_get_user_by_id_not_found(self):
        """Test retrieving a non-existent user by ID."""
        retrieved_user = self.db.get_user_by_id(9999)
        self.assertIsNone(retrieved_user)
    
    def test_get_user_by_username(self):
        """Test retrieving a user by username."""
        user = User.create(
            username="testuser",
            email="test@example.com",
            password="securepassword123"
        )
        self.db.create_user(user)
        
        retrieved_user = self.db.get_user_by_username("testuser")
        
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.username, "testuser")
    
    def test_get_user_by_username_not_found(self):
        """Test retrieving a non-existent user by username."""
        retrieved_user = self.db.get_user_by_username("nonexistent")
        self.assertIsNone(retrieved_user)
    
    def test_get_user_by_email(self):
        """Test retrieving a user by email."""
        user = User.create(
            username="testuser",
            email="test@example.com",
            password="securepassword123"
        )
        self.db.create_user(user)
        
        retrieved_user = self.db.get_user_by_email("test@example.com")
        
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.email, "test@example.com")
    
    def test_get_user_by_email_not_found(self):
        """Test retrieving a non-existent user by email."""
        retrieved_user = self.db.get_user_by_email("nonexistent@example.com")
        self.assertIsNone(retrieved_user)
    
    def test_update_user(self):
        """Test updating a user."""
        user = User.create(
            username="testuser",
            email="test@example.com",
            password="securepassword123"
        )
        created_user = self.db.create_user(user)
        
        # Update username and email
        created_user.username = "updateduser"
        created_user.email = "updated@example.com"
        
        result = self.db.update_user(created_user)
        
        self.assertTrue(result)
        
        # Verify the update
        retrieved_user = self.db.get_user_by_id(created_user.id)
        self.assertEqual(retrieved_user.username, "updateduser")
        self.assertEqual(retrieved_user.email, "updated@example.com")
    
    def test_update_user_not_found(self):
        """Test updating a non-existent user."""
        user = User(
            id=9999,
            username="testuser",
            email="test@example.com",
            password_hash="somehash"
        )
        
        result = self.db.update_user(user)
        
        self.assertFalse(result)
    
    def test_update_user_no_id(self):
        """Test updating a user without an ID."""
        user = User.create(
            username="testuser",
            email="test@example.com",
            password="securepassword123"
        )
        
        result = self.db.update_user(user)
        
        self.assertFalse(result)
    
    def test_delete_user(self):
        """Test deleting a user."""
        user = User.create(
            username="testuser",
            email="test@example.com",
            password="securepassword123"
        )
        created_user = self.db.create_user(user)
        
        result = self.db.delete_user(created_user.id)
        
        self.assertTrue(result)
        
        # Verify deletion
        retrieved_user = self.db.get_user_by_id(created_user.id)
        self.assertIsNone(retrieved_user)
    
    def test_delete_user_not_found(self):
        """Test deleting a non-existent user."""
        result = self.db.delete_user(9999)
        self.assertFalse(result)
    
    def test_authenticate_user_success(self):
        """Test successful user authentication."""
        password = "securepassword123"
        user = User.create(
            username="testuser",
            email="test@example.com",
            password=password
        )
        self.db.create_user(user)
        
        authenticated_user = self.db.authenticate_user("testuser", password)
        
        self.assertIsNotNone(authenticated_user)
        self.assertEqual(authenticated_user.username, "testuser")
    
    def test_authenticate_user_wrong_password(self):
        """Test authentication with wrong password."""
        user = User.create(
            username="testuser",
            email="test@example.com",
            password="securepassword123"
        )
        self.db.create_user(user)
        
        authenticated_user = self.db.authenticate_user("testuser", "wrongpassword")
        
        self.assertIsNone(authenticated_user)
    
    def test_authenticate_user_not_found(self):
        """Test authentication with non-existent user."""
        authenticated_user = self.db.authenticate_user("nonexistent", "password")
        
        self.assertIsNone(authenticated_user)
    
    def test_get_all_users(self):
        """Test retrieving all users."""
        user1 = User.create(username="user1", email="user1@example.com", password="password1")
        user2 = User.create(username="user2", email="user2@example.com", password="password2")
        user3 = User.create(username="user3", email="user3@example.com", password="password3")
        
        self.db.create_user(user1)
        self.db.create_user(user2)
        self.db.create_user(user3)
        
        users = self.db.get_all_users()
        
        self.assertEqual(len(users), 3)
        usernames = [u.username for u in users]
        self.assertIn("user1", usernames)
        self.assertIn("user2", usernames)
        self.assertIn("user3", usernames)
    
    def test_get_all_users_empty(self):
        """Test retrieving all users when database is empty."""
        users = self.db.get_all_users()
        self.assertEqual(len(users), 0)


if __name__ == '__main__':
    unittest.main()
