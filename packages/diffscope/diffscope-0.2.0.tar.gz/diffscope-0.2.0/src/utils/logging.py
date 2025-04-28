"""
Logging configuration for DiffScope.

This module sets up structured logging using structlog.
"""

import sys
import logging
import structlog
from typing import Any, Dict, Optional

# # Configure standard logging
# logging.basicConfig(
#     format="%(message)s",
#     stream=sys.stdout,
#     level=logging.INFO,
# )

# # Configure structlog
# structlog.configure(
#     processors=[
#         structlog.stdlib.filter_by_level,
#         structlog.stdlib.add_logger_name,
#         structlog.stdlib.add_log_level,
#         structlog.stdlib.PositionalArgumentsFormatter(),
#         structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
#         structlog.processors.StackInfoRenderer(),
#         structlog.processors.format_exc_info,
#         structlog.processors.UnicodeDecoder(),
#         structlog.dev.ConsoleRenderer(colors=True),
#     ],
#     context_class=dict,
#     logger_factory=structlog.stdlib.LoggerFactory(),
#     wrapper_class=structlog.stdlib.BoundLogger,
#     cache_logger_on_first_use=True,
# )

def get_logger(name: str, **initial_values: Any) -> structlog.BoundLogger:
    """
    Get a structured logger with the given name and initial values.
    
    Args:
        name: The name of the logger, usually the module name.
        initial_values: Initial values to bind to the logger.
        
    Returns:
        A structured logger instance.
    """
    return structlog.get_logger(name, **initial_values)

def set_log_level(level: str) -> None:
    """
    Set the log level for DiffScope.
    
    Args:
        level: The log level to set (DEBUG, INFO, WARNING, ERROR, CRITICAL).
    """
    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {level}")
    logging.getLogger().setLevel(numeric_level) 