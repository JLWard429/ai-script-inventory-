#!/usr/bin/env python3
"""
Centralized Logging Utility for AI Script Inventory.

This module provides a comprehensive, configurable logging system with:
- Structured logging with configurable levels and formats
- Performance monitoring and timing utilities
- Context-aware logging with metadata
- File and console output management
- Integration with the superhuman terminal system

Usage:
    from python_scripts.logging_utils import get_logger, log_performance
    
    logger = get_logger(__name__)
    logger.info("Application started")
    
    @log_performance
    def some_function():
        # Function implementation
        pass
"""

import logging
import logging.handlers
import sys
import time
from contextlib import contextmanager
from datetime import datetime
from functools import wraps
from pathlib import Path
from typing import Any, Dict, Optional, Union

# Configure default logging settings
DEFAULT_LOG_FORMAT = "%(asctime)s [%(levelname)8s] %(name)s:%(lineno)d - %(message)s"
DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
DEFAULT_LOG_LEVEL = logging.INFO
LOG_DIRECTORY = Path("logs")


class StructuredLogger:
    """
    A structured logging manager that provides consistent logging across the application.
    
    Features:
    - Configurable log levels and formats
    - File rotation and retention
    - Performance monitoring
    - Context-aware logging
    - Thread-safe operations
    """

    def __init__(
        self,
        name: str,
        level: Union[int, str] = DEFAULT_LOG_LEVEL,
        log_format: str = DEFAULT_LOG_FORMAT,
        date_format: str = DEFAULT_DATE_FORMAT,
        enable_file_logging: bool = True,
        enable_console_logging: bool = True,
        log_directory: Optional[Path] = None,
    ) -> None:
        """
        Initialize the structured logger.
        
        Args:
            name: Logger name (typically __name__)
            level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_format: Format string for log messages
            date_format: Format string for timestamps
            enable_file_logging: Whether to log to files
            enable_console_logging: Whether to log to console
            log_directory: Directory for log files (default: ./logs)
        """
        self.name = name
        self.level = level if isinstance(level, int) else getattr(logging, level.upper())
        self.log_format = log_format
        self.date_format = date_format
        self.enable_file_logging = enable_file_logging
        self.enable_console_logging = enable_console_logging
        self.log_directory = log_directory or LOG_DIRECTORY
        
        self._logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """Set up and configure the logger with handlers."""
        logger = logging.getLogger(self.name)
        logger.setLevel(self.level)
        
        # Clear existing handlers to avoid duplicates
        logger.handlers.clear()
        
        formatter = logging.Formatter(self.log_format, self.date_format)
        
        # Console handler
        if self.enable_console_logging:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(self.level)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
        
        # File handler with rotation
        if self.enable_file_logging:
            self._ensure_log_directory()
            
            # Create a sanitized filename from logger name
            safe_name = self.name.replace(".", "_").replace("/", "_")
            log_file = self.log_directory / f"{safe_name}.log"
            
            file_handler = logging.handlers.RotatingFileHandler(
                log_file,
                maxBytes=10 * 1024 * 1024,  # 10MB
                backupCount=5
            )
            file_handler.setLevel(logging.DEBUG)  # File gets all levels
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        
        return logger

    def _ensure_log_directory(self) -> None:
        """Ensure the log directory exists."""
        try:
            self.log_directory.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            print(f"Warning: Could not create log directory {self.log_directory}: {e}")

    def get_logger(self) -> logging.Logger:
        """Get the configured logger instance."""
        return self._logger

    def log_with_context(
        self, 
        level: int, 
        message: str, 
        context: Optional[Dict[str, Any]] = None,
        **kwargs: Any
    ) -> None:
        """
        Log a message with additional context information.
        
        Args:
            level: Logging level
            message: Log message
            context: Additional context dictionary
            **kwargs: Additional context as keyword arguments
        """
        context = context or {}
        context.update(kwargs)
        
        if context:
            context_str = " | ".join(f"{k}={v}" for k, v in context.items())
            formatted_message = f"{message} | {context_str}"
        else:
            formatted_message = message
        
        self._logger.log(level, formatted_message)

    def debug(self, message: str, **kwargs: Any) -> None:
        """Log a debug message with optional context."""
        self.log_with_context(logging.DEBUG, message, **kwargs)

    def info(self, message: str, **kwargs: Any) -> None:
        """Log an info message with optional context."""
        self.log_with_context(logging.INFO, message, **kwargs)

    def warning(self, message: str, **kwargs: Any) -> None:
        """Log a warning message with optional context."""
        self.log_with_context(logging.WARNING, message, **kwargs)

    def error(self, message: str, **kwargs: Any) -> None:
        """Log an error message with optional context."""
        self.log_with_context(logging.ERROR, message, **kwargs)

    def critical(self, message: str, **kwargs: Any) -> None:
        """Log a critical message with optional context."""
        self.log_with_context(logging.CRITICAL, message, **kwargs)

    def exception(self, message: str, **kwargs: Any) -> None:
        """Log an exception with traceback."""
        self.log_with_context(logging.ERROR, message, **kwargs)
        self._logger.exception(message)


# Global logger instance cache
_logger_cache: Dict[str, StructuredLogger] = {}


def get_logger(
    name: str,
    level: Union[int, str] = DEFAULT_LOG_LEVEL,
    **kwargs: Any
) -> logging.Logger:
    """
    Get a configured logger instance.
    
    This function provides a simple interface to get loggers with consistent
    configuration across the application.
    
    Args:
        name: Logger name (typically __name__)
        level: Logging level
        **kwargs: Additional configuration options
    
    Returns:
        Configured logger instance
    
    Example:
        >>> logger = get_logger(__name__)
        >>> logger.info("Application started")
    """
    cache_key = f"{name}_{level}_{hash(tuple(sorted(kwargs.items())))}"
    
    if cache_key not in _logger_cache:
        _logger_cache[cache_key] = StructuredLogger(name, level, **kwargs)
    
    return _logger_cache[cache_key].get_logger()


def log_performance(func: Any = None, *, logger_name: Optional[str] = None) -> Any:
    """
    Decorator to log function performance timing.
    
    Args:
        func: Function to decorate
        logger_name: Custom logger name (defaults to function module)
    
    Returns:
        Decorated function
    
    Example:
        >>> @log_performance
        ... def slow_function():
        ...     time.sleep(1)
        ...     return "done"
        
        >>> @log_performance(logger_name="my.custom.logger")
        ... def another_function():
        ...     return "result"
    """
    def decorator(f: Any) -> Any:
        @wraps(f)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            logger_instance = StructuredLogger(logger_name or f.__module__)
            start_time = time.time()
            
            try:
                logger_instance.info(
                    f"Starting {f.__name__}",
                    function=f.__name__,
                    module=f.__module__
                )
                
                result = f(*args, **kwargs)
                
                duration = time.time() - start_time
                logger_instance.info(
                    f"Completed {f.__name__}",
                    function=f.__name__,
                    duration_ms=round(duration * 1000, 2),
                    success=True
                )
                
                return result
                
            except Exception as e:
                duration = time.time() - start_time
                logger_instance.error(
                    f"Failed {f.__name__}",
                    function=f.__name__,
                    duration_ms=round(duration * 1000, 2),
                    error=str(e),
                    success=False
                )
                raise
        
        return wrapper
    
    if func is None:
        return decorator
    else:
        return decorator(func)


@contextmanager
def log_context(
    logger: Union[logging.Logger, StructuredLogger],
    context_name: str,
    level: int = logging.INFO,
    **context: Any
):
    """
    Context manager for logging operation start and completion.
    
    Args:
        logger: Logger instance (can be standard logger or StructuredLogger)
        context_name: Name of the operation context
        level: Logging level
        **context: Additional context information
    
    Example:
        >>> logger = get_logger(__name__)
        >>> with log_context(logger, "file_processing", file_count=10):
        ...     # Process files
        ...     pass
    """
    start_time = time.time()
    
    # Handle both StructuredLogger and standard logger
    if isinstance(logger, StructuredLogger):
        log_func = logger.log_with_context
    else:
        # For standard logger, use a simpler approach
        def log_func(lvl: int, msg: str, **ctx: Any) -> None:
            ctx_str = " | ".join(f"{k}={v}" for k, v in ctx.items()) if ctx else ""
            full_msg = f"{msg} | {ctx_str}" if ctx_str else msg
            logger.log(lvl, full_msg)
    
    log_func(
        level,
        f"Starting {context_name}",
        operation=context_name,
        **context
    )
    
    try:
        yield
        
        duration = time.time() - start_time
        log_func(
            level,
            f"Completed {context_name}",
            operation=context_name,
            duration_ms=round(duration * 1000, 2),
            success=True,
            **context
        )
        
    except Exception as e:
        duration = time.time() - start_time
        log_func(
            logging.ERROR,
            f"Failed {context_name}",
            operation=context_name,
            duration_ms=round(duration * 1000, 2),
            error=str(e),
            success=False,
            **context
        )
        raise


def configure_root_logging(
    level: Union[int, str] = DEFAULT_LOG_LEVEL,
    format_string: str = DEFAULT_LOG_FORMAT,
    enable_file_logging: bool = True
) -> None:
    """
    Configure the root logger for the entire application.
    
    Args:
        level: Logging level for root logger
        format_string: Format string for log messages
        enable_file_logging: Whether to enable file logging
    
    Example:
        >>> configure_root_logging(level="DEBUG", enable_file_logging=True)
    """
    root_logger = get_logger(
        "ai_script_inventory",
        level=level,
        log_format=format_string,
        enable_file_logging=enable_file_logging
    )
    
    # Set this as the root logger configuration
    logging.basicConfig(
        level=level if isinstance(level, int) else getattr(logging, level.upper()),
        format=format_string,
        handlers=root_logger.handlers
    )


# Example usage and integration demonstration
if __name__ == "__main__":
    """
    Demonstration of logging utility features.
    """
    
    # Configure application-wide logging
    configure_root_logging(level="DEBUG")
    
    # Get a logger for this module
    logger = get_logger(__name__)
    
    # Basic logging with context
    logger.info("Application started")
    structured_logger = StructuredLogger(__name__)
    structured_logger.debug("Debug information", user_id=123, session="abc")
    structured_logger.warning("Warning message", component="auth")
    
    # Performance logging
    @log_performance
    def example_function(delay: float = 0.1) -> str:
        """Example function with performance logging."""
        time.sleep(delay)
        return "completed"
    
    result = example_function(0.2)
    structured_logger.info("Function result", result=result)
    
    # Context logging
    structured_logger = StructuredLogger(__name__)
    with log_context(structured_logger, "batch_processing", batch_size=100):
        time.sleep(0.1)  # Simulate work
        structured_logger.info("Processing item", item_id=42)
    
    # Error logging
    structured_logger = StructuredLogger(__name__)
    try:
        raise ValueError("Example error")
    except ValueError as e:
        structured_logger.exception("An error occurred", error_type=type(e).__name__)
    
    logger.info("Application completed")