import os
import logging
from typing import List, Tuple, Optional
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
deployment = os.getenv('DEPLOYMENT_NAME')
endpoint = os.getenv('ENDPOINT')

client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_version="2024-05-01-preview",
    api_key=openai_api_key
)

def generate_chapter_title(chapter: List[Tuple[str, float]], model: Optional[str] = None) -> str:
    """
    Generate a chapter title for a segment of a YouTube video using OpenAI.
    Args:
        chapter: List of (text, timestamp) tuples for the chapter.
        model: Optional model/deployment name to use.
    Returns:
        str: Generated chapter title.
    """
    chapter_content = ' '.join(text for text, _ in chapter)
    prompt = (
        "I need a chapter title for a segment of a YouTube video. "
        "This particular segment covers the following content: "
        f"{chapter_content}. "
        "The title should be no more than 6 words and describe the segment concisely and accurately."
    )
    try:
        completion = client.chat.completions.create(
            model=model or deployment,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        logging.error(f"Error generating chapter title: {e}")
        return "Untitled Chapter" 