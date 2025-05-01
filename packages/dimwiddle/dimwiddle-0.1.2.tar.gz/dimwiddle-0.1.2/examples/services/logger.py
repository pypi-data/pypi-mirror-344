import logging
from typing import Optional

class Logger:
    """
    A simple logging service that demonstrates configuration injection.
    """
    
    LOG_LEVELS = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }
    
    def __init__(self, log_level: str = 'info'):
        """
        Initialize the logger with the specified log level.
        
        Args:
            log_level: The logging level (debug, info, warning, error, critical)
        """
        # Convert string log level to logging constant
        numeric_level = self.LOG_LEVELS.get(log_level.lower(), logging.INFO)
        
        # Configure logging
        logging.basicConfig(
            level=numeric_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        self.logger = logging.getLogger('dimwiddle')
        
    def debug(self, message: str):
        """Log a debug message."""
        self.logger.debug(message)
        
    def info(self, message: str):
        """Log an info message."""
        self.logger.info(message)
        
    def warning(self, message: str):
        """Log a warning message."""
        self.logger.warning(message)
        
    def error(self, message: str):
        """Log an error message."""
        self.logger.error(message)
        
    def critical(self, message: str):
        """Log a critical message."""
        self.logger.critical(message)