# Repo Summarizer (Python Version)

A CLI tool to summarize files in a directory using OpenAI.

## Installation

### Step 1: Set up a virtual environment (recommended)

```bash
cd repo-summarizer-py
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 2: Install dependencies

```bash
pip install -r requirements.txt
pip install -e .
```

**Note:** To deactivate the virtual environment when you're done, run `deactivate`.

## Usage

```bash
repo-summarizer -d /path/to/directory -k your_openai_api_key
```

### Options

- `-d, --directory` (required): Directory to process
- `-o, --output`: Output JSON file path
- `-k, --api-key`: OpenAI API key (or set OPENAI_API_KEY env var)
- `-l, --log-level`: Log level (debug, info, warn, error) [default: info]
- `-m, --model`: OpenAI model to use [default: gpt-3.5-turbo]

### Environment Variables

You can set the OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY="your_api_key_here"
repo-summarizer -d /path/to/directory
```

## Example

```bash
# Summarize files and output to console
repo-summarizer -d ./test-files -k sk-your-api-key

# Summarize files and save to JSON file
repo-summarizer -d ./test-files -o summary.json -k sk-your-api-key

# Use environment variable for API key
export OPENAI_API_KEY="sk-your-api-key"
repo-summarizer -d ./test-files -o summary.json
```

## Features

- Processes text files in a directory
- Generates AI-powered summaries using OpenAI
- Supports multiple file formats (js, ts, py, md, txt, etc.)
- JSON output with file metadata
- Configurable logging levels
- Error handling and connection testing

## Requirements

- Python 3.8+
- OpenAI API key
- Internet connection
