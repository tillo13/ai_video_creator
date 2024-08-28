import os
import re
import subprocess

# Define the directory containing the video files
VIDEO_DIR = 'prod'
OUTPUT_FILENAME = 'final_video.mp4'

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def create_concat_file(videos, concat_file_path):
    with open(concat_file_path, 'w') as f:
        for video in videos:
            # Write the relative path of each video file
            relative_video_path = os.path.relpath(video, start=VIDEO_DIR)
            f.write(f"file '{relative_video_path}'\n")
    print(f"Concat file created at {concat_file_path}")

def concatenate_videos(video_list, output_path):
    try:
        # File to store the list of videos to concatenate
        concat_file = os.path.join(VIDEO_DIR, 'videos_to_concat.txt')
        
        # Create list of files inside the concat file
        create_concat_file(video_list, concat_file)
        
        # Run ffmpeg to concatenate the videos
        subprocess.run(['ffmpeg', '-f', 'concat', '-safe', '0', '-i', concat_file, '-c', 'copy', output_path, '-y'], check=True)
        print(f"Videos concatenated and saved as {output_path}")
        
        # Clean up
        os.remove(concat_file)
        
    except Exception as e:
        print(f"Error concatenating videos: {e}")

def get_sorted_video_files(directory):
    video_extensions = {'.mp4', '.avi', '.mov'}
    files = [
        os.path.join(directory, f) 
        for f in os.listdir(directory) 
        if os.path.isfile(os.path.join(directory, f)) and os.path.splitext(f)[1].lower() in video_extensions and re.match(r'^\d', f)
    ]
    
    def numeric_sort_key(file):
        base_name = os.path.basename(file)
        numbers = re.findall(r'\d+', base_name)
        return [int(num) for num in numbers]

    files.sort(key=numeric_sort_key)
    return files

def main():
    video_files = get_sorted_video_files(VIDEO_DIR)
    output_path = os.path.join(VIDEO_DIR, OUTPUT_FILENAME)

    ensure_directory_exists(VIDEO_DIR)
    concatenate_videos(video_files, output_path)

if __name__ == "__main__":
    main()