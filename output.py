import cv2
import os

def extract_frames_from_video(video_path, output_folder, frame_rate=1):
    """Extract frames from a video and save them to a single output folder."""
    os.makedirs(output_folder, exist_ok=True)
    video_capture = cv2.VideoCapture(video_path)
    frame_count = 0

    while True:
        success, frame = video_capture.read()
        if not success:
            break

        # Save frames at the specified frame rate
        if frame_count % frame_rate == 0:
            # Create a unique filename using the video name and frame count
            video_name = os.path.basename(video_path).split('.')[0]
            frame_filename = os.path.join(output_folder, f"{video_name}_frame_{frame_count}.jpg")
            cv2.imwrite(frame_filename, frame)

        frame_count += 1

    video_capture.release()

def convert_videos_to_frames(input_folders, output_folder, frame_rate=1):
    """Convert all .mp4 videos in the input folders to frames in a single output folder."""
    os.makedirs(output_folder, exist_ok=True)

    for input_folder in input_folders:
        video_files = [f for f in os.listdir(input_folder) if f.endswith('.mp4')]

        for video_file in video_files:
            video_path = os.path.join(input_folder, video_file)
            extract_frames_from_video(video_path, output_folder, frame_rate)
            print(f"Finished extracting frames from {video_file} in folder {input_folder}")

# Usage
input_folders = ['fighting/Fighting002_x264.mp4', 'fighting/Fighting003_x264.mp4','fighting/Fighting005_x264.mp4','fighting/Fighting007_x264.mp4','fighting/Fighting009_x264.mp4','fighting/Fighting012_x264.mp4','fighting/Fighting013_x264.mp4','fighting/Fighting014_x264.mp4']  # List of folders where your videos are stored
output_folder = 'Fighting'  # Single folder to save all extracted frames
frame_rate = 30  # Adjust frame rate as needed

convert_videos_to_frames(input_folders, output_folder, frame_rate)
