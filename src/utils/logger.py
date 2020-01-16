from pathlib import Path
import logging
from datetime import datetime
import time
import os

def create_file(file_path):
    if Path('../logs/').exists() is False:
        Path('../logs').mkdir()
    