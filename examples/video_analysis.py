#!/usr/bin/env python3
"""
Example: Process a video file for exercise detection.

This example demonstrates how to analyze a pre-recorded video
for rehabilitation exercise detection and generate a report.

Usage:
    python video_analysis.py input_video.mp4 --exercise shoulder_flexion
"""

import cv2
import argparse
import json
import sys
import os
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rehab_exercise_detection import (
    ExerciseEvaluator,
    ExerciseConfig
)


def analyze_video(
    video_path: str,
    exercise_name: str,
    side: str = 'left',
    target_angle: float = 90.0,
    output_video: str = None,
    output_report: str = None
):
    """
    Analyze a video for exercise detection.
    
    Args:
        video_path: Path to input video file
        exercise_name: Name of the exercise to evaluate
        side: Body side to evaluate ('left' or 'right')
        target_angle: Target angle for the exercise
        output_video: Optional path to save annotated video
        output_report: Optional path to save JSON report
    """
    print(f"Analyzing video: {video_path}")
    print(f"Exercise: {exercise_name}")
    print(f"Side: {side}")
    print(f"Target angle: {target_angle}°")
    print("-" * 50)
    
    # Open video
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file: {video_path}")
        return None
    
    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    print(f"Video: {frame_width}x{frame_height} @ {fps}fps, {total_frames} frames")
    
    # Setup video writer if output requested
    video_writer = None
    if output_video:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(
            output_video, fourcc, fps, (frame_width, frame_height)
        )
    
    # Configure exercise
    config = ExerciseConfig(
        target_angle=target_angle,
        tolerance=15.0,
        side=side
    )
    
    # Initialize evaluator
    evaluator = ExerciseEvaluator(target_reps=100)  # High number, video-based
    evaluator.set_exercise_by_name(exercise_name, config)
    evaluator.start_session()
    
    # Track results
    frame_results = []
    frames_processed = 0
    
    # Process video
    print("\nProcessing video...")
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        frames_processed += 1
        
        # Evaluate frame
        feedback = evaluator.evaluate_frame(frame)
        
        # Store result
        frame_results.append({
            'frame': frames_processed,
            'timestamp': frames_processed / fps,
            'angle': feedback.current_angle,
            'score': feedback.score,
            'is_correct': feedback.is_correct,
            'level': feedback.level.value
        })
        
        # Draw feedback on frame
        if video_writer:
            annotated = evaluator.draw_feedback(frame, feedback)
            video_writer.write(annotated)
        
        # Progress update
        if frames_processed % 30 == 0:
            progress = (frames_processed / total_frames) * 100
            print(f"  Progress: {progress:.1f}% ({frames_processed}/{total_frames})")
    
    # Cleanup
    cap.release()
    if video_writer:
        video_writer.release()
        print(f"\nAnnotated video saved to: {output_video}")
    
    # Generate report
    session_summary = evaluator.get_session_summary()
    
    # Calculate statistics
    valid_angles = [r['angle'] for r in frame_results if r['angle'] is not None]
    correct_frames = sum(1 for r in frame_results if r['is_correct'])
    
    report = {
        'analysis_date': datetime.now().isoformat(),
        'video_file': video_path,
        'exercise': exercise_name,
        'configuration': {
            'side': side,
            'target_angle': target_angle,
            'tolerance': config.tolerance
        },
        'video_info': {
            'fps': fps,
            'resolution': f"{frame_width}x{frame_height}",
            'total_frames': total_frames,
            'duration_seconds': total_frames / fps
        },
        'results': {
            'frames_processed': frames_processed,
            'frames_with_pose': len(valid_angles),
            'frames_correct': correct_frames,
            'accuracy_percentage': (correct_frames / len(valid_angles) * 100) 
                                   if valid_angles else 0,
            'angle_statistics': {
                'min': min(valid_angles) if valid_angles else None,
                'max': max(valid_angles) if valid_angles else None,
                'mean': sum(valid_angles) / len(valid_angles) if valid_angles else None,
            }
        },
        'session': session_summary,
        'frame_data': frame_results
    }
    
    # Save report
    if output_report:
        with open(output_report, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"Report saved to: {output_report}")
    
    # Print summary
    print("\n" + "=" * 50)
    print("ANALYSIS SUMMARY")
    print("=" * 50)
    print(f"Frames processed: {frames_processed}")
    print(f"Frames with pose detected: {len(valid_angles)}")
    print(f"Frames in correct position: {correct_frames}")
    print(f"Accuracy: {report['results']['accuracy_percentage']:.1f}%")
    
    if valid_angles:
        print(f"\nAngle Statistics:")
        print(f"  Min: {report['results']['angle_statistics']['min']:.1f}°")
        print(f"  Max: {report['results']['angle_statistics']['max']:.1f}°")
        print(f"  Mean: {report['results']['angle_statistics']['mean']:.1f}°")
    
    if session_summary:
        print(f"\nSession Results:")
        print(f"  Completed reps: {session_summary['completed_reps']}")
        print(f"  Average score: {session_summary['average_score']:.1f}%")
    
    evaluator.close()
    return report


def main():
    parser = argparse.ArgumentParser(
        description='Analyze video for rehabilitation exercise detection'
    )
    parser.add_argument('video', help='Path to input video file')
    parser.add_argument(
        '--exercise', '-e',
        default='shoulder_flexion',
        choices=[
            'shoulder_flexion', 'shoulder_abduction',
            'elbow_flexion', 'knee_flexion',
            'hip_flexion', 'hip_abduction'
        ],
        help='Exercise to evaluate (default: shoulder_flexion)'
    )
    parser.add_argument(
        '--side', '-s',
        default='left',
        choices=['left', 'right'],
        help='Body side to evaluate (default: left)'
    )
    parser.add_argument(
        '--target', '-t',
        type=float,
        default=90.0,
        help='Target angle in degrees (default: 90)'
    )
    parser.add_argument(
        '--output-video', '-ov',
        help='Path to save annotated output video'
    )
    parser.add_argument(
        '--output-report', '-or',
        help='Path to save JSON analysis report'
    )
    
    args = parser.parse_args()
    
    # Check input file exists
    if not os.path.exists(args.video):
        print(f"Error: Video file not found: {args.video}")
        sys.exit(1)
    
    analyze_video(
        video_path=args.video,
        exercise_name=args.exercise,
        side=args.side,
        target_angle=args.target,
        output_video=args.output_video,
        output_report=args.output_report
    )


if __name__ == "__main__":
    main()
