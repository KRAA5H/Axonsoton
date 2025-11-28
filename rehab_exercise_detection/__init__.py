"""
Rehab Exercise Detection System

A system that uses MediaPipe to detect whether a patient is correctly
performing rehabilitation exercises used to cure/improve gross motor disorders.
"""

from .pose_detector import PoseDetector
from .angle_calculator import AngleCalculator
from .exercise_evaluator import ExerciseEvaluator
from .exercises import (
    Exercise,
    ExerciseConfig,
    ShoulderFlexion,
    ShoulderAbduction,
    ElbowFlexion,
    KneeFlexion,
    HipFlexion,
    HipAbduction,
    get_exercise,
    list_available_exercises,
)
from .feedback import ExerciseFeedback, FeedbackLevel

__version__ = "1.0.0"
__all__ = [
    "PoseDetector",
    "AngleCalculator",
    "ExerciseEvaluator",
    "Exercise",
    "ExerciseConfig",
    "ShoulderFlexion",
    "ShoulderAbduction",
    "ElbowFlexion",
    "KneeFlexion",
    "HipFlexion",
    "HipAbduction",
    "get_exercise",
    "list_available_exercises",
    "ExerciseFeedback",
    "FeedbackLevel",
]
