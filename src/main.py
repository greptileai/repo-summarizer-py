#!/usr/bin/env python3

import asyncio
import json
import os
import sys
import time
from typing import Optional

import click

from .file_processor import FileProcessor
from .summarizer import FileSummarizer
from .logger import Logger
from .types import SummarizerOptions, ProcessorOptions, SummaryResult


@click.command()
@click.option('-d', '--directory', required=True, help='Directory to process')
@click.option('-o', '--output', help='Output JSON file path')
@click.option('-k', '--api-key', help='OpenAI API key (or set OPENAI_API_KEY env var)')
@click.option('-l', '--log-level', default='info', help='Log level (debug, info, warn, error)')
@click.option('-m', '--model', default='gpt-3.5-turbo', help='OpenAI model to use')
@click.version_option(version='1.0.0')
def main(directory: str, output: Optional[str], api_key: Optional[str], log_level: str, model: str):
    """Summarize files in a directory using OpenAI"""
    asyncio.run(_main(directory, output, api_key, log_level, model))


async def _main(directory: str, output: Optional[str], api_key: Optional[str], log_level: str, model: str):
    logger = Logger(log_level)

    try:
        # Get API key from option or environment
        final_api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not final_api_key:
            logger.error('OpenAI API key is required. Use --api-key or set OPENAI_API_KEY environment variable.')
            sys.exit(1)

        logger.info('Initializing summarizer...')
        summarizer_options = SummarizerOptions(
            api_key=final_api_key,
            model=model
        )
        summarizer = FileSummarizer(summarizer_options, logger)

        # Test OpenAI connection
        connection_test = await summarizer.test_connection()
        if not connection_test:
            logger.error('Failed to connect to OpenAI API')
            sys.exit(1)

        processor = FileProcessor(summarizer, logger)

        start_time = time.time()

        processor_options = ProcessorOptions(
            directory=directory,
            log_level=log_level
        )
        summaries = await processor.process_directory(processor_options)

        end_time = time.time()
        processing_time = int((end_time - start_time) * 1000)  # Convert to milliseconds

        result = SummaryResult(
            total_files=len(summaries),
            processed_files=len(summaries),
            skipped_files=0,
            summaries=summaries,
            processing_time=processing_time
        )

        # Convert dataclasses to dictionaries for JSON serialization
        def dataclass_to_dict(obj):
            if hasattr(obj, '__dataclass_fields__'):
                return {k: dataclass_to_dict(v) for k, v in obj.__dict__.items()}
            elif isinstance(obj, list):
                return [dataclass_to_dict(item) for item in obj]
            else:
                return obj

        result_dict = dataclass_to_dict(result)
        output_json = json.dumps(result_dict, indent=2)

        if output:
            with open(output, 'w') as f:
                f.write(output_json)
            logger.info(f"Results written to: {output}")
        else:
            print(output_json)

        logger.info(f"Processing completed. Processed {result.processed_files} files in {result.processing_time}ms")

    except Exception as error:
        logger.error('Application error', error)
        sys.exit(1)


if __name__ == '__main__':
    main()