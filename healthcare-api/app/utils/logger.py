"""
Smart Logging System for Healthcare Chatbot
Provides structured logging with rotation, colors, and JSON formatting
"""
import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from datetime import datetime
import json
from typing import Any, Dict
from pythonjsonlogger import jsonlogger
import colorlog

# Create logs directory
LOGS_DIR = Path(__file__).parent.parent.parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)


class HealthcareLogger:
    """Smart logger with multiple handlers and formatting"""
    
    def __init__(self, name: str = "healthcare_api"):
        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Prevent duplicate handlers
        if self.logger.handlers:
            return
            
        # Console Handler with Colors
        self._add_console_handler()
        
        # File Handler - General logs (with rotation)
        self._add_file_handler(
            filename=LOGS_DIR / "app.log",
            level=logging.INFO,
            max_bytes=10 * 1024 * 1024,  # 10MB
            backup_count=5
        )
        
        # File Handler - Error logs
        self._add_file_handler(
            filename=LOGS_DIR / "error.log",
            level=logging.ERROR,
            max_bytes=10 * 1024 * 1024,
            backup_count=5
        )
        
        # File Handler - JSON logs for parsing
        self._add_json_handler(
            filename=LOGS_DIR / "app.json.log",
            level=logging.INFO
        )
        
        # File Handler - Daily rotating logs
        self._add_daily_handler(
            filename=LOGS_DIR / "daily.log",
            level=logging.INFO
        )
    
    def _add_console_handler(self):
        """Add colored console handler"""
        console_handler = colorlog.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        
        console_formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s | %(levelname)-8s | %(name)s | %(message)s%(reset)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )
        
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
    
    def _add_file_handler(self, filename: Path, level: int, max_bytes: int, backup_count: int):
        """Add rotating file handler"""
        file_handler = RotatingFileHandler(
            filename=filename,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(level)
        
        file_formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
    
    def _add_json_handler(self, filename: Path, level: int):
        """Add JSON formatted handler for log parsing"""
        json_handler = RotatingFileHandler(
            filename=filename,
            maxBytes=10 * 1024 * 1024,
            backupCount=5,
            encoding='utf-8'
        )
        json_handler.setLevel(level)
        
        json_formatter = jsonlogger.JsonFormatter(
            "%(asctime)s %(name)s %(levelname)s %(funcName)s %(lineno)d %(message)s",
            timestamp=True
        )
        
        json_handler.setFormatter(json_formatter)
        self.logger.addHandler(json_handler)
    
    def _add_daily_handler(self, filename: Path, level: int):
        """Add daily rotating handler"""
        daily_handler = TimedRotatingFileHandler(
            filename=filename,
            when='midnight',
            interval=1,
            backupCount=30,
            encoding='utf-8'
        )
        daily_handler.setLevel(level)
        
        daily_formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
        daily_handler.setFormatter(daily_formatter)
        self.logger.addHandler(daily_handler)
    
    def debug(self, message: str, **kwargs):
        """Log debug message with context"""
        self.logger.debug(message, extra=kwargs)
    
    def info(self, message: str, **kwargs):
        """Log info message with context"""
        self.logger.info(message, extra=kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log warning message with context"""
        self.logger.warning(message, extra=kwargs)
    
    def error(self, message: str, exc_info: bool = False, **kwargs):
        """Log error message with context"""
        self.logger.error(message, exc_info=exc_info, extra=kwargs)
    
    def critical(self, message: str, exc_info: bool = False, **kwargs):
        """Log critical message with context"""
        self.logger.critical(message, exc_info=exc_info, extra=kwargs)
    
    def api_request(self, method: str, path: str, status_code: int, duration: float, user_id: str = None):
        """Log API request details"""
        self.info(
            f"API Request: {method} {path} - Status: {status_code} - Duration: {duration:.2f}s",
            method=method,
            path=path,
            status_code=status_code,
            duration=duration,
            user_id=user_id
        )
    
    def ocr_processing(self, document_id: str, filename: str, status: str, duration: float = None):
        """Log OCR processing details"""
        msg = f"OCR Processing: {filename} ({document_id}) - Status: {status}"
        if duration:
            msg += f" - Duration: {duration:.2f}s"
        self.info(msg, document_id=document_id, filename=filename, status=status, duration=duration)
    
    def ai_request(self, agent: str, prompt_length: int, response_length: int, duration: float):
        """Log AI agent request details"""
        self.info(
            f"AI Request: {agent} - Prompt: {prompt_length} chars - Response: {response_length} chars - Duration: {duration:.2f}s",
            agent=agent,
            prompt_length=prompt_length,
            response_length=response_length,
            duration=duration
        )
    
    def database_query(self, collection: str, operation: str, duration: float, success: bool = True):
        """Log database operations"""
        status = "Success" if success else "Failed"
        self.info(
            f"Database: {collection}.{operation} - {status} - Duration: {duration:.3f}s",
            collection=collection,
            operation=operation,
            duration=duration,
            success=success
        )
    
    def health_summary(self, user_id: str, chats_count: int, docs_count: int, duration: float):
        """Log health summary generation"""
        self.info(
            f"Health Summary Generated: User {user_id} - Chats: {chats_count} - Docs: {docs_count} - Duration: {duration:.2f}s",
            user_id=user_id,
            chats_count=chats_count,
            docs_count=docs_count,
            duration=duration
        )


# Global logger instance
logger = HealthcareLogger("healthcare_api")


# Convenience functions
def debug(message: str, **kwargs):
    logger.debug(message, **kwargs)


def info(message: str, **kwargs):
    logger.info(message, **kwargs)


def warning(message: str, **kwargs):
    logger.warning(message, **kwargs)


def error(message: str, exc_info: bool = False, **kwargs):
    logger.error(message, exc_info=exc_info, **kwargs)


def critical(message: str, exc_info: bool = False, **kwargs):
    logger.critical(message, exc_info=exc_info, **kwargs)


# Specialized logging functions
def log_api_request(method: str, path: str, status_code: int, duration: float, user_id: str = None):
    logger.api_request(method, path, status_code, duration, user_id)


def log_ocr_processing(document_id: str, filename: str, status: str, duration: float = None):
    logger.ocr_processing(document_id, filename, status, duration)


def log_ai_request(agent: str, prompt_length: int, response_length: int, duration: float):
    logger.ai_request(agent, prompt_length, response_length, duration)


def log_database_query(collection: str, operation: str, duration: float, success: bool = True):
    logger.database_query(collection, operation, duration, success)


def log_health_summary(user_id: str, chats_count: int, docs_count: int, duration: float):
    logger.health_summary(user_id, chats_count, docs_count, duration)
