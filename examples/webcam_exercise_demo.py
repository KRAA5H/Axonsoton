#!/usr/bin/env python3
"""
Example: Real-time exercise detection from webcam.

This example demonstrates how to use the rehab exercise detection system
to evaluate shoulder flexion exercises in real-time using a webcam.

Usage:
    python webcam_exercise_demo.py
    
Press 'q' to quit, 's' to switch exercises, 'r' to reset session.
"""

import cv2
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rehab_exercise_detection import (
    ExerciseEvaluator,
    ShoulderFlexion,
    ShoulderAbduction,
    ElbowFlexion,
    ExerciseConfig
)


def main():
    """Run the webcam exercise detection demo."""
    print("=" * 60)
    print("Rehab Exercise Detection - Webcam Demo")
    print("=" * 60)
    print("\nControls:")
    print("  q - Quit")
    print("  s - Switch exercise")
    print("  r - Reset session")
    print("  l/r - Switch to left/right side")
    print("\n")
    
    # Available exercises
    exercises = [
        ('shoulder_flexion', 'Shoulder Flexion'),
        ('shoulder_abduction', 'Shoulder Abduction'),
        ('elbow_flexion', 'Elbow Flexion'),
        ('knee_flexion', 'Knee Flexion'),
        ('hip_flexion', 'Hip Flexion'),
        ('hip_abduction', 'Hip Abduction'),
    ]
    current_exercise_idx = 0
    current_side = 'left'
    
    # Initialize evaluator
    evaluator = ExerciseEvaluator(target_reps=10)
    
    def set_current_exercise():
        """Set the current exercise with current settings."""
        exercise_name = exercises[current_exercise_idx][0]
        config = ExerciseConfig(
            target_angle=90.0,  # Default target
            tolerance=15.0,
            side=current_side
        )
        evaluator.set_exercise_by_name(exercise_name, config)
        evaluator.start_session()
        print(f"\nStarted: {exercises[current_exercise_idx][1]} ({current_side} side)")
        print(f"Target: {evaluator.exercise.config.target_angle}° with ±{evaluator.exercise.config.tolerance}° tolerance")
    
    # Register callbacks
    def on_rep_completed(data):
        print(f"  Rep {data['rep_number']} completed! "
              f"{'✓ Good' if data['was_successful'] else '✗ Needs work'}")
    
    def on_session_completed(session):
        print(f"\n{'=' * 40}")
        print(f"Session Complete!")
        print(f"  Total reps: {session.completed_reps}")
        print(f"  Successful: {session.successful_reps}")
        print(f"  Average score: {session.average_score:.1f}%")
        print(f"  Duration: {session.duration:.1f} seconds")
        print(f"{'=' * 40}\n")
    
    evaluator.register_callback('rep_completed', on_rep_completed)
    evaluator.register_callback('session_completed', on_session_completed)
    
    # Set initial exercise
    set_current_exercise()
    
    # Open webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        print("Please ensure a webcam is connected and accessible.")
        return
    
    # Set resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    print("\nWebcam opened. Starting detection...")
    print("Stand in front of the camera with your full body visible.\n")
    
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break
            
            # Mirror the frame for more intuitive interaction
            frame = cv2.flip(frame, 1)
            
            # Evaluate the current frame
            feedback = evaluator.evaluate_frame(frame)
            
            # Draw feedback on frame
            annotated_frame = evaluator.draw_feedback(frame, feedback)
            
            # Add instructions
            cv2.putText(
                annotated_frame,
                "q:Quit | s:Switch Exercise | r:Reset | l/r:Change Side",
                (10, annotated_frame.shape[0] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1
            )
            
            # Display
            cv2.imshow('Rehab Exercise Detection', annotated_frame)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                break
            elif key == ord('s'):
                # Switch to next exercise
                current_exercise_idx = (current_exercise_idx + 1) % len(exercises)
                set_current_exercise()
            elif key == ord('r'):
                # Reset current session
                evaluator.reset()
                evaluator.start_session()
                print("\nSession reset.")
            elif key == ord('l'):
                current_side = 'left'
                set_current_exercise()
            elif key == ord('r'):
                current_side = 'right'
                set_current_exercise()
    
    finally:
        cap.release()
        cv2.destroyAllWindows()
        evaluator.close()
        print("\nDemo ended.")


if __name__ == "__main__":
    main()
