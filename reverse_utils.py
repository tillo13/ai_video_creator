import os
import subprocess

# Configuration
FILE_TO_REVERSE = 'trim/1_emerge4_reverse_remainder_8s.mp4'

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def reverse_video(input_path, output_path):
    try:
        subprocess.run(['ffmpeg', '-i', input_path, '-vf', "reverse", '-af', "areverse", output_path, '-y'], check=True)
        print(f"Video reversed and saved as {output_path}")
    except Exception as e:
        print(f"Error reversing video: {e}")

def main():
    input_filename = os.path.basename(FILE_TO_REVERSE)
    filename_wo_ext, ext = os.path.splitext(input_filename)
    output_directory = 'reversed_video'
    output_filename = f"{filename_wo_ext}_reversed{ext}"
    output_path = os.path.join(output_directory, output_filename)

    ensure_directory_exists(output_directory)
    reverse_video(FILE_TO_REVERSE, output_path)

if __name__ == "__main__":
    main()