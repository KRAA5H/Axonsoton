"""
SQLite database operations for user login details.
"""

import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Generator, Optional

from .user import User


class Database:
    """SQLite database for storing user login details."""
    
    def __init__(self, db_path: str = "users.db"):
        """Initialize the database connection.
        
        Args:
            db_path: Path to the SQLite database file.
        """
        self.db_path = db_path
        self._create_tables()
    
    @contextmanager
    def _get_connection(self) -> Generator[sqlite3.Connection, None, None]:
        """Get a database connection context manager.
        
        Yields:
            A SQLite connection object.
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def _create_tables(self) -> None:
        """Create the users table if it doesn't exist."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            # Create index on username and email for faster lookups
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)
            ''')
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)
            ''')
    
    def create_user(self, user: User) -> User:
        """Insert a new user into the database.
        
        Args:
            user: The User object to insert.
            
        Returns:
            The User object with the assigned id.
            
        Raises:
            sqlite3.IntegrityError: If username or email already exists.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                INSERT INTO users (username, email, password_hash)
                VALUES (?, ?, ?)
                ''',
                (user.username, user.email, user.password_hash)
            )
            user.id = cursor.lastrowid
            # Fetch the created_at and updated_at timestamps
            cursor.execute(
                'SELECT created_at, updated_at FROM users WHERE id = ?',
                (user.id,)
            )
            row = cursor.fetchone()
            if row:
                user.created_at = datetime.fromisoformat(row['created_at'])
                user.updated_at = datetime.fromisoformat(row['updated_at'])
        return user
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Retrieve a user by their ID.
        
        Args:
            user_id: The ID of the user to retrieve.
            
        Returns:
            The User object if found, None otherwise.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM users WHERE id = ?',
                (user_id,)
            )
            row = cursor.fetchone()
            if row:
                return self._row_to_user(row)
        return None
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Retrieve a user by their username.
        
        Args:
            username: The username to search for.
            
        Returns:
            The User object if found, None otherwise.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM users WHERE username = ?',
                (username,)
            )
            row = cursor.fetchone()
            if row:
                return self._row_to_user(row)
        return None
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Retrieve a user by their email.
        
        Args:
            email: The email address to search for.
            
        Returns:
            The User object if found, None otherwise.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM users WHERE email = ?',
                (email,)
            )
            row = cursor.fetchone()
            if row:
                return self._row_to_user(row)
        return None
    
    def update_user(self, user: User) -> bool:
        """Update an existing user's details.
        
        Args:
            user: The User object with updated details.
            
        Returns:
            True if the user was updated, False if not found.
        """
        if user.id is None:
            return False
            
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                UPDATE users
                SET username = ?, email = ?, password_hash = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                ''',
                (user.username, user.email, user.password_hash, user.id)
            )
            return cursor.rowcount > 0
    
    def delete_user(self, user_id: int) -> bool:
        """Delete a user from the database.
        
        Args:
            user_id: The ID of the user to delete.
            
        Returns:
            True if the user was deleted, False if not found.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'DELETE FROM users WHERE id = ?',
                (user_id,)
            )
            return cursor.rowcount > 0
    
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate a user with username and password.
        
        Args:
            username: The username to authenticate.
            password: The plain text password to verify.
            
        Returns:
            The User object if authentication succeeds, None otherwise.
        """
        user = self.get_user_by_username(username)
        if user and User.verify_password(password, user.password_hash):
            return user
        return None
    
    def get_all_users(self) -> list[User]:
        """Retrieve all users from the database.
        
        Returns:
            A list of all User objects.
        """
        users = []
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users ORDER BY id')
            for row in cursor.fetchall():
                users.append(self._row_to_user(row))
        return users
    
    def _row_to_user(self, row: sqlite3.Row) -> User:
        """Convert a database row to a User object.
        
        Args:
            row: The database row.
            
        Returns:
            A User object.
        """
        return User(
            id=row['id'],
            username=row['username'],
            email=row['email'],
            password_hash=row['password_hash'],
            created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None,
            updated_at=datetime.fromisoformat(row['updated_at']) if row['updated_at'] else None
        )
    
    def close(self) -> None:
        """Clean up resources. For SQLite, connections are closed after each operation."""
        pass
    
    def delete_database(self) -> None:
        """Delete the database file. Use with caution."""
        path = Path(self.db_path)
        if path.exists():
            path.unlink()
