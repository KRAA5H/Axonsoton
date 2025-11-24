# Rehab Exercise Detection System

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
A Python-based system that uses MediaPipe to detect whether a patient is correctly performing rehabilitation exercises used to cure/improve gross motor disorders.

## Features

- **Real-time pose detection** using MediaPipe Pose
- **Multiple exercise support**:
  - Shoulder Flexion
  - Shoulder Abduction
  - Elbow Flexion
  - Knee Flexion
  - Hip Flexion
  - Hip Abduction
- **Accurate angle measurement** for joint positions
- **Real-time feedback** with quality scoring
- **Repetition tracking** with session management
- **Customizable exercise parameters** (target angles, tolerance, etc.)
- **Support for both webcam and video file analysis**

## Installation

### Requirements

- Python 3.8 or higher
- Webcam (for real-time detection)

### Install Dependencies

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
Or install the package directly:

```bash
pip install -e .
```

## Quick Start

### Basic Usage

```python
from rehab_exercise_detection import (
    ExerciseEvaluator,
    ExerciseConfig,
    ShoulderFlexion
)

# Create an exercise with custom configuration
config = ExerciseConfig(
    target_angle=90.0,    # Target 90 degrees
    tolerance=15.0,       # ±15 degrees acceptable
    side='left'           # Evaluate left arm
)

# Create the evaluator
evaluator = ExerciseEvaluator(target_reps=10)
evaluator.set_exercise_by_name('shoulder_flexion', config)

# Start a session
evaluator.start_session()

# Process video frames (example with OpenCV)
import cv2
cap = cv2.VideoCapture(0)  # Use webcam

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Evaluate the frame
    feedback = evaluator.evaluate_frame(frame)
    
    # Draw feedback overlay
    annotated = evaluator.draw_feedback(frame, feedback)
    
    # Display
    cv2.imshow('Exercise Detection', annotated)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

### Run the Webcam Demo

```bash
python examples/webcam_exercise_demo.py
```

### Analyze a Video File

```bash
python examples/video_analysis.py input_video.mp4 --exercise shoulder_flexion
```

## Supported Exercises

### Upper Body

| Exercise | Description | Default Target |
|----------|-------------|----------------|
| Shoulder Flexion | Raise arm forward and upward | 90° |
| Shoulder Abduction | Raise arm sideways | 90° |
| Elbow Flexion | Bend elbow | 140° |

### Lower Body

| Exercise | Description | Default Target |
|----------|-------------|----------------|
| Knee Flexion | Bend knee | 90° |
| Hip Flexion | Raise thigh forward | 90° |
| Hip Abduction | Move leg sideways | 30° |

## API Reference

### ExerciseEvaluator

The main class for evaluating exercises:

```python
evaluator = ExerciseEvaluator(target_reps=10)

# Set exercise by name
evaluator.set_exercise_by_name('shoulder_flexion', config)

# Or set exercise directly
evaluator.set_exercise(ShoulderFlexion(config))

# Start a session
evaluator.start_session()

# Evaluate a frame
feedback = evaluator.evaluate_frame(frame)

# Get session summary
summary = evaluator.get_session_summary()
```

### ExerciseFeedback

Feedback object returned from evaluation:

```python
feedback.is_correct      # bool: Whether position is correct
feedback.level           # FeedbackLevel: EXCELLENT, GOOD, NEEDS_IMPROVEMENT, INCORRECT, ERROR
feedback.score           # float: 0-100 score
feedback.current_angle   # float: Current measured angle
feedback.target_angle    # float: Target angle
feedback.messages        # List[str]: Feedback messages
feedback.corrections     # List[str]: Suggested corrections
```

### ExerciseConfig

Configuration for exercises:

```python
config = ExerciseConfig(
    target_angle=90.0,     # Target angle in degrees
    tolerance=15.0,        # Acceptable deviation
    min_angle=0.0,         # Minimum angle (for range-based)
    max_angle=180.0,       # Maximum angle (for range-based)
    hold_duration=0.0,     # Required hold time in seconds
    repetitions=1,         # Target repetitions
    side='left',           # 'left' or 'right'
    use_3d=False           # Use 3D angle calculation
)
```

## Architecture

```
rehab_exercise_detection/
├── __init__.py              # Package exports
├── pose_detector.py         # MediaPipe pose detection wrapper
├── angle_calculator.py      # Joint angle calculations
├── exercises.py             # Exercise definitions
├── exercise_evaluator.py    # High-level evaluation logic
└── feedback.py              # Feedback generation
```

## Testing

Run the tests:

```bash
pytest tests/ -v
```

## References

- [MediaPipe Pose](https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker)
- [MediaPipe Gesture Recognizer](https://ai.google.dev/edge/mediapipe/solutions/vision/gesture_recognizer)
- [Project Documentation](https://docs.google.com/document/d/1nP6FtXBxIDLaF_Th2AUVDnthiqoOZYtdLUcuB1-zIUk/edit?usp=sharing)

## License

MIT License
