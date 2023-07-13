import openai
import os
import argparse
from youtube_transcript_api import YouTubeTranscriptApi

def format_timestamp(seconds):
    # Convert seconds to mm:ss format
    minutes, seconds = divmod(seconds, 60)
    return f"{int(minutes):02d}:{int(seconds):02d}"


def get_captions(video_id):
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    transcript = transcript_list.find_transcript(['en'])
    return [(t['text'], t['start']) for t in transcript.fetch()]


def split_into_chapters(captions, num_chapters):
    # Split the captions into num_chapters chapters
    captions_per_chapter = len(captions) // num_chapters
    return [captions[i:i+captions_per_chapter] for i in range(0, len(captions), captions_per_chapter)]


def generate_chapter_title(chapter):

    prompt = f"The following text needs a title: {' '.join(text for text, _ in chapter)}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"{prompt}"}
        ]
    )
    return response['choices'][0]['message']['content']


def generate_chapter_titles(video_id, num_chapters):

    openai.api_key = os.getenv('OPENAI_API_KEY')
    # Get the captions for the video
    captions = get_captions(video_id)

    # Split the captions into chapters
    chapters = split_into_chapters(captions, num_chapters)

    # Generate a title for each chapter
    titles = [(format_timestamp(chapter[0][1]), generate_chapter_title(chapter)) for chapter in chapters]

    return titles


def main():
    parser = argparse.ArgumentParser(
        description='Generate YouTube chapter titles for a YouTube video')
    parser.add_argument('video_id', type=str, help='The YouTube video ID')
    parser.add_argument('num_chapters', type=int,
                        help='The number of chapters to generate')
    args = parser.parse_args()

    titles = generate_chapter_titles(args.video_id, args.num_chapters)
    for i, (time,title) in enumerate(titles):
        print(f"{time}: {title}")


if __name__ == '__main__':
    main()
