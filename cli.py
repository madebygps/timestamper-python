import argparse
import logging
from captions import get_captions
from chapters import split_into_chapters_by_topic
from titles import generate_chapter_title
from utils import format_timestamp
from rich.console import Console
from rich.table import Table
from typing import Optional

def main() -> None:
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description='Generate YouTube chapter titles for a YouTube video')
    parser.add_argument('--video_id', type=str, required=True, help='The YouTube video ID')
    args = parser.parse_args()

    captions = get_captions(args.video_id)
    chapters = split_into_chapters_by_topic(captions)
    logging.info(f"Found {len(chapters)} chapters")

    table = Table(title="", show_header=True, header_style="bold magenta", box=None)
    table.add_column("Timestamp", style="cyan")
    table.add_column("Title", style="magenta")

    for chapter in chapters:
        timestamp = format_timestamp(chapter[0][1])
        title = generate_chapter_title(chapter)
        table.add_row(timestamp, title)

    console = Console()
    console.print(table) 