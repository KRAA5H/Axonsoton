"""
Exercises Module

Contains implementations of specific rehabilitation exercises.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Dict, Any, List
from .pose_detector import PoseLandmarks
from .angle_calculator import AngleCalculator
from .feedback import ExerciseFeedback, FeedbackGenerator, FeedbackLevel


@dataclass
class ExerciseConfig:
    """Configuration parameters for an exercise."""
    target_angle: float
    tolerance: float = 15.0  # Degrees of acceptable deviation
    min_angle: Optional[float] = None  # For range-based exercises
    max_angle: Optional[float] = None  # For range-based exercises
    hold_duration: float = 0.0  # Required hold time in seconds
    repetitions: int = 1  # Target number of repetitions
    side: str = 'left'  # Which side of the body
    use_3d: bool = False  # Whether to use 3D angle calculation


class Exercise(ABC):
    """
    Abstract base class for rehabilitation exercises.
    
    This class defines the interface for all exercise implementations.
    Subclasses must implement the evaluate() method to provide
    exercise-specific evaluation logic.
    """
    
    def __init__(self, config: Optional[ExerciseConfig] = None):
        """
        Initialize the exercise.
        
        Args:
            config: Exercise configuration parameters
        """
        self.config = config or self._get_default_config()
        self.name = self._get_exercise_name()
        self.description = self._get_exercise_description()
        self.instructions = self._get_exercise_instructions()
        
        # Tracking state
        self._rep_count = 0
        self._is_in_position = False
        self._hold_start_time: Optional[float] = None
        self._angles_history: List[float] = []
    
    @abstractmethod
    def _get_exercise_name(self) -> str:
        """Return the name of the exercise."""
        pass
    
    @abstractmethod
    def _get_exercise_description(self) -> str:
        """Return a description of the exercise."""
        pass
    
    @abstractmethod
    def _get_exercise_instructions(self) -> List[str]:
        """Return step-by-step instructions for the exercise."""
        pass
    
    @abstractmethod
    def _get_default_config(self) -> ExerciseConfig:
        """Return the default configuration for this exercise."""
        pass
    
    @abstractmethod
    def _calculate_angle(self, landmarks: PoseLandmarks) -> Optional[float]:
        """Calculate the primary angle for this exercise."""
        pass
    
    def evaluate(self, landmarks: PoseLandmarks) -> ExerciseFeedback:
        """
        Evaluate whether the exercise is being performed correctly.
        
        Args:
            landmarks: PoseLandmarks from pose detection
            
        Returns:
            ExerciseFeedback with evaluation results
        """
        angle = self._calculate_angle(landmarks)
        
        if angle is None:
            return ExerciseFeedback(
                is_correct=False,
                level=FeedbackLevel.ERROR,
                score=0,
                messages=["Cannot detect required body landmarks. Please ensure you're fully visible."],
                corrections=["Position yourself so the camera can see your entire body."]
            )
        
        # Track angle history
        self._angles_history.append(angle)
        if len(self._angles_history) > 30:  # Keep last 30 frames
            self._angles_history.pop(0)
        
        # Generate feedback based on configuration
        if self.config.min_angle is not None and self.config.max_angle is not None:
            feedback = FeedbackGenerator.generate_range_of_motion_feedback(
                current_angle=angle,
                min_angle=self.config.min_angle,
                max_angle=self.config.max_angle,
                exercise_name=self.name
            )
        else:
            feedback = FeedbackGenerator.generate_angle_feedback(
                current_angle=angle,
                target_angle=self.config.target_angle,
                tolerance=self.config.tolerance,
                exercise_name=self.name
            )
        
        return feedback
    
    def get_current_angle(self, landmarks: PoseLandmarks) -> Optional[float]:
        """Get the current angle without evaluating."""
        return self._calculate_angle(landmarks)
    
    def get_rep_count(self) -> int:
        """Get the current repetition count."""
        return self._rep_count
    
    def reset(self):
        """Reset the exercise tracking state."""
        self._rep_count = 0
        self._is_in_position = False
        self._hold_start_time = None
        self._angles_history.clear()
    
    def get_average_angle(self) -> Optional[float]:
        """Get the average angle from recent history."""
        if self._angles_history:
            return sum(self._angles_history) / len(self._angles_history)
        return None


class ShoulderFlexion(Exercise):
    """
    Shoulder Flexion Exercise
    
    Patient raises their arm forward and upward from the body.
    This exercise helps improve shoulder mobility and strength.
    """
    
    def _get_exercise_name(self) -> str:
        return "Shoulder Flexion"
    
    def _get_exercise_description(self) -> str:
        return (
            "Raise your arm forward and upward, keeping your elbow straight. "
            "This exercise improves the range of motion in your shoulder joint."
        )
    
    def _get_exercise_instructions(self) -> List[str]:
        return [
            "Stand or sit with good posture, arms at your sides.",
            f"Slowly raise your {self.config.side} arm forward and up.",
            "Keep your elbow straight throughout the movement.",
            f"Aim to raise your arm to {self.config.target_angle}° from your body.",
            "Hold the position briefly, then slowly lower your arm.",
            "Repeat as directed by your therapist."
        ]
    
    def _get_default_config(self) -> ExerciseConfig:
        return ExerciseConfig(
            target_angle=90.0,  # Target 90 degrees (horizontal)
            tolerance=15.0,
            min_angle=0.0,
            max_angle=180.0,
            side='left'
        )
    
    def _calculate_angle(self, landmarks: PoseLandmarks) -> Optional[float]:
        return AngleCalculator.get_shoulder_flexion_angle(
            landmarks,
            side=self.config.side,
            use_3d=self.config.use_3d
        )


class ShoulderAbduction(Exercise):
    """
    Shoulder Abduction Exercise
    
    Patient raises their arm out to the side away from the body.
    This exercise improves lateral shoulder mobility.
    """
    
    def _get_exercise_name(self) -> str:
        return "Shoulder Abduction"
    
    def _get_exercise_description(self) -> str:
        return (
            "Raise your arm out to the side, keeping your elbow straight. "
            "This exercise improves shoulder mobility in the frontal plane."
        )
    
    def _get_exercise_instructions(self) -> List[str]:
        return [
            "Stand with good posture, arms at your sides.",
            f"Slowly raise your {self.config.side} arm out to the side.",
            "Keep your palm facing down and elbow straight.",
            f"Aim to raise your arm to {self.config.target_angle}° from your body.",
            "Hold briefly, then slowly lower.",
            "Repeat as directed."
        ]
    
    def _get_default_config(self) -> ExerciseConfig:
        return ExerciseConfig(
            target_angle=90.0,
            tolerance=15.0,
            min_angle=0.0,
            max_angle=180.0,
            side='left'
        )
    
    def _calculate_angle(self, landmarks: PoseLandmarks) -> Optional[float]:
        return AngleCalculator.get_shoulder_abduction_angle(
            landmarks,
            side=self.config.side,
            use_3d=self.config.use_3d
        )


class ElbowFlexion(Exercise):
    """
    Elbow Flexion Exercise
    
    Patient bends their elbow, bringing hand toward shoulder.
    This exercise improves elbow range of motion and bicep strength.
    """
    
    def _get_exercise_name(self) -> str:
        return "Elbow Flexion"
    
    def _get_exercise_description(self) -> str:
        return (
            "Bend your elbow, bringing your hand toward your shoulder. "
            "This exercise improves elbow mobility and forearm strength."
        )
    
    def _get_exercise_instructions(self) -> List[str]:
        return [
            "Stand or sit with your arm at your side.",
            f"Keep your {self.config.side} upper arm still.",
            "Slowly bend your elbow, bringing your hand toward your shoulder.",
            f"Aim for {self.config.target_angle}° of flexion.",
            "Hold briefly at the top, then slowly straighten.",
            "Repeat as directed."
        ]
    
    def _get_default_config(self) -> ExerciseConfig:
        return ExerciseConfig(
            target_angle=140.0,  # Near full flexion
            tolerance=15.0,
            min_angle=0.0,
            max_angle=150.0,
            side='left'
        )
    
    def _calculate_angle(self, landmarks: PoseLandmarks) -> Optional[float]:
        return AngleCalculator.get_elbow_flexion_angle(
            landmarks,
            side=self.config.side,
            use_3d=self.config.use_3d
        )


class KneeFlexion(Exercise):
    """
    Knee Flexion Exercise
    
    Patient bends their knee, bringing heel toward buttocks.
    Important for lower limb rehabilitation.
    """
    
    def _get_exercise_name(self) -> str:
        return "Knee Flexion"
    
    def _get_exercise_description(self) -> str:
        return (
            "Bend your knee, bringing your heel toward your buttocks. "
            "This exercise improves knee mobility and hamstring strength."
        )
    
    def _get_exercise_instructions(self) -> List[str]:
        return [
            "Stand holding onto a stable surface for balance.",
            f"Lift your {self.config.side} foot off the ground.",
            "Slowly bend your knee, bringing your heel toward your buttocks.",
            f"Aim for {self.config.target_angle}° of flexion.",
            "Hold briefly, then slowly lower your foot.",
            "Repeat as directed."
        ]
    
    def _get_default_config(self) -> ExerciseConfig:
        return ExerciseConfig(
            target_angle=90.0,
            tolerance=15.0,
            min_angle=0.0,
            max_angle=135.0,
            side='left'
        )
    
    def _calculate_angle(self, landmarks: PoseLandmarks) -> Optional[float]:
        return AngleCalculator.get_knee_flexion_angle(
            landmarks,
            side=self.config.side,
            use_3d=self.config.use_3d
        )


class HipFlexion(Exercise):
    """
    Hip Flexion Exercise
    
    Patient raises their thigh forward and upward.
    Important for hip mobility and core stability.
    """
    
    def _get_exercise_name(self) -> str:
        return "Hip Flexion"
    
    def _get_exercise_description(self) -> str:
        return (
            "Raise your thigh forward and upward while standing. "
            "This exercise improves hip mobility and core stability."
        )
    
    def _get_exercise_instructions(self) -> List[str]:
        return [
            "Stand with good posture, holding onto a stable surface.",
            f"Slowly raise your {self.config.side} knee forward and up.",
            "Keep your back straight - don't lean backward.",
            f"Aim to raise your thigh to {self.config.target_angle}° from vertical.",
            "Hold briefly, then slowly lower.",
            "Repeat as directed."
        ]
    
    def _get_default_config(self) -> ExerciseConfig:
        return ExerciseConfig(
            target_angle=90.0,
            tolerance=15.0,
            min_angle=0.0,
            max_angle=120.0,
            side='left'
        )
    
    def _calculate_angle(self, landmarks: PoseLandmarks) -> Optional[float]:
        return AngleCalculator.get_hip_flexion_angle(
            landmarks,
            side=self.config.side,
            use_3d=self.config.use_3d
        )


class HipAbduction(Exercise):
    """
    Hip Abduction Exercise
    
    Patient moves their leg outward away from the body's midline.
    Important for hip stability and walking.
    """
    
    def _get_exercise_name(self) -> str:
        return "Hip Abduction"
    
    def _get_exercise_description(self) -> str:
        return (
            "Move your leg outward, away from your body. "
            "This exercise improves hip stability and lateral movement."
        )
    
    def _get_exercise_instructions(self) -> List[str]:
        return [
            "Stand with good posture, holding onto a stable surface.",
            f"Keep your {self.config.side} leg straight.",
            "Slowly move your leg outward, away from your body.",
            f"Aim for {self.config.target_angle}° of abduction.",
            "Keep your toes pointing forward.",
            "Hold briefly, then slowly return to start.",
            "Repeat as directed."
        ]
    
    def _get_default_config(self) -> ExerciseConfig:
        return ExerciseConfig(
            target_angle=30.0,  # Hip abduction range is smaller
            tolerance=10.0,
            min_angle=0.0,
            max_angle=45.0,
            side='left'
        )
    
    def _calculate_angle(self, landmarks: PoseLandmarks) -> Optional[float]:
        return AngleCalculator.get_hip_abduction_angle(
            landmarks,
            side=self.config.side,
            use_3d=self.config.use_3d
        )


# Exercise registry for easy lookup
EXERCISE_REGISTRY: Dict[str, type] = {
    'shoulder_flexion': ShoulderFlexion,
    'shoulder_abduction': ShoulderAbduction,
    'elbow_flexion': ElbowFlexion,
    'knee_flexion': KneeFlexion,
    'hip_flexion': HipFlexion,
    'hip_abduction': HipAbduction,
}


def get_exercise(name: str, config: Optional[ExerciseConfig] = None) -> Exercise:
    """
    Get an exercise instance by name.
    
    Args:
        name: Name of the exercise (e.g., 'shoulder_flexion')
        config: Optional configuration for the exercise
        
    Returns:
        Exercise instance
        
    Raises:
        ValueError: If exercise name is not recognized
    """
    if name not in EXERCISE_REGISTRY:
        available = ', '.join(EXERCISE_REGISTRY.keys())
        raise ValueError(f"Unknown exercise: {name}. Available: {available}")
    
    return EXERCISE_REGISTRY[name](config)


def list_available_exercises() -> List[str]:
    """Return list of available exercise names."""
    return list(EXERCISE_REGISTRY.keys())
