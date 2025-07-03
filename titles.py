import os
import logging
from typing import List, Tuple
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

def generate_chapter_title(chapter: List[Tuple[str, float]]) -> str:
    chapter_content = ' '.join(text for text, _ in chapter)
    prompt = (
        "I need a chapter title for a segment of a YouTube video. "
        "This particular segment covers the following content: "
        f"{chapter_content}. "
        "The title should be no more than 6 words and describe the segment concisely and accurately."
    )
    try:
        completion = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        logging.error(f"Error generating chapter title: {e}")
        return "Untitled Chapter" 