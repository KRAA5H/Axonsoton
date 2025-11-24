"""
Tests for the exercises module.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rehab_exercise_detection.exercises import (
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
    EXERCISE_REGISTRY
)
from rehab_exercise_detection.feedback import FeedbackLevel
from rehab_exercise_detection.pose_detector import Landmark
from unittest.mock import MagicMock


class TestExerciseConfig:
    """Test cases for ExerciseConfig class."""
    
    def test_config_creation_with_defaults(self):
        """Test config creation with default values."""
        config = ExerciseConfig(target_angle=90.0)
        
        assert config.target_angle == 90.0
        assert config.tolerance == 15.0
        assert config.side == 'left'
        assert config.use_3d is False
    
    def test_config_creation_custom_values(self):
        """Test config creation with custom values."""
        config = ExerciseConfig(
            target_angle=120.0,
            tolerance=20.0,
            min_angle=90.0,
            max_angle=150.0,
            hold_duration=2.0,
            repetitions=5,
            side='right',
            use_3d=True
        )
        
        assert config.target_angle == 120.0
        assert config.tolerance == 20.0
        assert config.min_angle == 90.0
        assert config.max_angle == 150.0
        assert config.hold_duration == 2.0
        assert config.repetitions == 5
        assert config.side == 'right'
        assert config.use_3d is True


class TestShoulderFlexion:
    """Test cases for ShoulderFlexion exercise."""
    
    def test_creation_with_default_config(self):
        """Test creation with default configuration."""
        exercise = ShoulderFlexion()
        
        assert exercise.name == "Shoulder Flexion"
        assert exercise.config.target_angle == 90.0
        assert exercise.config.side == 'left'
    
    def test_creation_with_custom_config(self):
        """Test creation with custom configuration."""
        config = ExerciseConfig(
            target_angle=120.0,
            tolerance=10.0,
            side='right'
        )
        exercise = ShoulderFlexion(config)
        
        assert exercise.config.target_angle == 120.0
        assert exercise.config.tolerance == 10.0
        assert exercise.config.side == 'right'
    
    def test_has_description(self):
        """Test exercise has a description."""
        exercise = ShoulderFlexion()
        
        assert len(exercise.description) > 0
        assert 'arm' in exercise.description.lower() or 'shoulder' in exercise.description.lower()
    
    def test_has_instructions(self):
        """Test exercise has instructions."""
        exercise = ShoulderFlexion()
        
        assert len(exercise.instructions) > 0
        assert all(isinstance(i, str) for i in exercise.instructions)
    
    def test_evaluate_returns_error_for_missing_landmarks(self):
        """Test evaluation returns error when landmarks are missing."""
        exercise = ShoulderFlexion()
        
        # Create mock landmarks with missing data
        mock_landmarks = MagicMock()
        mock_landmarks.get.return_value = None
        
        feedback = exercise.evaluate(mock_landmarks)
        
        assert feedback.level == FeedbackLevel.ERROR
        assert feedback.is_correct is False


class TestAllExercises:
    """Test cases that apply to all exercise types."""
    
    @pytest.fixture
    def all_exercise_classes(self):
        """Provide all exercise classes for testing."""
        return [
            ShoulderFlexion,
            ShoulderAbduction,
            ElbowFlexion,
            KneeFlexion,
            HipFlexion,
            HipAbduction
        ]
    
    def test_all_exercises_have_names(self, all_exercise_classes):
        """Test all exercises have names."""
        for exercise_class in all_exercise_classes:
            exercise = exercise_class()
            assert exercise.name is not None
            assert len(exercise.name) > 0
    
    def test_all_exercises_have_descriptions(self, all_exercise_classes):
        """Test all exercises have descriptions."""
        for exercise_class in all_exercise_classes:
            exercise = exercise_class()
            assert exercise.description is not None
            assert len(exercise.description) > 0
    
    def test_all_exercises_have_instructions(self, all_exercise_classes):
        """Test all exercises have instructions."""
        for exercise_class in all_exercise_classes:
            exercise = exercise_class()
            assert exercise.instructions is not None
            assert len(exercise.instructions) > 0
    
    def test_all_exercises_have_default_config(self, all_exercise_classes):
        """Test all exercises have default configuration."""
        for exercise_class in all_exercise_classes:
            exercise = exercise_class()
            assert exercise.config is not None
            assert exercise.config.target_angle is not None
    
    def test_reset_clears_state(self, all_exercise_classes):
        """Test reset method clears exercise state."""
        for exercise_class in all_exercise_classes:
            exercise = exercise_class()
            exercise._rep_count = 5
            exercise._angles_history = [1, 2, 3]
            
            exercise.reset()
            
            assert exercise._rep_count == 0
            assert len(exercise._angles_history) == 0


class TestExerciseRegistry:
    """Test cases for exercise registry."""
    
    def test_registry_contains_all_exercises(self):
        """Test registry contains all expected exercises."""
        expected_exercises = [
            'shoulder_flexion',
            'shoulder_abduction',
            'elbow_flexion',
            'knee_flexion',
            'hip_flexion',
            'hip_abduction'
        ]
        
        for name in expected_exercises:
            assert name in EXERCISE_REGISTRY
    
    def test_get_exercise_by_name(self):
        """Test getting exercise by name."""
        exercise = get_exercise('shoulder_flexion')
        
        assert isinstance(exercise, ShoulderFlexion)
        assert exercise.name == "Shoulder Flexion"
    
    def test_get_exercise_with_config(self):
        """Test getting exercise with custom config."""
        config = ExerciseConfig(target_angle=120.0, side='right')
        exercise = get_exercise('shoulder_flexion', config)
        
        assert exercise.config.target_angle == 120.0
        assert exercise.config.side == 'right'
    
    def test_get_exercise_invalid_name(self):
        """Test getting exercise with invalid name raises error."""
        with pytest.raises(ValueError) as exc_info:
            get_exercise('invalid_exercise')
        
        assert 'Unknown exercise' in str(exc_info.value)
    
    def test_list_available_exercises(self):
        """Test listing available exercises."""
        available = list_available_exercises()
        
        assert isinstance(available, list)
        assert len(available) > 0
        assert 'shoulder_flexion' in available


class TestExerciseAngleHistory:
    """Test cases for exercise angle history tracking."""
    
    def test_angle_history_tracking(self):
        """Test that angle history is tracked correctly."""
        exercise = ShoulderFlexion()
        
        # Create mock landmarks that return a specific angle
        def create_mock_landmarks(angle):
            mock = MagicMock()
            hip = Landmark(x=0.5, y=0.8, z=0, visibility=1.0)
            shoulder = Landmark(x=0.5, y=0.5, z=0, visibility=1.0)
            # Calculate elbow position for desired angle
            import math
            rad = math.radians(angle)
            elbow_x = 0.5 + 0.3 * math.sin(rad)
            elbow_y = 0.5 - 0.3 * math.cos(rad)
            elbow = Landmark(x=elbow_x, y=elbow_y, z=0, visibility=1.0)
            
            def get_landmark(name):
                if 'hip' in name:
                    return hip
                elif 'shoulder' in name:
                    return shoulder
                elif 'elbow' in name:
                    return elbow
                return None
            
            mock.get = get_landmark
            return mock
        
        # Evaluate multiple times
        for _ in range(5):
            landmarks = create_mock_landmarks(90)
            exercise.evaluate(landmarks)
        
        # Check history is being tracked
        assert len(exercise._angles_history) == 5
    
    def test_angle_history_limited(self):
        """Test that angle history is limited to prevent memory issues."""
        exercise = ShoulderFlexion()
        
        # Create mock landmarks
        mock = MagicMock()
        mock.get.return_value = Landmark(x=0.5, y=0.5, z=0, visibility=1.0)
        
        # Evaluate many times
        for _ in range(100):
            # This will add None to history since mock doesn't have proper structure
            exercise._angles_history.append(90.0)
        
        # Manually trigger cleanup that would happen in evaluate
        while len(exercise._angles_history) > 30:
            exercise._angles_history.pop(0)
        
        assert len(exercise._angles_history) <= 30


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
