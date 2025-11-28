"""
Exercise Evaluator Module

High-level interface for evaluating rehabilitation exercises.
"""

import cv2
import time
import numpy as np
from typing import Optional, Dict, Any, List, Callable, Tuple
from dataclasses import dataclass
from enum import Enum

from .pose_detector import PoseDetector, PoseLandmarks
from .exercises import Exercise, ExerciseConfig, get_exercise, list_available_exercises
from .feedback import ExerciseFeedback, FeedbackLevel


class ExerciseState(Enum):
    """Current state of exercise execution."""
    IDLE = "idle"
    STARTING = "starting"
    IN_PROGRESS = "in_progress"
    HOLDING = "holding"
    COMPLETED = "completed"
    RESTING = "resting"


@dataclass
class ExerciseSession:
    """Tracks the progress of an exercise session."""
    exercise_name: str
    target_reps: int
    completed_reps: int = 0
    successful_reps: int = 0
    total_score: float = 0.0
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    feedback_history: List[ExerciseFeedback] = None
    
    def __post_init__(self):
        if self.feedback_history is None:
            self.feedback_history = []
    
    @property
    def average_score(self) -> float:
        """Calculate average score across all feedback."""
        if not self.feedback_history:
            return 0.0
        return sum(f.score for f in self.feedback_history) / len(self.feedback_history)
    
    @property
    def duration(self) -> Optional[float]:
        """Get session duration in seconds."""
        if self.start_time is None:
            return None
        end = self.end_time or time.time()
        return end - self.start_time
    
    @property
    def is_complete(self) -> bool:
        """Check if target repetitions are completed."""
        return self.completed_reps >= self.target_reps
    
    def to_dict(self) -> dict:
        """Convert session to dictionary."""
        return {
            "exercise_name": self.exercise_name,
            "target_reps": self.target_reps,
            "completed_reps": self.completed_reps,
            "successful_reps": self.successful_reps,
            "average_score": self.average_score,
            "duration": self.duration,
            "is_complete": self.is_complete
        }


class RepetitionTracker:
    """Tracks exercise repetitions based on angle changes."""
    
    def __init__(
        self,
        threshold_angle: float = 30.0,
        min_hold_time: float = 0.5,
        smoothing_window: int = 5
    ):
        """
        Initialize the repetition tracker.
        
        Args:
            threshold_angle: Minimum angle change to count as movement
            min_hold_time: Minimum time to hold position (seconds)
            smoothing_window: Number of frames for smoothing
        """
        self.threshold_angle = threshold_angle
        self.min_hold_time = min_hold_time
        self.smoothing_window = smoothing_window
        
        self._angle_history: List[float] = []
        self._is_in_rep = False
        self._rep_start_time: Optional[float] = None
        self._peak_angle = 0.0
        self._baseline_angle = 0.0
        self._rep_count = 0
    
    def update(self, angle: float) -> Tuple[bool, bool]:
        """
        Update tracker with new angle reading.
        
        Args:
            angle: Current angle measurement
            
        Returns:
            Tuple of (rep_started, rep_completed)
        """
        self._angle_history.append(angle)
        if len(self._angle_history) > self.smoothing_window:
            self._angle_history.pop(0)
        
        # Get smoothed angle
        smoothed_angle = sum(self._angle_history) / len(self._angle_history)
        
        rep_started = False
        rep_completed = False
        
        if not self._is_in_rep:
            # Check if starting a rep
            if smoothed_angle > self._baseline_angle + self.threshold_angle:
                self._is_in_rep = True
                self._rep_start_time = time.time()
                self._peak_angle = smoothed_angle
                rep_started = True
        else:
            # Track peak
            if smoothed_angle > self._peak_angle:
                self._peak_angle = smoothed_angle
            
            # Check if rep is complete (returned to baseline)
            if smoothed_angle < self._baseline_angle + self.threshold_angle * 0.5:
                # Check hold time
                if (self._rep_start_time and 
                    time.time() - self._rep_start_time >= self.min_hold_time):
                    self._rep_count += 1
                    rep_completed = True
                
                self._is_in_rep = False
                self._rep_start_time = None
                self._baseline_angle = smoothed_angle
        
        return rep_started, rep_completed
    
    def reset(self):
        """Reset the tracker."""
        self._angle_history.clear()
        self._is_in_rep = False
        self._rep_start_time = None
        self._peak_angle = 0.0
        self._baseline_angle = 0.0
        self._rep_count = 0
    
    @property
    def rep_count(self) -> int:
        """Get current repetition count."""
        return self._rep_count
    
    @property
    def is_in_rep(self) -> bool:
        """Check if currently in a repetition."""
        return self._is_in_rep


class ExerciseEvaluator:
    """
    High-level class for evaluating rehabilitation exercises.
    
    This class combines pose detection, exercise evaluation, and
    repetition tracking to provide comprehensive exercise feedback.
    """
    
    def __init__(
        self,
        exercise: Optional[Exercise] = None,
        pose_detector: Optional[PoseDetector] = None,
        target_reps: int = 10
    ):
        """
        Initialize the exercise evaluator.
        
        Args:
            exercise: The exercise to evaluate
            pose_detector: PoseDetector instance (created if not provided)
            target_reps: Target number of repetitions
        """
        self.exercise = exercise
        self.pose_detector = pose_detector or PoseDetector()
        self.target_reps = target_reps
        
        self._rep_tracker = RepetitionTracker()
        self._session: Optional[ExerciseSession] = None
        self._state = ExerciseState.IDLE
        self._last_feedback: Optional[ExerciseFeedback] = None
        self._callbacks: Dict[str, List[Callable]] = {
            'rep_started': [],
            'rep_completed': [],
            'session_started': [],
            'session_completed': [],
            'feedback_generated': []
        }
    
    def set_exercise(self, exercise: Exercise):
        """Set the exercise to evaluate."""
        self.exercise = exercise
        self.reset()
    
    def set_exercise_by_name(
        self,
        name: str,
        config: Optional[ExerciseConfig] = None
    ):
        """
        Set exercise by name.
        
        Args:
            name: Exercise name (e.g., 'shoulder_flexion')
            config: Optional exercise configuration
        """
        self.exercise = get_exercise(name, config)
        self.reset()
    
    def start_session(self, target_reps: Optional[int] = None):
        """
        Start a new exercise session.
        
        Args:
            target_reps: Override target repetitions for this session
        """
        if self.exercise is None:
            raise ValueError("No exercise set. Call set_exercise() first.")
        
        reps = target_reps or self.target_reps
        self._session = ExerciseSession(
            exercise_name=self.exercise.name,
            target_reps=reps
        )
        self._session.start_time = time.time()
        self._state = ExerciseState.STARTING
        self._rep_tracker.reset()
        self.exercise.reset()
        
        self._trigger_callbacks('session_started', self._session)
    
    def evaluate_frame(self, frame: np.ndarray) -> ExerciseFeedback:
        """
        Evaluate a single video frame.
        
        Args:
            frame: BGR image from video/camera
            
        Returns:
            ExerciseFeedback with evaluation results
        """
        if self.exercise is None:
            return ExerciseFeedback(
                is_correct=False,
                level=FeedbackLevel.ERROR,
                score=0,
                messages=["No exercise configured."]
            )
        
        # Detect pose
        landmarks = self.pose_detector.detect(frame)
        
        if landmarks is None:
            return ExerciseFeedback(
                is_correct=False,
                level=FeedbackLevel.ERROR,
                score=0,
                messages=["No person detected in frame."],
                corrections=["Please ensure you're visible to the camera."]
            )
        
        # Evaluate exercise
        feedback = self.exercise.evaluate(landmarks)
        self._last_feedback = feedback
        
        # Update session tracking
        if self._session:
            self._session.feedback_history.append(feedback)
            
            # Track repetitions if we have an angle
            if feedback.current_angle is not None:
                rep_started, rep_completed = self._rep_tracker.update(
                    feedback.current_angle
                )
                
                if rep_started:
                    self._state = ExerciseState.IN_PROGRESS
                    self._trigger_callbacks('rep_started', self._rep_tracker.rep_count)
                
                if rep_completed:
                    self._session.completed_reps += 1
                    if feedback.is_correct:
                        self._session.successful_reps += 1
                    
                    self._trigger_callbacks('rep_completed', {
                        'rep_number': self._session.completed_reps,
                        'was_successful': feedback.is_correct,
                        'feedback': feedback
                    })
                    
                    # Check if session is complete
                    if self._session.is_complete:
                        self._complete_session()
        
        self._trigger_callbacks('feedback_generated', feedback)
        return feedback
    
    def evaluate_landmarks(
        self,
        landmarks: PoseLandmarks
    ) -> ExerciseFeedback:
        """
        Evaluate pre-detected pose landmarks.
        
        Args:
            landmarks: PoseLandmarks from pose detection
            
        Returns:
            ExerciseFeedback with evaluation results
        """
        if self.exercise is None:
            return ExerciseFeedback(
                is_correct=False,
                level=FeedbackLevel.ERROR,
                score=0,
                messages=["No exercise configured."]
            )
        
        feedback = self.exercise.evaluate(landmarks)
        self._last_feedback = feedback
        
        if self._session:
            self._session.feedback_history.append(feedback)
        
        return feedback
    
    def draw_feedback(
        self,
        frame: np.ndarray,
        feedback: Optional[ExerciseFeedback] = None,
        show_angle: bool = True,
        show_score: bool = True,
        show_reps: bool = True
    ) -> np.ndarray:
        """
        Draw feedback overlay on frame.
        
        Args:
            frame: BGR image to draw on
            feedback: Feedback to display (uses last if None)
            show_angle: Display current angle
            show_score: Display score
            show_reps: Display repetition count
            
        Returns:
            Annotated frame
        """
        annotated = self.pose_detector.draw_landmarks(frame)
        feedback = feedback or self._last_feedback
        
        if feedback is None:
            return annotated
        
        # Color based on feedback level
        colors = {
            FeedbackLevel.EXCELLENT: (0, 255, 0),    # Green
            FeedbackLevel.GOOD: (0, 200, 100),       # Light green
            FeedbackLevel.NEEDS_IMPROVEMENT: (0, 165, 255),  # Orange
            FeedbackLevel.INCORRECT: (0, 0, 255),    # Red
            FeedbackLevel.ERROR: (128, 128, 128)     # Gray
        }
        color = colors.get(feedback.level, (255, 255, 255))
        
        y_offset = 30
        
        # Draw exercise name
        if self.exercise:
            cv2.putText(
                annotated, self.exercise.name,
                (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX,
                0.8, (255, 255, 255), 2
            )
            y_offset += 35
        
        # Draw angle
        if show_angle and feedback.current_angle is not None:
            angle_text = f"Angle: {feedback.current_angle:.1f}"
            if feedback.target_angle is not None:
                angle_text += f" / {feedback.target_angle:.1f}"
            cv2.putText(
                annotated, angle_text,
                (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX,
                0.7, color, 2
            )
            y_offset += 30
        
        # Draw score
        if show_score:
            cv2.putText(
                annotated, f"Score: {feedback.score:.0f}%",
                (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX,
                0.7, color, 2
            )
            y_offset += 30
        
        # Draw reps
        if show_reps and self._session:
            cv2.putText(
                annotated,
                f"Reps: {self._session.completed_reps}/{self._session.target_reps}",
                (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (255, 255, 255), 2
            )
            y_offset += 30
        
        # Draw feedback message
        message = feedback.get_primary_message()
        cv2.putText(
            annotated, message,
            (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX,
            0.6, color, 2
        )
        
        # Draw status indicator
        status_color = (0, 255, 0) if feedback.is_correct else (0, 0, 255)
        cv2.circle(
            annotated,
            (frame.shape[1] - 30, 30),
            20, status_color, -1
        )
        
        return annotated
    
    def get_session_summary(self) -> Optional[dict]:
        """Get summary of current/completed session."""
        if self._session:
            return self._session.to_dict()
        return None
    
    def register_callback(self, event: str, callback: Callable):
        """
        Register a callback for exercise events.
        
        Events:
            - 'rep_started': Called when a repetition starts
            - 'rep_completed': Called when a repetition completes
            - 'session_started': Called when session starts
            - 'session_completed': Called when session completes
            - 'feedback_generated': Called when feedback is generated
        """
        if event in self._callbacks:
            self._callbacks[event].append(callback)
    
    def _trigger_callbacks(self, event: str, data: Any = None):
        """Trigger all callbacks for an event."""
        for callback in self._callbacks.get(event, []):
            try:
                callback(data)
            except Exception as e:
                print(f"Callback error for {event}: {e}")
    
    def _complete_session(self):
        """Complete the current session."""
        if self._session:
            self._session.end_time = time.time()
            self._state = ExerciseState.COMPLETED
            self._trigger_callbacks('session_completed', self._session)
    
    def reset(self):
        """Reset the evaluator state."""
        self._rep_tracker.reset()
        self._session = None
        self._state = ExerciseState.IDLE
        self._last_feedback = None
        if self.exercise:
            self.exercise.reset()
    
    @property
    def state(self) -> ExerciseState:
        """Get current exercise state."""
        return self._state
    
    @property
    def last_feedback(self) -> Optional[ExerciseFeedback]:
        """Get the last generated feedback."""
        return self._last_feedback
    
    @staticmethod
    def available_exercises() -> List[str]:
        """List all available exercises."""
        return list_available_exercises()
    
    def close(self):
        """Release resources."""
        self.pose_detector.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
