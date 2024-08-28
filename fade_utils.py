import os
import subprocess

# Configuration
VIDEO_TO_EDIT = 'incoming_videos/pennyw/penny2.mp4'

START_TO_FADE = 8  # Start fading out to black at 8 seconds
EMERGE_FROM_FADE = 0  # Start emerging from black until 3 seconds in. If > 0, this takes precedence over START_TO_FADE.

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def run_ffmpeg_command(command):
    try:
        subprocess.run(command, check=True)
        print(f"Command '{' '.join(command)}' executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {' '.join(command)}")
        print(f"Error message: {e}")
        exit(1)

def fade_out_to_black(input_path, output_path, start_time):
    duration = get_video_duration(input_path)
    fade_duration = duration - start_time
    command = [
        'ffmpeg', '-i', input_path, '-vf', f"fade=t=out:st={start_time}:d={fade_duration}", 
        '-af', f"afade=t=out:st={start_time}:d={fade_duration}", output_path, '-y'
    ]
    run_ffmpeg_command(command)

def fade_in_from_black(input_path, output_path, fade_duration):
    command = [
        'ffmpeg', '-i', input_path, '-vf', f"fade=t=in:st=0:d={fade_duration}", 
        '-af', f"afade=t=in:st=0:d={fade_duration}", output_path, '-y'
    ]
    run_ffmpeg_command(command)

def get_video_duration(video_path):
    try:
        result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 
                                 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', video_path],
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return float(result.stdout)
    except Exception as e:
        print(f"Error retrieving video duration: {e}")
        exit(1)

def process_video(video_path, start_to_fade, emerge_from_fade):
    output_directory = 'fade'
    ensure_directory_exists(output_directory)
    
    video_basename = os.path.basename(video_path)
    filename_wo_ext, ext = os.path.splitext(video_basename)
    
    if emerge_from_fade > 0:
        output_path = os.path.join(output_directory, f"{filename_wo_ext}_fadein{ext}")
        fade_in_from_black(video_path, output_path, emerge_from_fade)
    elif start_to_fade > 0:
        output_path = os.path.join(output_directory, f"{filename_wo_ext}_fadeout{ext}")
        fade_out_to_black(video_path, output_path, start_to_fade)
    else:
        print("Please set either START_TO_FADE or EMERGE_FROM_FADE to a value greater than 0.")
        return
    
    print(f"Processed video saved as {output_path}")

def main():
    process_video(VIDEO_TO_EDIT, START_TO_FADE, EMERGE_FROM_FADE)

if __name__ == "__main__":
    main()