https://docs.google.com/document/d/1nP6FtXBxIDLaF_Th2AUVDnthiqoOZYtdLUcuB1-zIUk/edit?usp=sharinghttps://docs.google.com/document/d/1nP6FtXBxIDLaF_Th2AUVDnthiqoOZYtdLUcuB1-zIUk/edit?usp=sharing

https://ai.google.dev/edge/mediapipe/solutions/vision/gesture_recognizer

## User Login Database

A SQLite-based database module for storing and managing user login details with secure password hashing.

### Features

- **Secure Password Storage**: Uses bcrypt for secure password hashing
- **User Management**: Full CRUD operations (Create, Read, Update, Delete)
- **User Authentication**: Verify user credentials with username and password
- **SQLite Database**: Lightweight, file-based database requiring no external server
- **Duplicate Prevention**: Enforces unique usernames and email addresses

### Installation

```bash
pip install -r requirements.txt
```

### Usage

```python
from database import Database, User

# Initialize the database
db = Database("users.db")

# Create a new user
user = User.create(
    username="john_doe",
    email="john@example.com",
    password="securepassword123"
)
created_user = db.create_user(user)

# Authenticate a user
authenticated = db.authenticate_user("john_doe", "securepassword123")
if authenticated:
    print(f"Welcome, {authenticated.username}!")

# Get user by username or email
user = db.get_user_by_username("john_doe")
user = db.get_user_by_email("john@example.com")

# Update user details
user.email = "newemail@example.com"
db.update_user(user)

# Delete a user
db.delete_user(user.id)

# Get all users
all_users = db.get_all_users()
```

### Database Schema

The `users` table includes:
- `id`: Auto-incrementing primary key
- `username`: Unique username (indexed)
- `email`: Unique email address (indexed)
- `password_hash`: Bcrypt-hashed password
- `created_at`: Timestamp of user creation
- `updated_at`: Timestamp of last update

### Running Tests

```bash
python -m unittest discover -s tests -v
```
