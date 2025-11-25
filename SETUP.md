# Axonsoton - Complete Setup Guide

This guide provides step-by-step instructions to set up and run the complete Axonsoton system, which includes:
1. **Web Application** - GP and Patient dashboards for exercise assignment and tracking
2. **Exercise Detection System** - Python-based real-time exercise detection using MediaPipe

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the System](#running-the-system)
- [Using the Application](#using-the-application)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)

## Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** (version 14 or higher) - [Download](https://nodejs.org/)
- **Python** (version 3.8 or higher) - [Download](https://www.python.org/)
- **npm** (comes with Node.js)
- **pip** (comes with Python)
- **Webcam** (optional, for real-time exercise detection)

### Verify Installation

```bash
node --version    # Should show v14.x or higher
python3 --version # Should show Python 3.8 or higher
npm --version     # Should show 6.x or higher
pip --version     # Should show pip version
```

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/KRAA5H/Axonsoton.git
cd Axonsoton
```

### Step 2: Install Node.js Dependencies

```bash
npm install
```

This installs the required packages for the web application (Express, CORS, body-parser, etc.).

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs the required packages for exercise detection (MediaPipe, OpenCV, NumPy, etc.).

**Optional**: Install the Python package in development mode for easier testing:

```bash
pip install -e .
```

## Running the System

The Axonsoton system has two main components that can be run independently:

### 1. Web Application (GP & Patient Dashboards)

Start the Node.js web server:

```bash
npm start
```

The server will start on port 3000. You should see:
```
Sample data initialized
- 2 GPs
- 3 Patients
- 8 Exercises
- 2 Assignments
Server running on port 3000
Open http://localhost:3000 in your browser
```

**Access the application**: Open your web browser and navigate to:
```
http://localhost:3000
```

### 2. Exercise Detection System (Real-time Tracking)

The exercise detection system can be run separately for patients to perform exercises with real-time feedback.

#### Webcam Demo (Recommended for Patients)

```bash
python examples/webcam_exercise_demo.py
```

**Controls**:
- `q` - Quit the demo
- `s` - Switch to next exercise
- `x` - Reset current session
- `l` - Switch to left side
- `r` - Switch to right side

#### Video Analysis

To analyze a pre-recorded video:

```bash
python examples/video_analysis.py your_video.mp4 --exercise shoulder_flexion
```

## Using the Application

### For GPs (General Practitioners)

1. **Login**: Open http://localhost:3000 and click on a GP user (e.g., "Dr. Sarah Smith")
2. **View Patients**: See the list of all patients in your practice
3. **Assign Exercises**: 
   - Select a patient from the dropdown or click on a patient card
   - Choose an exercise from the available options
   - Set frequency, repetitions, sets, and add any notes
   - Click "Assign Exercise"
4. **Manage Assignments**: View all current assignments in the table, edit or delete as needed
5. **Logout**: Click the "Logout" button in the top right

### For Patients

1. **Login**: Open http://localhost:3000 and click on a patient user (e.g., "John Doe")
2. **View Dashboard**: See your exercise summary (total, active, completed exercises)
3. **View Assigned Exercises**: See all exercises assigned by your GP with:
   - Exercise name and description
   - Frequency and repetitions
   - Instructions from your GP
   - Detailed steps on how to perform the exercise
4. **Mark Complete**: Click "Mark Complete" when you finish an exercise
5. **Filter Exercises**: Use "Show active only" checkbox to filter your view
6. **Perform Exercises with Tracking**: 
   - Follow the instructions provided in each exercise card
   - For real-time tracking and feedback, use the Python exercise detection system (see below)

### Performing Exercises with Real-time Tracking

Patients can use the webcam demo for guided exercise sessions with real-time feedback:

1. Make sure you have a webcam connected
2. Run the exercise detection demo:
   ```bash
   python examples/webcam_exercise_demo.py
   ```
3. Stand in front of the camera with your full body visible
4. Select the appropriate exercise using the `s` key
5. Perform the exercise - the system will:
   - Track your movements in real-time
   - Count repetitions automatically
   - Provide feedback on form and technique
   - Score your performance
6. Press `q` to quit when done

## Testing

### Test the Web Application

Run the Node.js tests:

```bash
npm test
```

This will run all API tests including:
- Authentication tests
- GP routes tests
- Patient routes tests
- Assignment management tests

### Test the Exercise Detection System

Run the Python tests:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

Or if you have pytest installed:

```bash
pytest tests/ -v
```

## System Architecture

```
Axonsoton/
├── src/                          # Node.js backend
│   ├── app.js                    # Main Express application
│   ├── routes/                   # API route handlers
│   │   ├── authRoutes.js         # Authentication endpoints
│   │   ├── gpRoutes.js           # GP-specific endpoints
│   │   └── patientRoutes.js      # Patient-specific endpoints
│   ├── controllers/              # Business logic
│   │   ├── gpController.js       # GP operations
│   │   └── patientController.js  # Patient operations
│   ├── models/                   # Data models
│   │   ├── user.js               # User model (GP/Patient)
│   │   ├── exercise.js           # Exercise model
│   │   └── exerciseAssignment.js # Assignment model
│   ├── middleware/               # Express middleware
│   │   └── auth.js               # Authentication/authorization
│   └── data/                     # Data storage
│       └── store.js              # In-memory data store
├── public/                       # Frontend files
│   ├── index.html                # Main HTML page
│   ├── css/styles.css            # Styling
│   └── js/app.js                 # Frontend JavaScript
├── rehab_exercise_detection/    # Python exercise detection
│   ├── pose_detector.py          # MediaPipe integration
│   ├── angle_calculator.py       # Angle calculations
│   ├── exercises.py              # Exercise definitions
│   ├── exercise_evaluator.py    # Main evaluator
│   └── feedback.py               # Feedback system
├── examples/                     # Example scripts
│   ├── webcam_exercise_demo.py   # Real-time webcam demo
│   └── video_analysis.py         # Video analysis tool
└── tests/                        # Test files
```

## Demo Users

The system comes pre-loaded with demo users for testing:

### GPs (General Practitioners)
- **Dr. Sarah Smith** - dr.smith@hospital.com (password: password123)
- **Dr. Michael Jones** - dr.jones@hospital.com (password: password123)

### Patients
- **John Doe** - john.doe@email.com (password: password123)
- **Jane Wilson** - jane.wilson@email.com (password: password123)
- **Bob Brown** - bob.brown@email.com (password: password123)

**Note**: These are demo credentials for development/testing purposes only. In production, users would register with their own secure credentials.

## Troubleshooting

### Port Already in Use

If you see "Port 3000 is already in use":

```bash
# On Linux/Mac
lsof -ti:3000 | xargs kill -9

# Or use a different port
PORT=3001 npm start
```

### Webcam Not Detected

If the webcam demo cannot access your camera:
- Ensure your webcam is properly connected
- Check that no other application is using the webcam
- Grant camera permissions if prompted by your operating system

### Python Package Import Errors

If you encounter import errors when running Python examples:

```bash
# Reinstall dependencies
pip install -r requirements.txt

# Or install in development mode
pip install -e .
```

### Module Not Found Errors

Make sure you're running commands from the project root directory:

```bash
cd /path/to/Axonsoton
npm start  # For web app
python examples/webcam_exercise_demo.py  # For exercise detection
```

## Additional Features

### Exercise Categories

The system supports four categories of exercises:
- **Stretching** - Gentle stretches for mobility
- **Strength** - Strength-building exercises
- **Balance** - Balance and stability exercises
- **Cardio** - Cardiovascular exercises

### Difficulty Levels

- **Easy** - Suitable for beginners or those with limited mobility
- **Medium** - For patients with some recovery progress
- **Hard** - Advanced exercises for near-full recovery

## Support

For issues or questions, please refer to:
- [Project Documentation](https://docs.google.com/document/d/1nP6FtXBxIDLaF_Th2AUVDnthiqoOZYtdLUcuB1-zIUk/edit?usp=sharing)
- [MediaPipe Documentation](https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker)

## License

MIT License
