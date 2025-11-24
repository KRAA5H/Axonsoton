"""
Angle Calculator Module

Provides utilities for calculating joint angles from pose landmarks.
"""

import numpy as np
from typing import Tuple, Optional
from .pose_detector import Landmark, PoseLandmarks


class AngleCalculator:
    """
    Calculates angles between body joints for exercise analysis.
    
    This class provides methods to calculate various joint angles
    commonly used in rehabilitation exercise assessment.
    """
    
    @staticmethod
    def calculate_angle(
        point1: np.ndarray,
        point2: np.ndarray,
        point3: np.ndarray
    ) -> float:
        """
        Calculate the angle at point2 formed by points 1, 2, and 3.
        
        Args:
            point1: First point coordinates [x, y] or [x, y, z]
            point2: Vertex point coordinates [x, y] or [x, y, z]
            point3: Third point coordinates [x, y] or [x, y, z]
            
        Returns:
            Angle in degrees (0-180)
        """
        # Create vectors
        vector1 = point1 - point2
        vector2 = point3 - point2
        
        # Calculate angle using dot product
        cos_angle = np.dot(vector1, vector2) / (
            np.linalg.norm(vector1) * np.linalg.norm(vector2) + 1e-10
        )
        
        # Clamp to avoid numerical errors
        cos_angle = np.clip(cos_angle, -1.0, 1.0)
        
        # Convert to degrees
        angle = np.degrees(np.arccos(cos_angle))
        
        return angle
    
    @staticmethod
    def calculate_angle_2d(
        point1: Tuple[float, float],
        point2: Tuple[float, float],
        point3: Tuple[float, float]
    ) -> float:
        """
        Calculate 2D angle at point2 formed by points 1, 2, and 3.
        
        Args:
            point1: First point (x, y)
            point2: Vertex point (x, y)
            point3: Third point (x, y)
            
        Returns:
            Angle in degrees (0-180)
        """
        return AngleCalculator.calculate_angle(
            np.array(point1),
            np.array(point2),
            np.array(point3)
        )
    
    @staticmethod
    def calculate_angle_from_landmarks(
        landmark1: Landmark,
        landmark2: Landmark,
        landmark3: Landmark,
        use_3d: bool = False
    ) -> float:
        """
        Calculate angle from three Landmark objects.
        
        Args:
            landmark1: First landmark
            landmark2: Vertex landmark (where angle is measured)
            landmark3: Third landmark
            use_3d: If True, use 3D coordinates; otherwise use 2D
            
        Returns:
            Angle in degrees (0-180)
        """
        if use_3d:
            p1 = landmark1.to_array()
            p2 = landmark2.to_array()
            p3 = landmark3.to_array()
        else:
            p1 = landmark1.to_2d_array()
            p2 = landmark2.to_2d_array()
            p3 = landmark3.to_2d_array()
        
        return AngleCalculator.calculate_angle(p1, p2, p3)
    
    @staticmethod
    def get_shoulder_flexion_angle(
        landmarks: PoseLandmarks,
        side: str = 'left',
        use_3d: bool = False
    ) -> Optional[float]:
        """
        Calculate shoulder flexion angle.
        
        Shoulder flexion is the angle of the arm raised forward from the body.
        Measured from the hip through shoulder to elbow.
        
        Args:
            landmarks: PoseLandmarks object
            side: 'left' or 'right'
            use_3d: If True, use 3D coordinates
            
        Returns:
            Shoulder flexion angle in degrees, or None if landmarks not visible
        """
        hip = landmarks.get(f'{side}_hip')
        shoulder = landmarks.get(f'{side}_shoulder')
        elbow = landmarks.get(f'{side}_elbow')
        
        if not all([hip, shoulder, elbow]):
            return None
        
        angle = AngleCalculator.calculate_angle_from_landmarks(
            hip, shoulder, elbow, use_3d
        )
        
        # Convert to flexion angle (180 - calculated angle gives flexion from body)
        return 180 - angle
    
    @staticmethod
    def get_shoulder_abduction_angle(
        landmarks: PoseLandmarks,
        side: str = 'left',
        use_3d: bool = False
    ) -> Optional[float]:
        """
        Calculate shoulder abduction angle.
        
        Shoulder abduction is the angle of the arm raised sideways from the body.
        For frontal plane assessment.
        
        Args:
            landmarks: PoseLandmarks object
            side: 'left' or 'right'
            use_3d: If True, use 3D coordinates
            
        Returns:
            Shoulder abduction angle in degrees, or None if landmarks not visible
        """
        # Use opposite shoulder and same side hip to create torso reference
        if side == 'left':
            opposite_shoulder = landmarks.get('right_shoulder')
        else:
            opposite_shoulder = landmarks.get('left_shoulder')
        
        shoulder = landmarks.get(f'{side}_shoulder')
        elbow = landmarks.get(f'{side}_elbow')
        
        if not all([opposite_shoulder, shoulder, elbow]):
            return None
        
        angle = AngleCalculator.calculate_angle_from_landmarks(
            opposite_shoulder, shoulder, elbow, use_3d
        )
        
        return 180 - angle
    
    @staticmethod
    def get_elbow_flexion_angle(
        landmarks: PoseLandmarks,
        side: str = 'left',
        use_3d: bool = False
    ) -> Optional[float]:
        """
        Calculate elbow flexion angle.
        
        Elbow flexion is the angle between upper arm and forearm.
        
        Args:
            landmarks: PoseLandmarks object
            side: 'left' or 'right'
            use_3d: If True, use 3D coordinates
            
        Returns:
            Elbow flexion angle in degrees, or None if landmarks not visible
        """
        shoulder = landmarks.get(f'{side}_shoulder')
        elbow = landmarks.get(f'{side}_elbow')
        wrist = landmarks.get(f'{side}_wrist')
        
        if not all([shoulder, elbow, wrist]):
            return None
        
        angle = AngleCalculator.calculate_angle_from_landmarks(
            shoulder, elbow, wrist, use_3d
        )
        
        # Flexion angle (180 - angle gives how bent the elbow is)
        return 180 - angle
    
    @staticmethod
    def get_knee_flexion_angle(
        landmarks: PoseLandmarks,
        side: str = 'left',
        use_3d: bool = False
    ) -> Optional[float]:
        """
        Calculate knee flexion angle.
        
        Knee flexion is the angle between thigh and lower leg.
        
        Args:
            landmarks: PoseLandmarks object
            side: 'left' or 'right'
            use_3d: If True, use 3D coordinates
            
        Returns:
            Knee flexion angle in degrees, or None if landmarks not visible
        """
        hip = landmarks.get(f'{side}_hip')
        knee = landmarks.get(f'{side}_knee')
        ankle = landmarks.get(f'{side}_ankle')
        
        if not all([hip, knee, ankle]):
            return None
        
        angle = AngleCalculator.calculate_angle_from_landmarks(
            hip, knee, ankle, use_3d
        )
        
        return 180 - angle
    
    @staticmethod
    def get_hip_flexion_angle(
        landmarks: PoseLandmarks,
        side: str = 'left',
        use_3d: bool = False
    ) -> Optional[float]:
        """
        Calculate hip flexion angle.
        
        Hip flexion is the angle of the thigh raised forward from the body.
        
        Args:
            landmarks: PoseLandmarks object
            side: 'left' or 'right'
            use_3d: If True, use 3D coordinates
            
        Returns:
            Hip flexion angle in degrees, or None if landmarks not visible
        """
        shoulder = landmarks.get(f'{side}_shoulder')
        hip = landmarks.get(f'{side}_hip')
        knee = landmarks.get(f'{side}_knee')
        
        if not all([shoulder, hip, knee]):
            return None
        
        angle = AngleCalculator.calculate_angle_from_landmarks(
            shoulder, hip, knee, use_3d
        )
        
        return 180 - angle
    
    @staticmethod
    def get_hip_abduction_angle(
        landmarks: PoseLandmarks,
        side: str = 'left',
        use_3d: bool = False
    ) -> Optional[float]:
        """
        Calculate hip abduction angle.
        
        Hip abduction is the angle of the leg moved sideways from the body.
        
        Args:
            landmarks: PoseLandmarks object
            side: 'left' or 'right'
            use_3d: If True, use 3D coordinates
            
        Returns:
            Hip abduction angle in degrees, or None if landmarks not visible
        """
        if side == 'left':
            opposite_hip = landmarks.get('right_hip')
        else:
            opposite_hip = landmarks.get('left_hip')
        
        hip = landmarks.get(f'{side}_hip')
        knee = landmarks.get(f'{side}_knee')
        
        if not all([opposite_hip, hip, knee]):
            return None
        
        angle = AngleCalculator.calculate_angle_from_landmarks(
            opposite_hip, hip, knee, use_3d
        )
        
        return 180 - angle
    
    @staticmethod
    def get_trunk_lateral_flexion(
        landmarks: PoseLandmarks,
        use_3d: bool = False
    ) -> Optional[float]:
        """
        Calculate trunk lateral flexion angle.
        
        Measures side-bending of the trunk from vertical.
        
        Args:
            landmarks: PoseLandmarks object
            use_3d: If True, use 3D coordinates
            
        Returns:
            Trunk lateral flexion angle in degrees (positive = right, negative = left)
        """
        left_shoulder = landmarks.get('left_shoulder')
        right_shoulder = landmarks.get('right_shoulder')
        left_hip = landmarks.get('left_hip')
        right_hip = landmarks.get('right_hip')
        
        if not all([left_shoulder, right_shoulder, left_hip, right_hip]):
            return None
        
        # Calculate midpoints
        if use_3d:
            shoulder_mid = (left_shoulder.to_array() + right_shoulder.to_array()) / 2
            hip_mid = (left_hip.to_array() + right_hip.to_array()) / 2
        else:
            shoulder_mid = (left_shoulder.to_2d_array() + right_shoulder.to_2d_array()) / 2
            hip_mid = (left_hip.to_2d_array() + right_hip.to_2d_array()) / 2
        
        # Calculate angle from vertical
        trunk_vector = shoulder_mid - hip_mid
        
        if len(trunk_vector) >= 2:
            angle = np.degrees(np.arctan2(trunk_vector[0], -trunk_vector[1]))
            return angle
        
        return None
