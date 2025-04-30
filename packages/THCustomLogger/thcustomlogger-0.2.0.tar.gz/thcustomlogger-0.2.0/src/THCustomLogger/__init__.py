from __future__ import annotations

from .logger_setup import (
    LoggerFactory,
    CustomLogger,
    MultilineFormatter,
    ColoredMultilineFormatter
)

__all__ = [
    'LoggerFactory',
    'CustomLogger',
    'MultilineFormatter',
    'ColoredMultilineFormatter'
]

# Optional: Set default logging class
import logging
logging.setLoggerClass(CustomLogger)