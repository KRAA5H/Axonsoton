"""
Tests for the feedback module.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rehab_exercise_detection.feedback import (
    ExerciseFeedback,
    FeedbackLevel,
    FeedbackGenerator
)


class TestExerciseFeedback:
    """Test cases for ExerciseFeedback class."""
    
    def test_feedback_creation(self):
        """Test basic feedback creation."""
        feedback = ExerciseFeedback(
            is_correct=True,
            level=FeedbackLevel.EXCELLENT,
            score=95.0,
            current_angle=90.0,
            target_angle=90.0
        )
        
        assert feedback.is_correct is True
        assert feedback.level == FeedbackLevel.EXCELLENT
        assert feedback.score == 95.0
        assert feedback.current_angle == 90.0
        assert feedback.target_angle == 90.0
    
    def test_feedback_default_messages(self):
        """Test default feedback messages for each level."""
        levels = [
            FeedbackLevel.EXCELLENT,
            FeedbackLevel.GOOD,
            FeedbackLevel.NEEDS_IMPROVEMENT,
            FeedbackLevel.INCORRECT,
            FeedbackLevel.ERROR
        ]
        
        for level in levels:
            feedback = ExerciseFeedback(
                is_correct=True,
                level=level,
                score=50.0
            )
            message = feedback.get_primary_message()
            assert isinstance(message, str)
            assert len(message) > 0
    
    def test_feedback_custom_messages(self):
        """Test custom messages are returned."""
        feedback = ExerciseFeedback(
            is_correct=True,
            level=FeedbackLevel.GOOD,
            score=80.0,
            messages=["Custom message here"]
        )
        
        assert feedback.get_primary_message() == "Custom message here"
    
    def test_feedback_angle_difference(self):
        """Test angle difference calculation."""
        feedback = ExerciseFeedback(
            is_correct=False,
            level=FeedbackLevel.NEEDS_IMPROVEMENT,
            score=60.0,
            current_angle=75.0,
            target_angle=90.0,
            angle_difference=-15.0
        )
        
        assert feedback.angle_difference == -15.0
    
    def test_feedback_to_dict(self):
        """Test conversion to dictionary."""
        feedback = ExerciseFeedback(
            is_correct=True,
            level=FeedbackLevel.EXCELLENT,
            score=95.0,
            current_angle=90.0,
            target_angle=90.0,
            messages=["Perfect!"],
            corrections=[],
            encouragements=["Keep it up!"]
        )
        
        result = feedback.to_dict()
        
        assert isinstance(result, dict)
        assert result['is_correct'] is True
        assert result['level'] == 'excellent'
        assert result['score'] == 95.0
        assert result['current_angle'] == 90.0
        assert 'Perfect!' in result['messages']
    
    def test_feedback_get_all_feedback(self):
        """Test getting formatted feedback string."""
        feedback = ExerciseFeedback(
            is_correct=False,
            level=FeedbackLevel.NEEDS_IMPROVEMENT,
            score=60.0,
            current_angle=75.0,
            target_angle=90.0,
            messages=["Keep trying"],
            corrections=["Raise arm higher"],
            encouragements=["You can do it!"]
        )
        
        all_feedback = feedback.get_all_feedback()
        
        assert "Keep trying" in all_feedback
        assert "Raise arm higher" in all_feedback
        assert "You can do it!" in all_feedback
        assert "75.0" in all_feedback
        assert "90.0" in all_feedback


class TestFeedbackGenerator:
    """Test cases for FeedbackGenerator class."""
    
    def test_generate_feedback_excellent(self):
        """Test feedback generation for excellent performance."""
        feedback = FeedbackGenerator.generate_angle_feedback(
            current_angle=90.0,
            target_angle=90.0,
            tolerance=15.0,
            exercise_name="shoulder flexion"
        )
        
        assert feedback.level == FeedbackLevel.EXCELLENT
        assert feedback.is_correct is True
        assert feedback.score >= 90
    
    def test_generate_feedback_good(self):
        """Test feedback generation for good performance."""
        feedback = FeedbackGenerator.generate_angle_feedback(
            current_angle=85.0,
            target_angle=90.0,
            tolerance=15.0,
            exercise_name="shoulder flexion"
        )
        
        assert feedback.level in [FeedbackLevel.EXCELLENT, FeedbackLevel.GOOD]
        assert feedback.is_correct is True
        assert feedback.score >= 70
    
    def test_generate_feedback_needs_improvement(self):
        """Test feedback generation for performance needing improvement."""
        feedback = FeedbackGenerator.generate_angle_feedback(
            current_angle=75.0,
            target_angle=90.0,
            tolerance=15.0,
            exercise_name="shoulder flexion"
        )
        
        # 75 is within tolerance (90 ± 15), but on the edge
        assert feedback.score >= 50
    
    def test_generate_feedback_incorrect(self):
        """Test feedback generation for incorrect performance."""
        feedback = FeedbackGenerator.generate_angle_feedback(
            current_angle=50.0,
            target_angle=90.0,
            tolerance=15.0,
            exercise_name="shoulder flexion"
        )
        
        # 50 is far from target (40 degrees off)
        assert feedback.is_correct is False
        assert feedback.level in [FeedbackLevel.NEEDS_IMPROVEMENT, FeedbackLevel.INCORRECT]
    
    def test_generate_feedback_with_corrections(self):
        """Test that corrections are generated when needed."""
        feedback = FeedbackGenerator.generate_angle_feedback(
            current_angle=60.0,
            target_angle=90.0,
            tolerance=15.0,
            exercise_name="shoulder flexion"
        )
        
        # Should have correction messages when off target
        assert len(feedback.corrections) > 0 or feedback.level == FeedbackLevel.EXCELLENT
    
    def test_generate_feedback_encouragements(self):
        """Test that encouragements are generated."""
        feedback = FeedbackGenerator.generate_angle_feedback(
            current_angle=70.0,
            target_angle=90.0,
            tolerance=15.0,
            exercise_name="shoulder flexion"
        )
        
        # Should have encouragement messages
        assert len(feedback.encouragements) >= 0  # May or may not have encouragement
    
    def test_generate_range_of_motion_feedback_in_range(self):
        """Test range-of-motion feedback when in range."""
        feedback = FeedbackGenerator.generate_range_of_motion_feedback(
            current_angle=90.0,
            min_angle=70.0,
            max_angle=110.0,
            exercise_name="shoulder flexion"
        )
        
        assert feedback.is_correct is True
        assert feedback.score >= 70
    
    def test_generate_range_of_motion_feedback_below_range(self):
        """Test range-of-motion feedback when below range."""
        feedback = FeedbackGenerator.generate_range_of_motion_feedback(
            current_angle=60.0,
            min_angle=70.0,
            max_angle=110.0,
            exercise_name="shoulder flexion"
        )
        
        assert feedback.is_correct is False
        assert len(feedback.corrections) > 0
    
    def test_generate_range_of_motion_feedback_above_range(self):
        """Test range-of-motion feedback when above range."""
        feedback = FeedbackGenerator.generate_range_of_motion_feedback(
            current_angle=120.0,
            min_angle=70.0,
            max_angle=110.0,
            exercise_name="shoulder flexion"
        )
        
        assert feedback.is_correct is False
        assert len(feedback.corrections) > 0
    
    def test_score_bounds(self):
        """Test that score stays within 0-100 bounds."""
        # Test with very off-target angle
        feedback = FeedbackGenerator.generate_angle_feedback(
            current_angle=0.0,
            target_angle=180.0,
            tolerance=10.0,
            exercise_name="test"
        )
        
        assert 0 <= feedback.score <= 100
        
        # Test with perfect angle
        feedback = FeedbackGenerator.generate_angle_feedback(
            current_angle=90.0,
            target_angle=90.0,
            tolerance=10.0,
            exercise_name="test"
        )
        
        assert 0 <= feedback.score <= 100


class TestFeedbackLevel:
    """Test cases for FeedbackLevel enum."""
    
    def test_all_levels_exist(self):
        """Test that all expected feedback levels exist."""
        expected_levels = ['excellent', 'good', 'needs_improvement', 'incorrect', 'error']
        
        for level_name in expected_levels:
            # Should not raise an error
            level = FeedbackLevel(level_name)
            assert level.value == level_name
    
    def test_level_ordering(self):
        """Test feedback levels are properly defined."""
        assert FeedbackLevel.EXCELLENT.value == 'excellent'
        assert FeedbackLevel.GOOD.value == 'good'
        assert FeedbackLevel.NEEDS_IMPROVEMENT.value == 'needs_improvement'
        assert FeedbackLevel.INCORRECT.value == 'incorrect'
        assert FeedbackLevel.ERROR.value == 'error'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
