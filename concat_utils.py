import os
import subprocess

# Configuration
VIDEO_1 = 'trim/1_emerge4_reverse_trimmed_2s.mp4'
VIDEO_2 = 'sped_up/1_emerge4_reverse_remainder_8s_1_emerge4_reverse_concat_speed_3x.mp4'

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def create_concat_file(videos, concat_file_path):
    with open(concat_file_path, 'w') as f:
        for video in videos:
            f.write(f"file '{video}'\n")

def concatenate_videos(video1, video2, output_path):
    try:
        # File to store the list of videos to concatenate
        concat_file = 'videos_to_concat.txt'
        
        # Create list of files inside the concat file
        create_concat_file([video1, video2], concat_file)
        
        # Run ffmpeg to concatenate the videos
        subprocess.run(['ffmpeg', '-f', 'concat', '-safe', '0', '-i', concat_file, '-c', 'copy', output_path, '-y'], check=True)
        print(f"Videos concatenated and saved as {output_path}")
        
        # Clean up
        os.remove(concat_file)
        
    except Exception as e:
        print(f"Error concatenating videos: {e}")

def main():
    video1_filename = os.path.basename(VIDEO_1)
    video2_filename = os.path.basename(VIDEO_2)
    filename_wo_ext1, ext1 = os.path.splitext(video1_filename)
    filename_wo_ext2, ext2 = os.path.splitext(video2_filename)
    output_directory = 'concat_files'
    output_filename = f"{filename_wo_ext1}_{filename_wo_ext2}_concat{ext1}"
    output_path = os.path.join(output_directory, output_filename)

    ensure_directory_exists(output_directory)
    concatenate_videos(VIDEO_1, VIDEO_2, output_path)

if __name__ == "__main__":
    main()