import cv2
import os
from datetime import datetime

def extract_frames(video_path, output_folder, frame_skip=15, max_frames=None, save_timestamps=False):
    """
    Extract frames from a video with configurable skipping and timestamp logging.
    
    Args:
        video_path (str): Path to the input video file.
        output_folder (str): Folder to save extracted frames.
        frame_skip (int): Save every N-th frame (default=10).
        max_frames (int): Maximum frames to extract (optional).
        save_timestamps (bool): Save timestamps to a CSV file.
    """
    # Create output folders
    os.makedirs(output_folder, exist_ok=True)
    images_folder = os.path.join(output_folder, "images")
    os.makedirs(images_folder, exist_ok=True)
    
    # Open video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise FileNotFoundError(f"Could not open video: {video_path}")
    
    # Video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration_sec = total_frames / fps
    
    print(f"Video Info: {fps} FPS, {total_frames} frames (~{duration_sec:.2f} sec)")
    
    # Timestamp logging
    timestamp_file = None
    if save_timestamps:
        timestamp_file = open(os.path.join(output_folder, "timestamps.csv"), "w")
        timestamp_file.write("frame_number,timestamp_ms\n")
    
    # Frame extraction loop
    count = 0
    saved_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break  # End of video
        
        # Save every N-th frame
        if count % frame_skip == 0:
            frame_filename = os.path.join(images_folder, f"frame_{saved_count:06d}.jpg")
            cv2.imwrite(frame_filename, frame)
            
            # Log timestamp if enabled
            if save_timestamps:
                timestamp_ms = cap.get(cv2.CAP_PROP_POS_MSEC)
                timestamp_file.write(f"{saved_count},{timestamp_ms}\n")
            
            saved_count += 1
            print(f"Saved: {frame_filename}", end="\r")
        
        count += 1
        if max_frames and count >= max_frames:
            break
    
    # Cleanup
    cap.release()
    if timestamp_file:
        timestamp_file.close()
    
    print(f"\nDone! Extracted {saved_count}/{total_frames} frames to {images_folder}")

if __name__ == "__main__":
    # ===== CONFIGURE HERE =====
    VIDEO_PATH = "C:/Users/fahri/OneDrive/Documents/Skripsi/data/raw/data_09_mei_2025_gedel/video_1.mp4"  # Path to your new CCTV footage
    OUTPUT_FOLDER = "C:/Users/fahri/OneDrive/Documents/Skripsi/data/processed/data_09_mei_2025"  # Output folder
    FRAME_SKIP = 10  # Save every 10th frame (adjust based on FPS)
    MAX_FRAMES = None  # Set to 1000 for testing with a subset
    SAVE_TIMESTAMPS = True  # Useful for temporal analysis later
    # =========================
    
    extract_frames(VIDEO_PATH, OUTPUT_FOLDER, FRAME_SKIP, MAX_FRAMES, SAVE_TIMESTAMPS)