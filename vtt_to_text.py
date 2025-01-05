"""Script to convert VTT subtitle files to plain text transcripts."""

import argparse
import re
import os
from itertools import groupby


def vtt_to_transcript(vtt_file_path):
    """
    Converts a VTT subtitle file to a plain text transcript using regex.

    Args:
        vtt_file_path (str): The path to the input .vtt file.

    Returns:
        str: The plain text transcript, or None if an error occurs.
    """
    try:
        with open(vtt_file_path, "r", encoding="utf-8") as file:
            content = file.read()
    except FileNotFoundError:
        print(f"Error: File not found at {vtt_file_path}")
        return None
    except Exception as e:  # pylint: disable=broad-except
        print(f"Error reading file: {e}")
        return None

    # Remove header (more robust)
    content = re.sub(
        r"^.*?(\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}).*?\n",
        r"\1",
        content,
        flags=re.DOTALL,
    )

    # Extract text lines, removing timestamps and HTML tags
    lines = []
    for line in content.splitlines():
        if re.match(r"^\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}", line):
            continue  # Skip timestamp lines
        line = re.sub(r"<[^>]+>", "", line)  # Remove HTML tags
        line = line.strip()
        if line:
            lines.append(line)

    # Remove consecutive duplicate lines
    unique_lines = [k for k, _ in groupby(lines)]

    transcript = " ".join(unique_lines)
    return transcript


def process_directory(input_dir, output_dir):
    """
    Processes all VTT files in the input directory and saves transcripts to the output directory.

    Args:
        input_dir (str): The path to the input directory.
        output_dir (str): The path to the output directory.
    """
    if not os.path.isdir(input_dir):
        print(f"Error: Input directory not found: {input_dir}")
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".vtt"):
            input_file_path = os.path.join(input_dir, filename)
            output_file_name = os.path.splitext(filename)[0] + ".txt"
            output_file_path = os.path.join(output_dir, output_file_name)

            transcript = vtt_to_transcript(input_file_path)
            if transcript:
                try:
                    with open(output_file_path, "w", encoding="utf-8") as f:
                        f.write(transcript)
                    print(f"Transcript saved to {output_file_path}")
                except Exception as e:  # pylint: disable=broad-except
                    print(f"Error writing to file: {e}")


def main():
    """
    Parses command-line arguments and executes the VTT to transcript conversion.
    """
    parser = argparse.ArgumentParser(
        description="Convert VTT subtitle file(s) to plain text transcript(s)."
    )
    parser.add_argument(
        "input", nargs="?", help="Path to the input .vtt file (optional if -i is used)"
    )
    parser.add_argument(
        "-i",
        "--input-path",
        help="Path to the input directory containing multiple .vtt files",
    )
    parser.add_argument(
        "-o",
        "--output-path",
        dest="output_dir",
        help="Path to the output directory for transcript files (required if -i is used)",
    )

    args = parser.parse_args()

    if args.input_path:
        if not args.output_dir:
            parser.error(
                "-o/--output-path must be specified if -i/--input-path is used"
            )
        process_directory(args.input_path, args.output_dir)
    elif args.input:
        transcript = vtt_to_transcript(args.input)
        if transcript:
            output_file_name = os.path.splitext(args.input)[0] + ".txt"
            output_file_path = os.path.join(
                os.path.dirname(args.input), output_file_name
            )
            try:
                with open(output_file_path, "w", encoding="utf-8") as f:
                    f.write(transcript)
                print(f"Transcript saved to {output_file_path}")
            except Exception as e:  # pylint: disable=broad-except
                print(f"Error writing to file: {e}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
