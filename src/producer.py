import subprocess
import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

AWS_KINESISVIDEO_NAME = os.getenv('AWS_KINESISVIDEO_NAME')
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
REGION_NAME = os.getenv('REGION_NAME')

def loop():
    try:
        while True:
           subprocess.Popen(['../gstreamer.sh', AWS_KINESISVIDEO_NAME, AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY])
    except KeyboardInterrupt:
        return

if __name__ == '__main__':
    file_name = datetime.now().strftime('%d-%m-%H:%M:%S_logs.txt')
    loop()
