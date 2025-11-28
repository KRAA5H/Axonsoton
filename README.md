# Axonsoton - Rehabilitation Exercise Management System

A comprehensive system for managing and tracking rehabilitation exercises, combining a web-based assignment platform for GPs and patients with real-time exercise detection using AI.

![Patient Dashboard](https://github.com/user-attachments/assets/f9e74a9e-8c95-4a9b-a9a9-4cc9b4653687)
![GP Dashboard](https://github.com/user-attachments/assets/ae70c838-b3c5-4984-b02b-12ea80e26a28)

## 🚀 Quick Start

**Want to get started immediately?** See **[SETUP.md](SETUP.md)** for complete installation and usage instructions.

```bash
# 1. Install Node.js dependencies
npm install

# 2. Create Python 3.12 virtual environment
python3.12 -m venv venv
source venv/bin/activate  # On Linux/Mac
# venv\Scripts\activate   # On Windows

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Start the web application
npm start

# 5. Open browser to http://localhost:3000
```

## Overview

Axonsoton is a dual-component rehabilitation system designed to improve patient outcomes:

### 1. Web Application (GP & Patient Portal)

A user-friendly platform where:
- **GPs** can assign customized exercises to patients with specific parameters
- **Patients** can view, track, and complete their personalized exercise plans

### 2. Exercise Detection System (AI-Powered Tracking)

A Python-based system using MediaPipe that:
- Provides real-time feedback on exercise form and technique
- Automatically counts repetitions
- Scores performance quality
- Tracks patient progress during exercise sessions

## Features

### For General Practitioners (GPs)
- 👥 View all patients in their practice
- 📋 Assign customized exercises to patients
- ⚙️ Set exercise parameters (frequency, repetitions, sets, duration)
- 📝 Add personalized notes and instructions
- 📊 Track patient progress and adherence
- ✏️ Manage and update exercise assignments

### For Patients
- 📱 View assigned exercises from their GP
- 📖 See detailed exercise instructions
- ✅ Mark exercises as complete
- 📈 Track exercise history and statistics
- 💬 Access personalized notes from their GP
- 🎥 Perform exercises with real-time AI feedback (via webcam demo)

### Exercise Detection Capabilities
- **Real-time pose detection** using MediaPipe Pose
- **Accurate angle measurement** for joint positions
- **Instant feedback** with quality scoring (0-100)
- **Automatic repetition counting**
- **Session management and summaries**
- **Customizable parameters** (target angles, tolerance levels)
- **Support for webcam and video file analysis**

## Supported Exercises

The system supports six rehabilitation exercises:

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

## How to Run the Complete System

### Step 1: Start the Web Application

```bash
npm start
```

The server will start on port 3000. Open http://localhost:3000 in your browser.

### Step 2: Login

**Demo users are pre-loaded:**

**GPs:**
- Dr. Sarah Smith (dr.smith@hospital.com)
- Dr. Michael Jones (dr.jones@hospital.com)

**Patients:**
- John Doe (john.doe@email.com)
- Jane Wilson (jane.wilson@email.com)
- Bob Brown (bob.brown@email.com)

Click on any user to login (password: password123 for all demo users).

### Step 3: Use the Application

**As a GP:**
1. Click on a GP user to login
2. View your patients on the dashboard
3. Select a patient and exercise from the dropdowns
4. Set exercise parameters (frequency, reps, sets)
5. Add any special instructions in the notes field
6. Click "Assign Exercise"

**As a Patient:**
1. Click on a patient user to login
2. View your assigned exercises
3. Read the instructions provided
4. Mark exercises as complete after finishing them
5. For real-time tracking, use the exercise detection system (see below)

### Step 4: Use Exercise Detection (Optional)

For patients who want real-time feedback while performing exercises:

```bash
python examples/webcam_exercise_demo.py
```

**Controls:**
- `q` - Quit
- `s` - Switch exercise
- `x` - Reset session
- `l/r` - Switch to left/right side

## Testing

### Test the Web Application
```bash
npm test
```

### Test the Exercise Detection System
```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

## Project Structure

```
Axonsoton/
├── src/                          # Node.js backend
│   ├── app.js                    # Main Express application
│   ├── routes/                   # API endpoints
│   ├── controllers/              # Business logic
│   ├── models/                   # Data models
│   ├── middleware/               # Authentication
│   └── data/                     # In-memory data store
├── public/                       # Frontend files
│   ├── index.html                # Single-page application
│   ├── css/styles.css            # Styling
│   └── js/app.js                 # Frontend JavaScript
├── rehab_exercise_detection/    # Python exercise detection
│   ├── pose_detector.py          # MediaPipe integration
│   ├── angle_calculator.py       # Angle calculations
│   ├── exercises.py              # Exercise definitions
│   └── exercise_evaluator.py    # Main evaluation logic
├── examples/                     # Python examples
│   ├── webcam_exercise_demo.py   # Webcam demo
│   └── video_analysis.py         # Video analysis
├── tests/                        # Test files
├── SETUP.md                      # Detailed setup guide
├── package.json                  # Node.js dependencies
└── requirements.txt              # Python dependencies
```

## Documentation

- **[SETUP.md](SETUP.md)** - Complete installation and setup guide
- **[Project Documentation](https://docs.google.com/document/d/1nP6FtXBxIDLaF_Th2AUVDnthiqoOZYtdLUcuB1-zIUk/edit?usp=sharing)** - Detailed project documentation
- **[MediaPipe Pose](https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker)** - MediaPipe documentation

## Technology Stack

**Backend:**
- Node.js with Express
- In-memory data storage (ready for database integration)

**Frontend:**
- Vanilla JavaScript
- HTML5 & CSS3
- Chart.js for visualizations

**Exercise Detection:**
- Python 3.12
- MediaPipe Pose
- OpenCV for video processing
- NumPy for calculations

## License

MIT License
