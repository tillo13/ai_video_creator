import os
import subprocess
import json

# File paths
VIDEO_FILE = 'prod/final_video.mp4'
AUDIO_TO_ADD = 'incoming_videos/pennyw/into_the_darkness.mp3'

# Fade out duration for the audio (in seconds)
FADE_AUDIO_REMAINING_SECONDS = 8

def get_media_duration(file_path):
    """Gets the duration of a media file using ffprobe."""
    command = [
        'ffprobe', 
        '-v', 'error', 
        '-show_entries', 'format=duration', 
        '-of', 'default=noprint_wrappers=1:nokey=1', 
        file_path
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return float(result.stdout.strip())

def adjust_audio_length(video_duration, audio_path):
    adjusted_audio_path = 'temp_adjusted_audio.mp3'
    fade_audio_length = video_duration - FADE_AUDIO_REMAINING_SECONDS
    command = [
        'ffmpeg', 
        '-i', audio_path, 
        '-filter_complex', f"afade=t=out:st={fade_audio_length}:d={FADE_AUDIO_REMAINING_SECONDS},loop=loop=-1:size=44100,start=0", 
        '-t', str(video_duration), 
        '-y',
        adjusted_audio_path
    ]
    subprocess.run(command, check=True)
    return adjusted_audio_path

def overlay_audio_on_video(video_path, audio_path, output_path):
    command = [
        'ffmpeg', 
        '-i', video_path, 
        '-i', audio_path, 
        '-c:v', 'copy', 
        '-map', '0:v:0', 
        '-map', '1:a:0', 
        '-shortest', 
        '-y',
        output_path
    ]
    subprocess.run(command, check=True)

def main():
    video_duration = get_media_duration(VIDEO_FILE)
    audio_duration = get_media_duration(AUDIO_TO_ADD)
    
    if audio_duration < video_duration:
        adjusted_audio_path = adjust_audio_length(video_duration, AUDIO_TO_ADD)
    else:
        fade_audio_length = video_duration - FADE_AUDIO_REMAINING_SECONDS
        command = [
            'ffmpeg', 
            '-i', AUDIO_TO_ADD, 
            '-filter_complex', f"afade=t=out:st={fade_audio_length}:d={FADE_AUDIO_REMAINING_SECONDS}", 
            '-t', str(video_duration), 
            '-y',
            'temp_adjusted_audio.mp3'
        ]
        subprocess.run(command, check=True)
        adjusted_audio_path = 'temp_adjusted_audio.mp3'

    output_file = 'prod/final_video_with_audio.mp4'
    overlay_audio_on_video(VIDEO_FILE, adjusted_audio_path, output_file)
    os.remove(adjusted_audio_path)
    print(f"Final video with audio saved as {output_file}")

if __name__ == "__main__":
    main()