import logging
from youtube_transcript_api import YouTubeTranscriptApi
from typing import List, Tuple


def get_captions(video_id: str, language: str = "en") -> List[Tuple[str, float]]:
    """
    Retrieves the captions and corresponding start times for a given YouTube video.
    Args:
        video_id (str): The ID of the YouTube video.
        language (str): The language code for captions.
    Returns:
        list: A list of tuples containing the caption text and start time for each caption.
    """
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcript_list.find_transcript([language])
        return [(t["text"], t["start"]) for t in transcript.fetch()]
    except Exception as e:
        logging.error(f"Error fetching captions: {e}")
        return []
