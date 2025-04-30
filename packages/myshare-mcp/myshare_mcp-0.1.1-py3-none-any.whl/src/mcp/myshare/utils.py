# Add these imports at the top
from datetime import datetime, timedelta
import os

# support logging
import logging
from logging.handlers import RotatingFileHandler

# Configure logging
def setup_logger():
    # Create logs directory if it doesn't exist
    log_dir = "logs"
    log_file = os.path.join(log_dir, "myshare.log")
    os.makedirs(log_dir, exist_ok=True)

    # Log format
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(log_format)

    # Log to console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Log to file (with rotation)
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=1024 * 1024,  # 1MB per file
        backupCount=5,          # Keep 5 backups
    )
    file_handler.setFormatter(formatter)

    # Root logger configuration
    logging.basicConfig(
        level=logging.INFO,     # Default level
        handlers=[console_handler, file_handler]
    )

def get_working_days(start_date: str, end_date: str) -> int:
    """Calculate number of working days between two dates"""
    start = datetime.strptime(start_date, "%Y%m%d")
    end = datetime.strptime(end_date, "%Y%m%d")
    days = 0
    current = start
    
    while current <= end:
        # Skip weekends (5 = Saturday, 6 = Sunday)
        if current.weekday() < 5:
            days += 1
        current += timedelta(days=1)
    
    return days

# 示例调用
if __name__ == "__main__":
    start_date = "20230101"
    end_date = "20230110"
    working_days = get_working_days(start_date, end_date)
    print(f"从 {start_date} 到 {end_date} 的工作日数量: {working_days}")