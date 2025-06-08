import os
import datetime
import logging


def setup_logging():
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    log_folder = os.path.join('logs', current_date)
    os.makedirs(log_folder, exist_ok=True)
    
    log_levels = ['INFO','WARNING','ERROR']
    
    for log_level in log_levels:
        
        log_path = os.path.join(log_folder, f'{log_level.lower()}.log')
        logger = logging.getLogger(log_level)
        logger.setLevel(logging.getLevelName(log_level))        
        file_handler = logging.FileHandler(log_path)
        formatter = logging.Formatter('%(asctime)s-%(levelname)s-%(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)