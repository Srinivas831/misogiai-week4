from moviepy.editor import VideoFileClip

def extract_audio_from_video(video_path: str, output_audio_path: str) -> str:
    try:
        video = VideoFileClip(video_path)
        print("video",video)
        audio = video.audio
        print("audio",audio)
        audio.write_audiofile(output_audio_path)
        return output_audio_path
    except Exception as e:
        print(f"Error extracting audio from video: {e}")
        return None
