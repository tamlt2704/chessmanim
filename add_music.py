import subprocess
import sys

def add_background_music(video_path, audio_path, output_path, volume=0.3):
    """
    Add background music to a video file.
    
    Args:
        video_path: Path to the input video file
        audio_path: Path to the background music (mp3/wav)
        output_path: Path for the output video with music
        volume: Volume level for background music (0.0 to 1.0)
    """
    
    # FFmpeg command to add background music
    # -i: input files
    # -filter_complex: audio mixing with volume adjustment
    # -c:v copy: copy video without re-encoding (faster)
    # -c:a aac: encode audio as AAC
    # -shortest: end when shortest input ends
    
    command = [
        'ffmpeg',
        '-i', video_path,
        '-i', audio_path,
        '-filter_complex', f'[1:a]volume={volume}[a1];[0:a][a1]amix=inputs=2:duration=first[aout]',
        '-map', '0:v',
        '-map', '[aout]',
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-b:a', '192k',
        '-shortest',
        '-y',  # Overwrite output file if exists
        output_path
    ]
    
    print(f"Adding background music to video...")
    print(f"Video: {video_path}")
    print(f"Music: {audio_path}")
    print(f"Output: {output_path}")
    print(f"Volume: {volume}")
    
    try:
        subprocess.run(command, check=True)
        print(f"\nSuccess! Video with music saved to: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python add_music.py <video_file> <music_file> <output_file> [volume]")
        print("Example: python add_music.py video.mp4 music.mp3 output.mp4 0.3")
        sys.exit(1)
    
    video = sys.argv[1]
    music = sys.argv[2]
    output = sys.argv[3]
    volume = float(sys.argv[4]) if len(sys.argv) > 4 else 0.3
    
    add_background_music(video, music, output, volume)
