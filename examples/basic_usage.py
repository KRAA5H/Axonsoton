#!/usr/bin/env python3
"""
Example: Basic usage of the rehab exercise detection system.

This example shows the fundamental concepts and API usage.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rehab_exercise_detection import (
    PoseDetector,
    AngleCalculator,
    ExerciseEvaluator,
    ShoulderFlexion,
    ElbowFlexion,
    ExerciseConfig,
    FeedbackLevel
)


def example_basic_usage():
    """Demonstrate basic API usage without camera/video."""
    print("=" * 60)
    print("Rehab Exercise Detection - Basic Usage Example")
    print("=" * 60)
    
    # 1. List available exercises
    print("\n1. Available exercises:")
    exercises = ExerciseEvaluator.available_exercises()
    for ex in exercises:
        print(f"   - {ex}")
    
    # 2. Create an exercise with custom configuration
    print("\n2. Creating shoulder flexion exercise:")
    config = ExerciseConfig(
        target_angle=90.0,    # Target 90 degrees
        tolerance=15.0,       # ±15 degrees acceptable
        side='left',          # Evaluate left arm
        use_3d=False          # Use 2D angle calculation
    )
    
    shoulder_exercise = ShoulderFlexion(config)
    print(f"   Name: {shoulder_exercise.name}")
    print(f"   Description: {shoulder_exercise.description}")
    print(f"   Target angle: {config.target_angle}°")
    print(f"   Tolerance: ±{config.tolerance}°")
    
    # 3. Show exercise instructions
    print("\n3. Exercise instructions:")
    for i, instruction in enumerate(shoulder_exercise.instructions, 1):
        print(f"   {i}. {instruction}")
    
    # 4. Create an evaluator
    print("\n4. Setting up exercise evaluator:")
    evaluator = ExerciseEvaluator(target_reps=5)
    evaluator.set_exercise(shoulder_exercise)
    print(f"   Exercise set: {evaluator.exercise.name}")
    print(f"   Target reps: {evaluator.target_reps}")
    
    # 5. Explain feedback levels
    print("\n5. Feedback levels:")
    for level in FeedbackLevel:
        print(f"   - {level.value}")
    
    # 6. Show how angle calculation works
    print("\n6. Angle calculation example:")
    print("   For shoulder flexion, we measure the angle between:")
    print("   - Hip (reference point)")
    print("   - Shoulder (vertex)")
    print("   - Elbow (end point)")
    print("\n   A person with their arm:")
    print("   - At their side: ~0° flexion")
    print("   - Horizontal forward: ~90° flexion")
    print("   - Straight up: ~180° flexion")
    
    print("\n" + "=" * 60)
    print("For real-time detection, use the webcam_exercise_demo.py example")
    print("For video analysis, use the video_analysis.py example")
    print("=" * 60)


def example_angle_calculations():
    """Demonstrate angle calculation utilities."""
    import numpy as np
    
    print("\n" + "=" * 60)
    print("Angle Calculation Examples")
    print("=" * 60)
    
    # Example: Calculate angle at a vertex point
    print("\n1. Basic angle calculation:")
    
    # Points forming a 90-degree angle
    p1 = np.array([0, 0])      # First point
    vertex = np.array([0, 1])   # Vertex (where angle is measured)
    p3 = np.array([1, 1])       # Third point
    
    angle = AngleCalculator.calculate_angle(p1, vertex, p3)
    print(f"   Points: ({p1}) - ({vertex}) - ({p3})")
    print(f"   Calculated angle: {angle:.1f}°")
    
    # Example: Straight line (180 degrees)
    print("\n2. Straight line (180°):")
    p1 = np.array([0, 0])
    vertex = np.array([1, 0])
    p3 = np.array([2, 0])
    angle = AngleCalculator.calculate_angle(p1, vertex, p3)
    print(f"   Points: ({p1}) - ({vertex}) - ({p3})")
    print(f"   Calculated angle: {angle:.1f}°")
    
    # Example: 45-degree angle
    print("\n3. 45-degree angle:")
    p1 = np.array([0, 1])
    vertex = np.array([0, 0])
    p3 = np.array([1, 1])
    angle = AngleCalculator.calculate_angle(p1, vertex, p3)
    print(f"   Points: ({p1}) - ({vertex}) - ({p3})")
    print(f"   Calculated angle: {angle:.1f}°")


def example_feedback_system():
    """Demonstrate the feedback generation system."""
    from rehab_exercise_detection.feedback import FeedbackGenerator
    
    print("\n" + "=" * 60)
    print("Feedback System Examples")
    print("=" * 60)
    
    target_angle = 90.0
    tolerance = 15.0
    
    print(f"\nTarget angle: {target_angle}°")
    print(f"Tolerance: ±{tolerance}°")
    print("\nFeedback for various angles:")
    print("-" * 40)
    
    test_angles = [90, 85, 95, 80, 100, 70, 110, 50, 130]
    
    for angle in test_angles:
        feedback = FeedbackGenerator.generate_angle_feedback(
            current_angle=float(angle),
            target_angle=target_angle,
            tolerance=tolerance,
            exercise_name="shoulder flexion"
        )
        
        status = "✓" if feedback.is_correct else "✗"
        print(f"   {angle:3d}° → {feedback.level.value:20s} "
              f"Score: {feedback.score:5.1f}% {status}")


if __name__ == "__main__":
    example_basic_usage()
    example_angle_calculations()
    example_feedback_system()
