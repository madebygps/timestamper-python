import os
import argparse
from youtube_transcript_api import YouTubeTranscriptApi
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from dotenv import load_dotenv
from openai import AzureOpenAI
from rich.console import Console
from rich.table import Table

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')
deployment = os.getenv('DEPLOYMENT_NAME')
endpoint = os.getenv('ENDPOINT')

client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_version="2024-05-01-preview",
    api_key=openai_api_key
)  

def format_timestamp(seconds):
    """
    Formats the given number of seconds into a timestamp string.

    Args:
        seconds (int): The number of seconds to be formatted.

    Returns:
        str: The formatted timestamp string in the format "hh:mm:ss" or "mm:ss".
    """
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)

    if hours > 0:
        return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
    else:
        return f"{int(minutes):02d}:{int(seconds):02d}"

def get_captions(video_id):
    """
    Retrieves the captions and corresponding start times for a given YouTube video.

    Args:
        video_id (str): The ID of the YouTube video.

    Returns:
        list: A list of tuples containing the caption text and start time for each caption.
    """
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    transcript = transcript_list.find_transcript(['en'])
    return [(t['text'], t['start']) for t in transcript.fetch()]

def generate_chapter_title(chapter):
    """
    Generates a chapter title for a segment of a YouTube video based on the given chapter content.

    Args:
        chapter (list): A list of tuples representing the content of the chapter. Each tuple contains
                        a text segment and its corresponding timestamp.

    Returns:
        str: The generated chapter title.
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
            model=deployment,  # Specify GPT-4 model here
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

def group_sentences(captions, num_chapters):
    """
    Groups the captions into sentences based on the specified group size.

    Args:
        captions (list): A list of tuples containing the caption text and start time.
        group_size (int, optional): The number of captions to group together. Defaults to 7.

    Returns:
        list: A list of tuples containing the grouped caption text and start time.
    """
    grouped_captions = []
    for i in range(0, len(captions), num_chapters):
        grouped_text = ' '.join(text for text, _ in captions[i:i+num_chapters])
        start_time = captions[i][1]
        grouped_captions.append((grouped_text, start_time))
    return grouped_captions

def split_into_chapters_by_topic(captions):
    """
    Splits a list of captions into chapters based on topic similarity.

    Args:
        captions (list): A list of captions representing sentences.
        threshold (float, optional): The similarity threshold for determining chapter breakpoints. Defaults to 0.1.
        group_size (int, optional): The number of captions to group together. Defaults to 20.

    Returns:
        list: A list of chapters, where each chapter is a list of captions.
    """
    
    group_size = 10
    grouped_captions = group_sentences(captions, group_size)
    threshold=0.1

    vectorizer = TfidfVectorizer()
    texts = [text for text, _ in grouped_captions]
    X = vectorizer.fit_transform(texts)

    sim_matrix = cosine_similarity(X)

    breakpoints = [0]
    for i in range(1, len(sim_matrix)):
        if sim_matrix[i-1][i] < threshold:
            breakpoints.append(i)

    breakpoints.append(len(sim_matrix))

    chapters = [grouped_captions[breakpoints[i]:breakpoints[i+1]] for i in range(len(breakpoints)-1)]

    return chapters

def generate_chapter_titles(video_id):
    """
    Generates chapter titles for a given video based on its captions.

    Args:
        video_id (str): The ID of the video.

    Returns:
        list: A list of tuples containing the formatted timestamps and generated chapter titles.
    """
    captions = get_captions(video_id)
    chapters = split_into_chapters_by_topic(captions)
    print(f"Found {len(chapters)} chapters")
    
    table = Table(title="", show_header=True, header_style="bold magenta")
    table.add_column("Timestamp", style="cyan") 
    table.add_column("Title", style="magenta")  
    
    for chapter in chapters:
        timestamp = format_timestamp(chapter[0][1])
        title = generate_chapter_title(chapter)
        table.add_row(timestamp, title)
    
    console = Console()
    console.print(table)
   

def main():
    parser = argparse.ArgumentParser(
        description='Generate YouTube chapter titles for a YouTube video')
    parser.add_argument('--video_id', type=str, help='The YouTube video ID')
    args = parser.parse_args()

    generate_chapter_titles(args.video_id)
    

if __name__ == '__main__':
    main()