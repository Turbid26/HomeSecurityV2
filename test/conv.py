import os, subprocess

def convert_avi_to_mp4(avi_path):
    mp4_path = avi_path.replace('.avi', '.mp4')
    try:
        subprocess.run([
            "ffmpeg", "-i", avi_path,
            "-vcodec", "libx264", "-acodec", "aac",
            "-preset", "ultrafast", mp4_path
        ], check=True)
        print(f"[DEBUG] Successfully converted AVI to MP4: {mp4_path}")
        return mp4_path
    except Exception as e:
        print(f"[ERROR] Video conversion failed: {e}")
        return None

convert_avi_to_mp4("https://res.cloudinary.com/duhho2j3z/video/upload/v1748488260/HomeSec/Alerted/a%40gmail.com_recording.avi")