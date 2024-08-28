import os
import subprocess

# GLOBAL VARIABLES
INCOMING_VIDEO = 'incoming_videos/1_emerge4_reverse.mp4'
INCOMING_VIDEO = 'incoming_videos/5_walk4_last.mp4'


INCOMING_VIDEO = 'incoming_videos/walk5trimat2.mp4'

INCOMING_VIDEO = 'incoming_videos/pennyw/penny8.mp4'

TIME_TO_TRIM_VIDEO = 6  # seconds
OUTPUT_FOLDER = 'trim'

# Ensure the trim directory exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Get the base name of the incoming video without the extension
base_name = os.path.splitext(os.path.basename(INCOMING_VIDEO))[0]

# Create the output paths
trimmed_video_path = os.path.join(OUTPUT_FOLDER, f'{base_name}_trimmed_{TIME_TO_TRIM_VIDEO}s.mp4')
remaining_video_path = os.path.join(OUTPUT_FOLDER, f'{base_name}_remainder.mp4')

def run_ffmpeg_command(command):
    try:
        subprocess.run(command, check=True)
        print(f"Command {' '.join(command)} executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {' '.join(command)}")
        print(f"Error message: {e}")
        exit(1)

def get_video_duration(video_path):
    try:
        result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                                 '-of', 'default=noprint_wrappers=1:nokey=1', video_path],
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return float(result.stdout)
    except Exception as e:
        print(f"Error retrieving video duration: {e}")
        return None

def trim_video(input_path, output_path, duration):
    command = ['ffmpeg', '-i', input_path, '-t', str(duration), '-c', 'copy', output_path, '-y']
    run_ffmpeg_command(command)

def extract_remaining_video(input_path, output_path, start_time):
    command = ['ffmpeg', '-ss', str(start_time), '-i', input_path, '-c', 'copy', output_path, '-y']
    run_ffmpeg_command(command)

def process_video(input_video, trim_duration):
    print(f"Processing {input_video}...")

    # Get the total duration of the video
    total_duration = get_video_duration(input_video)
    if total_duration is None:
        print("Failed to get video duration.")
        return

    print(f"Total Video Duration: {total_duration} seconds")

    # Step 1: Trim the first part of the video
    print(f"Trimming the first {trim_duration} seconds...")
    trim_video(input_video, trimmed_video_path, trim_duration)
    print(f"Trimmed video saved as {trimmed_video_path}")

    # Step 2: Save the remaining part of the video
    print(f"Saving the remaining {total_duration - trim_duration} seconds...")
    extract_remaining_video(input_video, remaining_video_path, trim_duration)
    remaining_duration = total_duration - trim_duration
    new_remaining_video_path = os.path.join(OUTPUT_FOLDER, f'{base_name}_remainder_{int(remaining_duration)}s.mp4')

    # Remove the existing file if it exists before renaming
    if os.path.exists(new_remaining_video_path):
        os.remove(new_remaining_video_path)

    os.rename(remaining_video_path, new_remaining_video_path)
    print(f"Remaining video saved as {new_remaining_video_path}")

if __name__ == "__main__":
    process_video(INCOMING_VIDEO, TIME_TO_TRIM_VIDEO)