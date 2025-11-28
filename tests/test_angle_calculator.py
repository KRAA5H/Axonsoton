"""
Tests for the angle calculator module.
"""

import pytest
import numpy as np
from unittest.mock import MagicMock

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rehab_exercise_detection.angle_calculator import AngleCalculator
from rehab_exercise_detection.pose_detector import Landmark, PoseLandmarks


class TestAngleCalculator:
    """Test cases for AngleCalculator class."""
    
    def test_calculate_angle_90_degrees(self):
        """Test calculation of a 90-degree angle."""
        p1 = np.array([0, 0])
        vertex = np.array([0, 1])
        p3 = np.array([1, 1])
        
        angle = AngleCalculator.calculate_angle(p1, vertex, p3)
        assert abs(angle - 90.0) < 0.1
    
    def test_calculate_angle_180_degrees(self):
        """Test calculation of a straight line (180 degrees)."""
        p1 = np.array([0, 0])
        vertex = np.array([1, 0])
        p3 = np.array([2, 0])
        
        angle = AngleCalculator.calculate_angle(p1, vertex, p3)
        assert abs(angle - 180.0) < 0.1
    
    def test_calculate_angle_45_degrees(self):
        """Test calculation of a 45-degree angle."""
        p1 = np.array([0, 1])
        vertex = np.array([0, 0])
        p3 = np.array([1, 1])
        
        angle = AngleCalculator.calculate_angle(p1, vertex, p3)
        assert abs(angle - 45.0) < 0.1
    
    def test_calculate_angle_60_degrees(self):
        """Test calculation of a 60-degree angle."""
        p1 = np.array([0, 0])
        vertex = np.array([0, 0])
        p3 = np.array([1, np.sqrt(3)])  # 60 degrees from x-axis
        
        # Create a proper 60-degree angle
        p1 = np.array([1, 0])
        vertex = np.array([0, 0])
        p3 = np.array([0.5, np.sqrt(3)/2])
        
        angle = AngleCalculator.calculate_angle(p1, vertex, p3)
        assert abs(angle - 60.0) < 0.5
    
    def test_calculate_angle_3d(self):
        """Test angle calculation with 3D points."""
        p1 = np.array([0, 0, 0])
        vertex = np.array([0, 1, 0])
        p3 = np.array([1, 1, 0])
        
        angle = AngleCalculator.calculate_angle(p1, vertex, p3)
        assert abs(angle - 90.0) < 0.1
    
    def test_calculate_angle_2d_tuple(self):
        """Test 2D angle calculation with tuples."""
        angle = AngleCalculator.calculate_angle_2d(
            (0, 0), (0, 1), (1, 1)
        )
        assert abs(angle - 90.0) < 0.1
    
    def test_calculate_angle_from_landmarks(self):
        """Test angle calculation from Landmark objects."""
        lm1 = Landmark(x=0, y=0, z=0, visibility=1.0)
        lm2 = Landmark(x=0, y=1, z=0, visibility=1.0)
        lm3 = Landmark(x=1, y=1, z=0, visibility=1.0)
        
        angle = AngleCalculator.calculate_angle_from_landmarks(
            lm1, lm2, lm3, use_3d=False
        )
        assert abs(angle - 90.0) < 0.1
    
    def test_zero_length_vector_handling(self):
        """Test handling of zero-length vectors."""
        # Same points should not cause division by zero
        p1 = np.array([0, 0])
        vertex = np.array([0, 0])
        p3 = np.array([0, 0])
        
        # Should return a valid number (handling edge case)
        angle = AngleCalculator.calculate_angle(p1, vertex, p3)
        assert not np.isnan(angle)


class TestLandmark:
    """Test cases for Landmark class."""
    
    def test_landmark_creation(self):
        """Test basic landmark creation."""
        lm = Landmark(x=0.5, y=0.3, z=0.1, visibility=0.9)
        assert lm.x == 0.5
        assert lm.y == 0.3
        assert lm.z == 0.1
        assert lm.visibility == 0.9
    
    def test_landmark_to_array(self):
        """Test conversion to numpy array."""
        lm = Landmark(x=0.5, y=0.3, z=0.1, visibility=0.9)
        arr = lm.to_array()
        
        assert isinstance(arr, np.ndarray)
        assert len(arr) == 3
        assert arr[0] == 0.5
        assert arr[1] == 0.3
        assert arr[2] == 0.1
    
    def test_landmark_to_2d_array(self):
        """Test conversion to 2D numpy array."""
        lm = Landmark(x=0.5, y=0.3, z=0.1, visibility=0.9)
        arr = lm.to_2d_array()
        
        assert isinstance(arr, np.ndarray)
        assert len(arr) == 2
        assert arr[0] == 0.5
        assert arr[1] == 0.3


class TestAngleCalculatorJointMethods:
    """Test joint-specific angle calculation methods."""
    
    def _create_mock_pose_landmarks(self, landmarks_dict):
        """Create a mock PoseLandmarks object with specified landmarks."""
        mock_landmarks = MagicMock(spec=PoseLandmarks)
        
        def get_landmark(name):
            return landmarks_dict.get(name)
        
        mock_landmarks.get = get_landmark
        return mock_landmarks
    
    def test_shoulder_flexion_angle(self):
        """Test shoulder flexion angle calculation."""
        # Create mock landmarks representing arm raised 90 degrees
        landmarks = {
            'left_hip': Landmark(x=0.4, y=0.8, z=0, visibility=1.0),
            'left_shoulder': Landmark(x=0.4, y=0.5, z=0, visibility=1.0),
            'left_elbow': Landmark(x=0.7, y=0.5, z=0, visibility=1.0),  # Arm horizontal
        }
        mock_pose = self._create_mock_pose_landmarks(landmarks)
        
        angle = AngleCalculator.get_shoulder_flexion_angle(mock_pose, side='left')
        assert angle is not None
        # With arm horizontal (90 degrees from body), should be close to 90
        assert 70 <= angle <= 110
    
    def test_shoulder_flexion_returns_none_for_missing_landmarks(self):
        """Test that None is returned when landmarks are missing."""
        landmarks = {
            'left_hip': Landmark(x=0.4, y=0.8, z=0, visibility=1.0),
            # Missing shoulder and elbow
        }
        mock_pose = self._create_mock_pose_landmarks(landmarks)
        
        angle = AngleCalculator.get_shoulder_flexion_angle(mock_pose, side='left')
        assert angle is None
    
    def test_elbow_flexion_angle(self):
        """Test elbow flexion angle calculation."""
        landmarks = {
            'left_shoulder': Landmark(x=0.4, y=0.5, z=0, visibility=1.0),
            'left_elbow': Landmark(x=0.4, y=0.7, z=0, visibility=1.0),
            'left_wrist': Landmark(x=0.6, y=0.7, z=0, visibility=1.0),  # 90 degree bend
        }
        mock_pose = self._create_mock_pose_landmarks(landmarks)
        
        angle = AngleCalculator.get_elbow_flexion_angle(mock_pose, side='left')
        assert angle is not None
        # Bent elbow at 90 degrees
        assert 70 <= angle <= 110
    
    def test_knee_flexion_angle(self):
        """Test knee flexion angle calculation."""
        landmarks = {
            'left_hip': Landmark(x=0.4, y=0.5, z=0, visibility=1.0),
            'left_knee': Landmark(x=0.4, y=0.7, z=0, visibility=1.0),
            'left_ankle': Landmark(x=0.4, y=0.9, z=0, visibility=1.0),  # Straight leg
        }
        mock_pose = self._create_mock_pose_landmarks(landmarks)
        
        angle = AngleCalculator.get_knee_flexion_angle(mock_pose, side='left')
        assert angle is not None
        # Straight leg should be close to 0 degrees flexion
        assert 0 <= angle <= 20


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
