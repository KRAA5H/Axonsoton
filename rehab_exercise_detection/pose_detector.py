"""
Pose Detection Module

Uses MediaPipe Pose to detect human body landmarks from images or video frames.
"""

import cv2
import numpy as np
import mediapipe as mp
from typing import Optional, Tuple, Dict, Any, NamedTuple
from dataclasses import dataclass


@dataclass
class Landmark:
    """Represents a single pose landmark with coordinates and visibility."""
    x: float
    y: float
    z: float
    visibility: float
    
    def to_array(self) -> np.ndarray:
        """Convert landmark to numpy array [x, y, z]."""
        return np.array([self.x, self.y, self.z])
    
    def to_2d_array(self) -> np.ndarray:
        """Convert landmark to 2D numpy array [x, y]."""
        return np.array([self.x, self.y])


class PoseLandmarks:
    """
    Container for all pose landmarks detected by MediaPipe.
    
    Provides easy access to specific body landmarks by name.
    """
    
    # MediaPipe Pose landmark indices
    LANDMARK_NAMES = {
        'nose': 0,
        'left_eye_inner': 1,
        'left_eye': 2,
        'left_eye_outer': 3,
        'right_eye_inner': 4,
        'right_eye': 5,
        'right_eye_outer': 6,
        'left_ear': 7,
        'right_ear': 8,
        'mouth_left': 9,
        'mouth_right': 10,
        'left_shoulder': 11,
        'right_shoulder': 12,
        'left_elbow': 13,
        'right_elbow': 14,
        'left_wrist': 15,
        'right_wrist': 16,
        'left_pinky': 17,
        'right_pinky': 18,
        'left_index': 19,
        'right_index': 20,
        'left_thumb': 21,
        'right_thumb': 22,
        'left_hip': 23,
        'right_hip': 24,
        'left_knee': 25,
        'right_knee': 26,
        'left_ankle': 27,
        'right_ankle': 28,
        'left_heel': 29,
        'right_heel': 30,
        'left_foot_index': 31,
        'right_foot_index': 32,
    }
    
    def __init__(self, landmarks: list):
        """
        Initialize PoseLandmarks with MediaPipe landmark data.
        
        Args:
            landmarks: List of MediaPipe landmark objects
        """
        self._landmarks = []
        for lm in landmarks:
            self._landmarks.append(Landmark(
                x=lm.x,
                y=lm.y,
                z=lm.z,
                visibility=lm.visibility
            ))
    
    def get(self, name: str) -> Optional[Landmark]:
        """
        Get a landmark by name.
        
        Args:
            name: Name of the landmark (e.g., 'left_shoulder')
            
        Returns:
            Landmark object or None if not found
        """
        if name not in self.LANDMARK_NAMES:
            return None
        idx = self.LANDMARK_NAMES[name]
        return self._landmarks[idx] if idx < len(self._landmarks) else None
    
    def get_by_index(self, index: int) -> Optional[Landmark]:
        """
        Get a landmark by index.
        
        Args:
            index: Index of the landmark
            
        Returns:
            Landmark object or None if index is out of range
        """
        return self._landmarks[index] if index < len(self._landmarks) else None
    
    def all(self) -> list:
        """Return all landmarks."""
        return self._landmarks.copy()
    
    def is_visible(self, name: str, threshold: float = 0.5) -> bool:
        """
        Check if a landmark is visible above a threshold.
        
        Args:
            name: Name of the landmark
            threshold: Visibility threshold (0-1)
            
        Returns:
            True if the landmark is visible above the threshold
        """
        landmark = self.get(name)
        return landmark is not None and landmark.visibility >= threshold


class PoseDetector:
    """
    Detects human pose using MediaPipe Pose.
    
    This class wraps MediaPipe's Pose solution to provide easy-to-use
    pose detection for rehabilitation exercise analysis.
    """
    
    def __init__(
        self,
        static_image_mode: bool = False,
        model_complexity: int = 1,
        smooth_landmarks: bool = True,
        enable_segmentation: bool = False,
        smooth_segmentation: bool = True,
        min_detection_confidence: float = 0.5,
        min_tracking_confidence: float = 0.5
    ):
        """
        Initialize the PoseDetector.
        
        Args:
            static_image_mode: If True, treats each image independently.
            model_complexity: Complexity of the pose model (0, 1, or 2).
            smooth_landmarks: If True, filters landmarks across frames.
            enable_segmentation: If True, generates segmentation mask.
            smooth_segmentation: If True, filters segmentation mask.
            min_detection_confidence: Minimum confidence for detection.
            min_tracking_confidence: Minimum confidence for tracking.
        """
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        self.pose = self.mp_pose.Pose(
            static_image_mode=static_image_mode,
            model_complexity=model_complexity,
            smooth_landmarks=smooth_landmarks,
            enable_segmentation=enable_segmentation,
            smooth_segmentation=smooth_segmentation,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        
        self._last_results = None
    
    def detect(self, image: np.ndarray) -> Optional[PoseLandmarks]:
        """
        Detect pose landmarks in an image.
        
        Args:
            image: BGR image from OpenCV or RGB image
            
        Returns:
            PoseLandmarks object if pose detected, None otherwise
        """
        # Convert BGR to RGB if needed (assuming BGR from OpenCV)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Process the image
        self._last_results = self.pose.process(image_rgb)
        
        if self._last_results.pose_landmarks:
            return PoseLandmarks(self._last_results.pose_landmarks.landmark)
        return None
    
    def detect_from_rgb(self, image: np.ndarray) -> Optional[PoseLandmarks]:
        """
        Detect pose landmarks from an RGB image.
        
        Args:
            image: RGB image
            
        Returns:
            PoseLandmarks object if pose detected, None otherwise
        """
        self._last_results = self.pose.process(image)
        
        if self._last_results.pose_landmarks:
            return PoseLandmarks(self._last_results.pose_landmarks.landmark)
        return None
    
    def draw_landmarks(
        self,
        image: np.ndarray,
        landmarks: Optional[PoseLandmarks] = None,
        draw_connections: bool = True
    ) -> np.ndarray:
        """
        Draw pose landmarks on an image.
        
        Args:
            image: Image to draw on (BGR format)
            landmarks: PoseLandmarks to draw (uses last detection if None)
            draw_connections: If True, draw connections between landmarks
            
        Returns:
            Image with landmarks drawn
        """
        annotated_image = image.copy()
        
        if self._last_results and self._last_results.pose_landmarks:
            self.mp_drawing.draw_landmarks(
                annotated_image,
                self._last_results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS if draw_connections else None,
                self.mp_drawing_styles.get_default_pose_landmarks_style()
            )
        
        return annotated_image
    
    def get_world_landmarks(self) -> Optional[PoseLandmarks]:
        """
        Get the 3D world landmarks from the last detection.
        
        World landmarks have real-world 3D coordinates in meters with
        the origin at the hip center.
        
        Returns:
            PoseLandmarks object with world coordinates or None
        """
        if self._last_results and self._last_results.pose_world_landmarks:
            return PoseLandmarks(self._last_results.pose_world_landmarks.landmark)
        return None
    
    def close(self):
        """Release resources."""
        self.pose.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
