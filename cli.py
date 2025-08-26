import argparse
import logging
from captions import get_captions
from chapters import split_into_chapters_by_topic
from titles import generate_chapter_title
from utils import format_timestamp
from rich.console import Console
from rich.table import Table


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(
        description="Generate YouTube chapter titles for a YouTube video"
    )
    parser.add_argument(
        "--video_id", type=str, required=True, help="The YouTube video ID"
    )
    parser.add_argument(
        "--language", type=str, default="en", help="Caption language (default: en)"
    )
    parser.add_argument(
        "--group-size",
        type=int,
        default=10,
        help="Number of captions per group (default: 10)",
    )
    parser.add_argument(
        "--similarity-threshold",
        type=float,
        default=0.1,
        help="Chapter segmentation threshold (default: 0.1)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="console",
        choices=["console"],
        help="Output format (default: console)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="OpenAI deployment/model name (optional)",
    )
    args = parser.parse_args()

    captions = get_captions(args.video_id, language=args.language)
    chapters = split_into_chapters_by_topic(
        captions, group_size=args.group_size, threshold=args.similarity_threshold
    )
    logging.info(f"Found {len(chapters)} chapters")

    table = Table(title="", show_header=True, header_style="bold magenta", box=None)
    table.add_column("Timestamp", style="cyan")
    table.add_column("Title", style="magenta")

    for chapter in chapters:
        timestamp = format_timestamp(chapter[0][1])
        title = generate_chapter_title(chapter, model=args.model)
        table.add_row(timestamp, title)

    if args.output == "console":
        console = Console()
        console.print(table)
