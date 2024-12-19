# vtt-to-text

A Python script to convert WebVTT subtitle files (.vtt) to plain text transcripts. Supports single file and batch directory processing.

## Features

- Convert single VTT files to plain text transcripts
- Batch process entire directories of VTT files
- Automatically removes HTML tags and timestamps
- Eliminates duplicate consecutive lines
- UTF-8 encoding support

## Usage

### Single File Conversion

```bash
python vtt_to_text.py input.vtt
```

This will create a text file with the same name as the input file (e.g., `input.txt`).

### Batch Directory Processing

```bash
python vtt_to_text.py -i /path/to/input/directory -o /path/to/output/directory
```

This will convert all .vtt files in the input directory and save the transcripts to the output directory.

## Command Line Arguments

- `input`: Path to a single input .vtt file (optional if -i is used)
- `-i, --input-path`: Path to the input directory containing multiple .vtt files
- `-o, --output-path`: Path to the output directory for transcript files (required when using -i)

## Example

```bash
# Convert a single file
python vtt_to_text.py subtitles.vtt

# Convert all VTT files in a directory
python vtt_to_text.py -i ./subtitles -o ./transcripts
```

## Error Handling

The script includes error handling for:

- File not found
- Directory not found
- Read/write permission issues
- Invalid file formats
