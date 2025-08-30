#!/usr/bin/env python3
"""
Tests for the centralized logging utility.
"""

import logging
import tempfile
import time
from pathlib import Path
from unittest.mock import patch

import pytest

from python_scripts.logging_utils import (
    StructuredLogger,
    configure_root_logging,
    get_logger,
    log_context,
    log_performance,
)


class TestStructuredLogger:
    """Test cases for StructuredLogger."""

    def test_structured_logger_creation(self):
        """Test that StructuredLogger can be created."""
        logger = StructuredLogger("test_logger")
        assert logger.name == "test_logger"
        assert isinstance(logger.get_logger(), logging.Logger)

    def test_structured_logger_with_context(self):
        """Test logging with context information."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_dir = Path(temp_dir)
            logger = StructuredLogger(
                "test_context",
                log_directory=log_dir,
                enable_console_logging=False
            )
            
            logger.info("Test message", user_id=123, session="abc")
            
            # Check that log file was created
            log_files = list(log_dir.glob("*.log"))
            assert len(log_files) == 1
            
            # Check log content
            log_content = log_files[0].read_text()
            assert "Test message" in log_content
            assert "user_id=123" in log_content
            assert "session=abc" in log_content

    def test_performance_decorator(self):
        """Test the performance monitoring decorator."""
        
        @log_performance
        def test_function(delay: float = 0.01) -> str:
            time.sleep(delay)
            return "success"
        
        # Mock to capture log output
        with patch('python_scripts.logging_utils.StructuredLogger') as mock_logger:
            mock_instance = mock_logger.return_value
            
            result = test_function(0.01)
            
            assert result == "success"
            # Verify that logger was called for start and completion
            assert mock_instance.info.call_count >= 2

    def test_log_context_manager(self):
        """Test the log context manager."""
        logger = StructuredLogger("test_context_mgr", enable_file_logging=False)
        
        with patch.object(logger, 'log_with_context') as mock_log:
            with log_context(logger, "test_operation", batch_size=10):
                time.sleep(0.01)
            
            # Should have logged start and completion
            assert mock_log.call_count == 2
            
            # Check that both calls included the batch_size context
            for call in mock_log.call_args_list:
                assert 'batch_size' in call[1]  # kwargs

    def test_log_context_manager_with_exception(self):
        """Test log context manager when an exception occurs."""
        logger = StructuredLogger("test_exception", enable_file_logging=False)
        
        with patch.object(logger, 'log_with_context') as mock_log:
            with pytest.raises(ValueError):
                with log_context(logger, "failing_operation"):
                    raise ValueError("Test error")
            
            # Should have logged start and failure
            assert mock_log.call_count == 2
            
            # Check that the failure log includes error info
            failure_call = mock_log.call_args_list[1]
            assert 'error' in failure_call[1]
            assert 'success=False' in str(failure_call)

    def test_get_logger_function(self):
        """Test the get_logger convenience function."""
        logger = get_logger("test_get_logger")
        assert isinstance(logger, logging.Logger)
        assert logger.name.endswith("test_get_logger")

    def test_different_log_levels(self):
        """Test different logging levels."""
        logger = StructuredLogger("test_levels", enable_file_logging=False)
        
        # Test all logging levels
        logger.debug("Debug message", category="debug")
        logger.info("Info message", category="info")
        logger.warning("Warning message", category="warning")
        logger.error("Error message", category="error")
        logger.critical("Critical message", category="critical")

    def test_file_rotation_setup(self):
        """Test that file rotation is properly configured."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_dir = Path(temp_dir)
            logger = StructuredLogger(
                "test_rotation",
                log_directory=log_dir,
                enable_console_logging=False
            )
            
            # Get the file handler
            file_handlers = [h for h in logger.get_logger().handlers 
                           if isinstance(h, logging.handlers.RotatingFileHandler)]
            
            assert len(file_handlers) == 1
            handler = file_handlers[0]
            assert handler.maxBytes == 10 * 1024 * 1024  # 10MB
            assert handler.backupCount == 5

    def test_configure_root_logging(self):
        """Test root logging configuration."""
        configure_root_logging(level="DEBUG", enable_file_logging=False)
        
        # Test that root logger level is set correctly
        root_logger = logging.getLogger("ai_script_inventory")
        assert root_logger.level == logging.DEBUG


class TestLoggingIntegration:
    """Integration tests for logging components."""

    def test_performance_and_context_integration(self):
        """Test that performance decorator and context manager work together."""
        
        @log_performance
        def complex_operation(items: int = 5) -> str:
            logger = StructuredLogger("complex_op", enable_file_logging=False)
            with log_context(logger, "processing", item_count=items):
                time.sleep(0.01)
                return f"processed {items} items"
        
        result = complex_operation(3)
        assert result == "processed 3 items"

    def test_error_handling_integration(self):
        """Test error handling across logging components."""
        
        @log_performance
        def failing_operation() -> None:
            logger = StructuredLogger("failing_op", enable_file_logging=False)
            with log_context(logger, "doomed_operation"):
                raise RuntimeError("Intentional failure")
        
        with pytest.raises(RuntimeError):
            failing_operation()

    def test_multiple_logger_instances(self):
        """Test that multiple logger instances work independently."""
        logger1 = StructuredLogger("logger1", enable_file_logging=False)
        logger2 = StructuredLogger("logger2", enable_file_logging=False)
        
        logger1.info("Message from logger 1")
        logger2.warning("Message from logger 2")
        
        # Both should work without interference
        assert logger1.name == "logger1"
        assert logger2.name == "logger2"


if __name__ == "__main__":
    pytest.main([__file__])