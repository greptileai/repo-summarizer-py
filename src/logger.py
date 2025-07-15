import logging
import sys
from typing import Optional
from colorama import Fore, Style, init

# Initialize colorama for cross-platform colored output
init(autoreset=True)


class ColoredFormatter(logging.Formatter):
    """Custom formatter that adds colors to log levels"""
    
    LEVEL_COLORS = {
        'DEBUG': Fore.CYAN,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.MAGENTA + Style.BRIGHT,
    }

    def format(self, record):
        # Save the original format
        original_format = self._style._fmt
        
        # Add color to the level name
        level_color = self.LEVEL_COLORS.get(record.levelname, '')
        colored_level = f"{level_color}{record.levelname}{Style.RESET_ALL}"
        
        # Temporarily modify the format to include colors
        self._style._fmt = original_format.replace('%(levelname)s', colored_level)
        
        # Format the record
        formatted = super().format(record)
        
        # Restore the original format
        self._style._fmt = original_format
        
        return formatted


class Logger:
    def __init__(self, level: str = "info"):
        self.logger = logging.getLogger("repo-summarizer")
        self.logger.setLevel(self._get_log_level(level))
        
        # Clear any existing handlers
        self.logger.handlers.clear()
        
        # Console handler with colored formatter
        console_handler = logging.StreamHandler(sys.stdout)
        console_formatter = ColoredFormatter(
            '%(asctime)s [%(levelname)s]: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # File handler
        file_handler = logging.FileHandler('summarizer.log')
        file_formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s]: %(message)s - %(pathname)s:%(lineno)d',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

    def _get_log_level(self, level: str) -> int:
        level_map = {
            "debug": logging.DEBUG,
            "info": logging.INFO,
            "warn": logging.WARNING,
            "warning": logging.WARNING,
            "error": logging.ERROR,
            "critical": logging.CRITICAL
        }
        return level_map.get(level.lower(), logging.INFO)

    def info(self, message: str, meta: Optional[dict] = None):
        if meta:
            self.logger.info(f"{message} - {meta}")
        else:
            self.logger.info(message)

    def error(self, message: str, error: Optional[Exception] = None):
        if error:
            self.logger.error(f"{message}: {str(error)}", exc_info=True)
        else:
            self.logger.error(message)

    def warn(self, message: str, meta: Optional[dict] = None):
        if meta:
            self.logger.warning(f"{message} - {meta}")
        else:
            self.logger.warning(message)

    def debug(self, message: str, meta: Optional[dict] = None):
        if meta:
            self.logger.debug(f"{message} - {meta}")
        else:
            self.logger.debug(message)

    def set_level(self, level: str):
        self.logger.setLevel(self._get_log_level(level))