"""
Feedback Module

Provides feedback generation for exercise evaluation.
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional


class FeedbackLevel(Enum):
    """Severity levels for exercise feedback."""
    EXCELLENT = "excellent"
    GOOD = "good"
    NEEDS_IMPROVEMENT = "needs_improvement"
    INCORRECT = "incorrect"
    ERROR = "error"


@dataclass
class ExerciseFeedback:
    """
    Contains feedback about an exercise repetition or hold.
    
    Attributes:
        is_correct: Whether the exercise is being performed correctly
        level: Overall quality level of the exercise performance
        score: Numerical score (0-100)
        current_angle: Current measured angle
        target_angle: Target angle for the exercise
        angle_difference: Difference from target angle
        messages: List of feedback messages
        corrections: List of suggested corrections
        encouragements: List of encouraging messages
    """
    is_correct: bool
    level: FeedbackLevel
    score: float
    current_angle: Optional[float] = None
    target_angle: Optional[float] = None
    angle_difference: Optional[float] = None
    messages: List[str] = field(default_factory=list)
    corrections: List[str] = field(default_factory=list)
    encouragements: List[str] = field(default_factory=list)
    
    def get_primary_message(self) -> str:
        """Get the most important feedback message."""
        if self.messages:
            return self.messages[0]
        return self._get_default_message()
    
    def _get_default_message(self) -> str:
        """Get a default message based on the feedback level."""
        messages = {
            FeedbackLevel.EXCELLENT: "Excellent form! Keep it up!",
            FeedbackLevel.GOOD: "Good job! Minor adjustments needed.",
            FeedbackLevel.NEEDS_IMPROVEMENT: "Keep trying! Focus on the corrections.",
            FeedbackLevel.INCORRECT: "Please adjust your position.",
            FeedbackLevel.ERROR: "Cannot evaluate - ensure you're visible."
        }
        return messages.get(self.level, "Continue with the exercise.")
    
    def get_all_feedback(self) -> str:
        """Get all feedback as a formatted string."""
        parts = []
        
        if self.messages:
            parts.append("Feedback:")
            parts.extend([f"  - {msg}" for msg in self.messages])
        
        if self.corrections:
            parts.append("Corrections needed:")
            parts.extend([f"  - {corr}" for corr in self.corrections])
        
        if self.encouragements:
            parts.append("Encouragement:")
            parts.extend([f"  - {enc}" for enc in self.encouragements])
        
        if self.current_angle is not None:
            parts.append(f"Current angle: {self.current_angle:.1f}°")
        
        if self.target_angle is not None:
            parts.append(f"Target angle: {self.target_angle:.1f}°")
        
        return "\n".join(parts)
    
    def to_dict(self) -> dict:
        """Convert feedback to dictionary format."""
        return {
            "is_correct": self.is_correct,
            "level": self.level.value,
            "score": self.score,
            "current_angle": self.current_angle,
            "target_angle": self.target_angle,
            "angle_difference": self.angle_difference,
            "messages": self.messages,
            "corrections": self.corrections,
            "encouragements": self.encouragements
        }


class FeedbackGenerator:
    """Generates contextual feedback for exercises."""
    
    # Correction messages for different joints and issues
    CORRECTIONS = {
        "shoulder_low": [
            "Raise your arm higher",
            "Try to lift your arm towards the target position"
        ],
        "shoulder_high": [
            "Lower your arm slightly",
            "Don't overextend - stay within comfortable range"
        ],
        "elbow_bent": [
            "Try to keep your elbow straighter",
            "Extend your arm more fully"
        ],
        "elbow_too_straight": [
            "Maintain a slight bend in your elbow",
            "Don't lock your elbow joint"
        ],
        "posture": [
            "Keep your back straight",
            "Maintain good posture throughout the movement"
        ],
        "speed": [
            "Move slowly and controlled",
            "Don't rush the movement"
        ],
        "range_insufficient": [
            "Try to increase your range of motion gradually",
            "Reach a little further if comfortable"
        ]
    }
    
    ENCOURAGEMENTS = {
        FeedbackLevel.EXCELLENT: [
            "Perfect! You're doing great!",
            "Excellent form! Keep it up!",
            "Outstanding! Maintain this quality!"
        ],
        FeedbackLevel.GOOD: [
            "Good job! Almost there!",
            "Nice work! Small improvement needed.",
            "You're doing well! Stay focused."
        ],
        FeedbackLevel.NEEDS_IMPROVEMENT: [
            "Keep trying! You're making progress.",
            "Don't give up! Focus on the corrections.",
            "Every repetition helps! Stay with it."
        ],
        FeedbackLevel.INCORRECT: [
            "Let's adjust and try again.",
            "Take a moment to reset your position.",
            "Remember to move slowly and deliberately."
        ]
    }
    
    @classmethod
    def generate_angle_feedback(
        cls,
        current_angle: float,
        target_angle: float,
        tolerance: float = 10.0,
        exercise_name: str = "exercise"
    ) -> ExerciseFeedback:
        """
        Generate feedback based on angle comparison.
        
        Args:
            current_angle: The current measured angle
            target_angle: The target angle to achieve
            tolerance: Acceptable deviation from target (degrees)
            exercise_name: Name of the exercise for context
            
        Returns:
            ExerciseFeedback object with detailed feedback
        """
        difference = current_angle - target_angle
        abs_difference = abs(difference)
        
        # Determine feedback level based on deviation
        if abs_difference <= tolerance * 0.3:
            level = FeedbackLevel.EXCELLENT
            score = 100 - (abs_difference / tolerance) * 10
            is_correct = True
        elif abs_difference <= tolerance * 0.6:
            level = FeedbackLevel.GOOD
            score = 80 - (abs_difference / tolerance) * 20
            is_correct = True
        elif abs_difference <= tolerance:
            level = FeedbackLevel.NEEDS_IMPROVEMENT
            score = 60 - (abs_difference / tolerance) * 10
            is_correct = True
        elif abs_difference <= tolerance * 2:
            level = FeedbackLevel.NEEDS_IMPROVEMENT
            score = 40 - (abs_difference / tolerance) * 10
            is_correct = False
        else:
            level = FeedbackLevel.INCORRECT
            score = max(0, 20 - (abs_difference / tolerance) * 5)
            is_correct = False
        
        score = max(0, min(100, score))
        
        # Generate messages
        messages = []
        corrections = []
        
        if level == FeedbackLevel.EXCELLENT:
            messages.append(f"Perfect {exercise_name} position!")
        elif level == FeedbackLevel.GOOD:
            messages.append(f"Good {exercise_name} - minor adjustment needed.")
            if difference > 0:
                corrections.append(f"Decrease angle by about {abs_difference:.0f}°")
            else:
                corrections.append(f"Increase angle by about {abs_difference:.0f}°")
        else:
            messages.append(f"Adjust your {exercise_name} position.")
            if difference > 0:
                corrections.append(f"Lower your position (currently {abs_difference:.0f}° too high)")
            else:
                corrections.append(f"Raise your position (currently {abs_difference:.0f}° too low)")
        
        # Get encouragement
        encouragements = []
        if level in cls.ENCOURAGEMENTS:
            import random
            encouragements.append(random.choice(cls.ENCOURAGEMENTS[level]))
        
        return ExerciseFeedback(
            is_correct=is_correct,
            level=level,
            score=score,
            current_angle=current_angle,
            target_angle=target_angle,
            angle_difference=difference,
            messages=messages,
            corrections=corrections,
            encouragements=encouragements
        )
    
    @classmethod
    def generate_range_of_motion_feedback(
        cls,
        current_angle: float,
        min_angle: float,
        max_angle: float,
        exercise_name: str = "exercise"
    ) -> ExerciseFeedback:
        """
        Generate feedback for exercises with a target range of motion.
        
        Args:
            current_angle: The current measured angle
            min_angle: Minimum acceptable angle
            max_angle: Maximum acceptable angle
            exercise_name: Name of the exercise
            
        Returns:
            ExerciseFeedback object
        """
        target_mid = (min_angle + max_angle) / 2
        range_size = max_angle - min_angle
        
        if min_angle <= current_angle <= max_angle:
            # Within range
            distance_from_mid = abs(current_angle - target_mid)
            normalized_distance = distance_from_mid / (range_size / 2)
            
            if normalized_distance <= 0.3:
                level = FeedbackLevel.EXCELLENT
                score = 95 - normalized_distance * 15
            elif normalized_distance <= 0.7:
                level = FeedbackLevel.GOOD
                score = 80 - normalized_distance * 20
            else:
                level = FeedbackLevel.GOOD
                score = 70 - normalized_distance * 10
            
            is_correct = True
            messages = [f"Good {exercise_name} - within target range!"]
            corrections = []
        else:
            # Outside range
            if current_angle < min_angle:
                deviation = min_angle - current_angle
                corrections = [f"Increase angle by {deviation:.0f}° to reach minimum"]
            else:
                deviation = current_angle - max_angle
                corrections = [f"Decrease angle by {deviation:.0f}° to stay in range"]
            
            if deviation <= range_size * 0.2:
                level = FeedbackLevel.NEEDS_IMPROVEMENT
                score = 50 - deviation
            else:
                level = FeedbackLevel.INCORRECT
                score = max(0, 30 - deviation)
            
            is_correct = False
            messages = [f"Adjust {exercise_name} to stay within range"]
        
        score = max(0, min(100, score))
        
        encouragements = []
        if level in cls.ENCOURAGEMENTS:
            import random
            encouragements.append(random.choice(cls.ENCOURAGEMENTS[level]))
        
        return ExerciseFeedback(
            is_correct=is_correct,
            level=level,
            score=score,
            current_angle=current_angle,
            target_angle=target_mid,
            angle_difference=current_angle - target_mid,
            messages=messages,
            corrections=corrections,
            encouragements=encouragements
        )
