"""
Logging utilities with structured logging
Uses loguru for enhanced logging capabilities
"""
import sys
from pathlib import Path
from loguru import logger
from src.models.config import AppConfig


def setup_logging(config: AppConfig) -> None:
    """
    Configure structured logging with loguru
    
    Args:
        config: Application configuration
    """
    # Remove default handler
    logger.remove()
    
    # Console logging with colors
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=config.log_level,
        colorize=True,
    )
    
    # File logging (JSON for production)
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    logger.add(
        log_dir / "app.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=config.log_level,
        rotation="10 MB",
        retention="7 days",
        compression="zip",
    )
    
    # Error logging (separate file)
    logger.add(
        log_dir / "errors.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="ERROR",
        rotation="10 MB",
        retention="30 days",
        compression="zip",
        backtrace=True,
        diagnose=True,
    )
    
    logger.info(f"Logging initialized | Level: {config.log_level} | Environment: {config.environment}")


def get_logger(name: str):
    """
    Get a logger instance for a specific module
    
    Args:
        name: Module name (usually __name__)
        
    Returns:
        Logger instance
    """
    return logger.bind(module=name)
