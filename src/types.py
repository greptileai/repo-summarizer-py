from dataclasses import dataclass
from typing import List, Optional


@dataclass
class FileSummary:
    file_path: str
    file_name: str
    summary: str
    file_size: int
    processed_at: str


@dataclass
class SummarizerOptions:
    api_key: str
    model: Optional[str] = "gpt-3.5-turbo"
    max_tokens: Optional[int] = 150
    temperature: Optional[float] = 0.3


@dataclass
class ProcessorOptions:
    directory: str
    output_file: Optional[str] = None
    log_level: Optional[str] = "info"


@dataclass
class SummaryResult:
    total_files: int
    processed_files: int
    skipped_files: int
    summaries: List[FileSummary]
    processing_time: int