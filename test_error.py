import yt_dlp
import imageio_ffmpeg
import os
import subprocess

ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
desktop = os.path.join(os.path.expanduser("~"), "Desktop")

ydl_opts = {
    'outtmpl': os.path.join(desktop, '%(title)s.%(ext)s'),
    'ffmpeg_location': ffmpeg_path,
    'quiet': False,
    'noplaylist': True,
    'restrictfilenames': True,
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'postprocessor_args': {
        'default': [
            '-codec:a', 'libmp3lame',
            '-ar', '44100',
            '-ac', '2',
            '-b:a', '192k',
            '-joint_stereo', '1',
            '-id3v2_version', '3',
            '-map_metadata', '-1'
        ]
    }
}

print("=== Downloading... ===")
yt_dlp.YoutubeDL(ydl_opts).download(['https://youtu.be/oPQ3o14ksaM'])

# Verify
mp3_file = os.path.join(desktop, "Sean_Paul_-_Get_Busy_Like_Glue_Official_Video.mp3")
if os.path.exists(mp3_file):
    print("\n=== VERIFYING MP3 ===")
    result = subprocess.run(
        [ffmpeg_path, '-i', mp3_file],
        capture_output=True, encoding='utf-8', errors='replace'
    )
    for line in result.stderr.split('\n'):
        if 'Audio:' in line or 'Duration:' in line:
            print(line.strip())
    
    size_mb = os.path.getsize(mp3_file) / (1024*1024)
    print(f"File size: {size_mb:.2f} MB")
    print(f"File name: {os.path.basename(mp3_file)}")
    print("=== VERIFICATION COMPLETE ===")
