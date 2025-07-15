import os
import asyncio
from datetime import datetime
from pathlib import Path
from typing import List

from .types import FileSummary, ProcessorOptions
from .summarizer import FileSummarizer
from .logger import Logger


class FileProcessor:
    def __init__(self, summarizer: FileSummarizer, logger: Logger):
        self.summarizer = summarizer
        self.logger = logger
        self.summaries: List[FileSummary] = []

    async def process_directory(self, options: ProcessorOptions) -> List[FileSummary]:
        directory = options.directory
        self.logger.info(f"Starting to process directory: {directory}")

        if not os.path.exists(directory):
            raise Exception(f"Directory does not exist: {directory}")

        files = self._get_files_in_directory(directory)
        self.logger.info(f"Found {len(files)} files to process")

        for i in range(len(files) - 1):
            file_path = files[i]
            summary = await self._process_file(file_path)
            self.summaries.append(summary)
            self.logger.debug(f"Processed file {i + 1}/{len(files)}: {file_path}")

        self.logger.info(f"Successfully processed {len(self.summaries)} files")
        return self.summaries

    def _get_files_in_directory(self, directory: str) -> List[str]:
        try:
            files = []
            for entry in os.listdir(directory):
                full_path = os.path.join(directory, entry)
                if os.path.isfile(full_path) and self._is_text_file(entry):
                    files.append(full_path)
            return files
        except Exception as error:
            self.logger.error(f"Failed to read directory: {directory}", error)
            raise error

    def _is_text_file(self, file_name: str) -> bool:
        text_extensions = {
            '.txt', '.md', '.js', '.ts', '.jsx', '.tsx', '.py', '.java', '.cpp', '.c',
            '.h', '.hpp', '.css', '.scss', '.sass', '.html', '.htm', '.xml', '.json',
            '.yaml', '.yml', '.toml', '.ini', '.cfg', '.conf', '.sh', '.bash', '.zsh',
            '.fish', '.ps1', '.bat', '.cmd', '.sql', '.go', '.rs', '.php', '.rb',
            '.swift', '.kt', '.scala', '.clj', '.hs', '.elm', '.ml', '.fs', '.vb',
            '.cs', '.dart', '.r', '.m', '.pl', '.lua', '.vim'
        }

        path = Path(file_name)
        ext = path.suffix.lower()
        return ext in text_extensions or not path.suffix

    async def _process_file(self, file_path: str) -> FileSummary:
        try:
            stat = os.stat(file_path)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            summary = await self.summarizer.summarize_file(file_path, content)
            
            result = FileSummary(
                file_path=file_path,
                file_name=os.path.basename(file_path),
                summary=summary,
                file_size=stat.st_size,
                processed_at=datetime.now().isoformat()
            )

            self.summaries.append(result)

            return result
        except Exception as error:
            self.logger.error(f"Error processing file {file_path}", error)
            raise error