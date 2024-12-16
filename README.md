# Video Color Palette Extractor

This repository contains two Python scripts designed to work with video files:

1. **Color Palette Extractor**: Extracts the most common color palette from a video by analyzing its frames.
2. **Frame Extractor**: Extracts individual frames from a video file at a specified interval.

---

## Features

### 1. **Color Palette Extractor**
- Extracts the dominant colors from frames of a video.
- Configurable frame extraction rate (frames per second).
- Adjustable image resizing, color tolerance, and the number of colors to extract.
- Outputs a sorted list of colors by occurrence.

### 2. **Frame Extractor**
- Extracts and saves frames from a video.
- Configurable frame extraction rate (frames per second).
- Outputs images to a designated directory.

---

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/DNSINED/Video_Color_Palette_Extractor.git
    cd Video_Color_Palette_Extractorr
    ```

2. Install the required Python libraries:
    ```bash
    pip install -r requirements.txt
    ```

### Required Libraries:
- `opencv-python`
- `numpy`
- `extcolors`
- `colormap`
- `Pillow`

---

## Usage

### **1. Color Palette Extractor**

Run the script to extract the dominant color palette from a video:
```bash
python colors_extractor.py
```

#### **Parameters:**
- `video_file`: Path to the input video file.
- `saving_fps`: Number of frames to analyze per second (default: `2`).
- `resize`: Width to resize frames for analysis (default: `900`).
- `tolerance`: Tolerance for color extraction (default: `0`).
- `limit`: Maximum number of colors to extract (default: `100`).

### **2. Frame Extractor**

Run the frame extraction script:
```bash
python frame_extractor.py
```

#### **Parameters:**
- `video_file`: Path to the input video file.
- `saving_fps`: Number of frames to save per second (default: `1`).

---

## Output

1. **Color Palette Extractor**:
   - Prints a sorted list of hex color codes with their occurrence rates.
   - Example output:
     ```
     Extracted Colors:
     #ffffff: 45
     #000000: 30
     #ff5733: 15
     ```

2. **Frame Extractor**:
   - Saves extracted frames as `.jpg` images in a new directory named `<video_file>_frames`.

---

## Example

### Extracting the Most Common Colors:
```bash
python colors_extractor.py
```
Input:
- A video file named `zoo.mp4`

Output:
- A list of the most common colors in the video frames.

### Extracting Frames from a Video:
```bash
python frame_extractor.py
```
Input:
- A video file named `zoo.mp4`

Output:
- A directory named `zoo_frames` containing `.jpg` images of the extracted frames.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Acknowledgments

- [Pillow (PIL)](https://python-pillow.org/)
- [OpenCV](https://opencv.org/)
- [extcolors](https://pypi.org/project/extcolors/)
- [colormap](https://pypi.org/project/colormap/)
