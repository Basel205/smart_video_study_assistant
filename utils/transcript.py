from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import re

def extract_video_id(youtube_url: str) -> str:
    # Supports various YouTube URL formats
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(pattern, youtube_url)
    if not match:
        raise ValueError("Invalid YouTube URL format")
    return match.group(1)

def get_transcript(video_url: str):
    video_id = extract_video_id(video_url)
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
    except Exception as e:
        return None, f"Transcript not available or error: {str(e)}"
    
    return transcript, None
