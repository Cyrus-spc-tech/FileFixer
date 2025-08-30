# upload.py
from dotenv import load_dotenv
import os
import subprocess

load_dotenv()

cmd = ["twine", "upload", "dist/*"]
subprocess.run(cmd, check=True)