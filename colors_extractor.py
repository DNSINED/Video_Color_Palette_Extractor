import os
import cv2
import numpy as np
import extcolors
from colormap import rgb2hex
from PIL import Image
from datetime import timedelta

def format_timedelta(td):
    """Format a timedelta object into a string suitable for file names."""
    result = str(td)
    try:
        result, ms = result.split(".")
    except ValueError:
        ms = "00"
    ms = int(ms)
    ms = round(ms / 1e4)
    result = result.replace(":", "-")  
    return f"{result}.{ms:02}"


def get_saved_frames_durations(cap, saving_fps):
    """Generate a list of timestamps for saving frames based on the desired FPS."""
    durations = []
    clip_duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
    for i in np.arange(0, clip_duration, 1 / saving_fps):
        durations.append(i)
    return durations

def frame_extractor(video_file, saving_fps):
    """Extract frames from a video file and save them as images.

    Args:
        video_file (str): Path to the video file.
        saving_fps (int): Number of frames to save per second.

    Returns:
        List[str]: List of paths to the saved frame images.
    """
    frame_dir, _ = os.path.splitext(video_file)
    frame_dir += "_frames"
    if not os.path.isdir(frame_dir):
        os.mkdir(frame_dir)

    cap = cv2.VideoCapture(video_file)
    fps = cap.get(cv2.CAP_PROP_FPS)
    saving_frames_per_second = min(fps, saving_fps)
    saving_frames_durations = get_saved_frames_durations(cap, saving_frames_per_second)

    frame_paths = []
    count = 0

    while True:
        is_read, frame = cap.read()
        if not is_read:
            break

        frame_duration = count / fps
        if saving_frames_durations and frame_duration >= saving_frames_durations[0]:
            frame_duration_formatted = format_timedelta(timedelta(seconds=frame_duration))
            frame_path = os.path.join(frame_dir, f"frame{frame_duration_formatted}.jpg")
            cv2.imwrite(frame_path, frame)
            frame_paths.append(frame_path)
            saving_frames_durations.pop(0)

        count += 1

    cap.release()
    return frame_paths

def extract_colors(image_path, resize=400, tolerance=5, limit=20):
    """Extract dominant colors from an image.

    Args:
        image_path (str): Path to the image file.
        resize (int): Resize width for processing.
        tolerance (int): Tolerance for color extraction.
        limit (int): Maximum number of colors to extract.

    Returns:
        List[Tuple[str, float]]: List of color hex codes and their occurrence rates.
    """
    img = Image.open(image_path)
    if img.size[0] > resize:
        wpercent = resize / float(img.size[0])
        hsize = int((float(img.size[1]) * wpercent))
        img = img.resize((resize, hsize), Image.Resampling.LANCZOS)

    colors_x = extcolors.extract_from_image(img, tolerance=tolerance, limit=limit)
    colors_hex = [rgb2hex(r, g, b) for (r, g, b), _ in colors_x[0]]
    occurrence_rates = [count for _, count in colors_x[0]]

    return list(zip(colors_hex, occurrence_rates))

def process_video_for_colors(video_file, saving_fps=2, resize=400, tolerance=5, limit=20):
    """Process a video to extract dominant colors from its frames.

    Args:
        video_file (str): Path to the video file.
        saving_fps (int): Number of frames to extract per second.
        resize (int): Resize width for color extraction.
        tolerance (int): Tolerance for color extraction.
        limit (int): Maximum number of colors to extract per image.

    Returns:
        List[Tuple[str, float]]: Consolidated list of unique colors and their occurrence rates.
    """
    frame_paths = frame_extractor(video_file, saving_fps)
    all_colors = []

    for frame_path in frame_paths:
        frame_colors = extract_colors(frame_path, resize, tolerance, limit)
        all_colors.extend(frame_colors)

    # Consolidate occurrences of the same color
    color_dict = {}
    for color, rate in all_colors:
        if color in color_dict:
            color_dict[color] += rate
        else:
            color_dict[color] = rate

    return sorted(color_dict.items(), key=lambda x: x[1], reverse=True)

if __name__ == "__main__":
    video_file = "zoo.mp4"
    colors = process_video_for_colors(video_file, saving_fps=2, resize=900, tolerance=0, limit=100)

    print("Extracted Colors:")
    for color, occurrence in colors:
        print(f"{color}: {occurrence}")
