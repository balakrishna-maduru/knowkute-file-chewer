# Centralized configuration for Knowkute File Chewer

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '../data')
MODELS_DIR = os.path.join(BASE_DIR, '../models')
CHUNK_SIZE = 512  # Default chunk size for splitting

# Add more config variables as needed
