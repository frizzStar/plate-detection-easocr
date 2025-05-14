import cv2
import os
import argparse
from tqdm import tqdm  # For progress bar

def extract_frames(video_path, output_dir, frame_skip=10, target_size=(640, 640), img_format="jpg"):
    """
    Extract frames from a video with resizing and frame skipping.
    
    Args:
        video_path (str): Path to input video.
        output_dir (str): Folder to save extracted frames.
        frame_skip (int): Save every Nth frame (default=10).
        target_size (tuple): Resize frames to (width, height).
        img_format (str): Output image format (jpg/png).
    """
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Open video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Could not open video: {video_path}")
    
    # Get video properties
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    duration = total_frames / fps
    
    print(f"Video Info:\n- Frames: {total_frames}\n- FPS: {fps:.1f}\n- Duration: {duration:.1f}s")
    
    saved_count = 0
    frame_count = 0
    
    # Progress bar setup
    pbar = tqdm(total=total_frames, desc="Extracting Frames")
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break  # End of video
        
        # Process every Nth frame
        if frame_count % frame_skip == 0:
            # Resize frame
            resized_frame = cv2.resize(frame, target_size)
            
            # Save frame
            output_path = os.path.join(output_dir, f"frame_{saved_count:06d}.{img_format}")
            cv2.imwrite(output_path, resized_frame)
            saved_count += 1
        
        frame_count += 1
        pbar.update(1)
    
    cap.release()
    pbar.close()
    print(f"Extracted {saved_count} frames to {output_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CCTV Frame Extractor")
    parser.add_argument("--video", type=str, required=True, help="Path to input video")
    parser.add_argument("--output", type=str, default="extracted_frames", help="Output directory")
    parser.add_argument("--skip", type=int, default=10, help="Save every Nth frame")
    parser.add_argument("--img_size", type=int, default=640, help="Resize frames to (size x size)")
    parser.add_argument("--format", type=str, default="jpg", choices=["jpg", "png"], help="Output image format")
    
    args = parser.parse_args()
    
    extract_frames(
        video_path=args.video,
        output_dir=args.output,
        frame_skip=args.skip,
        target_size=(args.img_size, args.img_size),
        img_format=args.format
    )