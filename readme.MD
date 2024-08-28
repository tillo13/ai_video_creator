# 🚀 AI Video Processing Pipeline

This project is ensemble of Python utility scripts designed to take your raw video content and transform it into a polished masterpiece leveraging the power of some slick AI tools, this pipeline integrates:

- **Flux**: For generating the main images that will captivate your audience.
- **Civitai with Phlux Lora**: To enhance and refine images to perfection.
- **RunwayML**: An AI video creator that brings still images to life with stunning motion graphics.
- **Suno.ai**: For crafting impeccable audio that syncs flawlessly with your visuals.

## Abilities
1. **Trimming** videos.
2. **Reversing** videos.
3. **Modifying speed** of videos.
4. **Adding fade-in and fade-out effects** to videos.
5. **Concatenating** video files.
6. **Adding audio** to the final video product.

The scripts work together to prepare your video files and place them in a production folder (`prod/`) before finalizing the video (`finalize_prod.py`) and adding audio (`add_audio.py`).

## Dependencies

Ensure you have [FFmpeg](https://ffmpeg.org/) installed on your system.

## Directory Structure

```plaintext
project/
│
├── prod/
│   ├── final_video.mp4
|   └── final_video_with_audio.mp4
├── trim/
│   ├── 1_emerge4_reverse_trimmed_2s.mp4
│   └── 1_emerge4_reverse_remainder_8s.mp4
├── sped_up/
│   └── 1_emerge4_reverse_remainder_8s_1_emerge4_reverse_concat_speed_3x.mp4
├── reversed_video/
│   └── 1_emerge4_reverse_remainder_8s_reversed.mp4
├── incoming_videos/
|   └── pennyw/
|       ├── penny2.mp4
|       ├── into_the_darkness.mp3
|       └── penny12.mp4
|
├── fade/
|   ├── penny2_fadein.mp4
│   └── penny2_fadeout.mp4
|
├── concat_files/
|   └── 12_penny13_13_penny13_reversed_speed_13x_concat.mp4
|
├── add_audio.py
├── concat_utils.py
├── fade_utils.py
├── finalize_prod.py
├── reverse_utils.py
├── speed_utils.py
└── trimmer_utils.py
```

## Installation
Clone the repository and navigate to the project directory:

git clone <repository-url>
cd project

## Usage
Follow the steps below to process and finalize your video project.

Step 1: Trim Video
Use trimmer_utils.py to trim a specified duration from the start of a video.

python trimmer_utils.py
Step 2: Reverse Video
Use reverse_utils.py to reverse a video.

python reverse_utils.py
Step 3: Modify Video Speed
Use speed_utils.py to increase, decrease, or randomize the speed of a video.

python speed_utils.py
Step 4: Add Fade-in/Fade-out Effects
Use fade_utils.py to add fade-in or fade-out effects to a video.

python fade_utils.py
Step 5: Concatenate Videos
Use concat_utils.py to concatenate multiple video files into a single video.

python concat_utils.py
Step 6: Finalize Production Video
Use finalize_prod.py to gather all processed video segments placed in the prod/ directory and concatenate them into the final video.

python finalize_prod.py
Step 7: Add Audio to Final Video
Use add_audio.py to overlay audio onto the final video file.

python add_audio.py
This will generate final_video_with_audio.mp4 in the prod/ directory.

[![Demo Video](https://img.youtube.com/vi/_SfW1ouFZ7Q/0.jpg)](https://www.youtube.com/watch?v=_SfW1ouFZ7Q)
