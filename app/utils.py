# utils.py
import os
import logging
import shutil

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    return logging.getLogger(__name__)

def ensure_directory_exists(directory):
    os.makedirs(directory, exist_ok=True)

def clean_temp_files(directory):
    if os.path.exists(directory):
        try:
            shutil.rmtree(directory)
            os.makedirs(directory)
        except Exception as e:
            print(f"Error cleaning directory {directory}: {e}")

def validate_file_extension(file_name, allowed_extensions):
    return any(file_name.lower().endswith(ext) for ext in allowed_extensions)

def get_file_size(file_path):
    try:
        return os.path.getsize(file_path)
    except FileNotFoundError:
        return None


