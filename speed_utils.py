import os
import subprocess
import random

# Configuration
FILE_TO_MODIFY = 'incoming_videos/pennyw/penny12.mp4'

FILE_TO_MODIFY = 'reversed_video/penny1_reversed.mp4'

SPEED_TO_INCREASE = 0  # Speed up the video by this factor (e.g., 6 for 6x faster)
SPEED_TO_DECREASE = 1.57  # Slow down the video by this factor (e.g., 6 for 6x slower)
RANDOMIZE = 13  # Target duration for random speed changes (e.g., stretch/skew to 30 seconds)
MIN_SPEED = 0.5  # Minimum speed factor for randomization
MAX_SPEED = 15.0  # Maximum speed factor for randomization

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

def get_video_duration(video_path):
    try:
        result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 
                                 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', video_path],
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return float(result.stdout)
    except Exception as e:
        print(f"Error retrieving video duration: {e}")
        exit(1)

def reverse_video(input_path, output_path):
    try:
        command = ['ffmpeg', '-i', input_path, '-vf', 'reverse', '-an', output_path, '-y']
        run_ffmpeg_command(command)
        print(f"Video reversed and saved as {output_path}")
    except Exception as e:
        print(f"Error reversing video: {e}")

def modify_video_speed(input_path, output_path, speed_increase, speed_decrease):
    try:
        if speed_increase > 0:
            command = [
                'ffmpeg', '-i', input_path, '-vf', f"setpts={1.0/speed_increase}*PTS",
                '-an', output_path, '-y'
            ]
            run_ffmpeg_command(command)
            print(f"Video speed increased by {speed_increase}x and saved as {output_path}")
        elif speed_decrease > 0:
            command = [
                'ffmpeg', '-i', input_path, '-vf', f"setpts={speed_decrease}*PTS",
                '-an', output_path, '-y'
            ]
            run_ffmpeg_command(command)
            print(f"Video speed decreased by {speed_decrease}x and saved as {output_path}")
        else:
            print("Please set either SPEED_TO_INCREASE or SPEED_TO_DECREASE to a value greater than 0.")
            return
    except Exception as e:
        print(f"Error modifying video speed: {e}")

def randomize_video_speed(input_path, output_path, target_duration):
    original_duration = get_video_duration(input_path)
    
    if original_duration >= target_duration:
        randomize_long_video(input_path, output_path, target_duration)
    else:
        randomize_short_video(input_path, output_path, target_duration)

def randomize_long_video(input_path, output_path, target_duration):
    original_duration = get_video_duration(input_path)
    speed_factors = [random.uniform(MIN_SPEED, MAX_SPEED) for _ in range(10)]
    
    total_new_duration = sum(original_duration / speed for speed in speed_factors)
    time_scaler = target_duration / total_new_duration
    
    adjusted_speeds = [speed * time_scaler for speed in speed_factors]
    filters = []
    for i, speed in enumerate(adjusted_speeds):
        start_time = (original_duration * i) / len(speed_factors)
        segment_duration = original_duration / len(speed_factors)
        filters.append(f"[0:v]trim=start={start_time}:end={start_time + segment_duration},setpts=PTS*{1/speed}[v{i}]")

    filter_complex = ";".join(filters) + ";" + "".join([f"[v{i}]" for i in range(len(adjusted_speeds))]) + f"concat=n={len(adjusted_speeds)}:v=1:a=0[v]"

    command = [
        'ffmpeg', '-i', input_path, '-filter_complex', filter_complex, '-map', '[v]', '-t', str(target_duration), '-an', output_path, '-y'
    ]
    run_ffmpeg_command(command)

    print(f"Video randomized to fit duration {target_duration} seconds and saved as {output_path}")

def randomize_short_video(input_path, output_path, target_duration):
    original_duration = get_video_duration(input_path)
    temp_reversed_path = 'temp_reversed.mp4'
    reverse_video(input_path, temp_reversed_path)
    
    segments = []
    current_duration = 0
    
    while current_duration < target_duration:
        if random.choice([True, False]):
            segment_path = input_path
        else:
            segment_path = temp_reversed_path
        
        speed = random.uniform(MIN_SPEED, MAX_SPEED)
        segment_duration = original_duration / speed
        if current_duration + segment_duration > target_duration:
            segment_duration = target_duration - current_duration
        
        current_duration += segment_duration
        segments.append((segment_path, speed, segment_duration))
    
    filters = []
    for i, (seg_path, speed, duration) in enumerate(segments):
        filters.append(f"[{i}:v]setpts=PTS*{1/speed}[v{i}]")

    filter_complex = "".join([f"[v{i}]" for i in range(len(segments))]) + f"concat=n={len(segments)}:v=1:a=0[v]"

    inputs = []
    for i, (seg_path, _, _) in enumerate(segments):
        inputs.extend(['-i', seg_path])

    command = ['ffmpeg'] + inputs + ['-filter_complex', f"{';'.join(filters)};{filter_complex}", '-map', '[v]', '-t', str(target_duration), '-an', output_path, '-y']
    run_ffmpeg_command(command)
    
    os.remove(temp_reversed_path)
    
    print(f"Video randomized to fit duration {target_duration} seconds and saved as {output_path}")

def main():
    input_filename = os.path.basename(FILE_TO_MODIFY)
    filename_wo_ext, ext = os.path.splitext(input_filename)
    output_directory = 'sped_up'
    ensure_directory_exists(output_directory)
    
    if SPEED_TO_INCREASE > 0:
        output_filename = f"{filename_wo_ext}_speed_{SPEED_TO_INCREASE}x{ext}"
        output_path = os.path.join(output_directory, output_filename)
        modify_video_speed(FILE_TO_MODIFY, output_path, SPEED_TO_INCREASE, 0)
    elif SPEED_TO_DECREASE > 0:
        output_filename = f"{filename_wo_ext}_slow_{SPEED_TO_DECREASE}x{ext}"
        output_path = os.path.join(output_directory, output_filename)
        modify_video_speed(FILE_TO_MODIFY, output_path, 0, SPEED_TO_DECREASE)
    elif RANDOMIZE > 0:
        output_filename = f"{filename_wo_ext}_randomized{ext}"
        output_path = os.path.join(output_directory, output_filename)
        randomize_video_speed(FILE_TO_MODIFY, output_path, RANDOMIZE)
    else:
        print("Please set either SPEED_TO_INCREASE, SPEED_TO_DECREASE, or RANDOMIZE to a value greater than 0.")

if __name__ == "__main__":
    main()