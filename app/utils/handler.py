import shutil
from pathlib import Path

def save_file(file, destination: Path):
    with destination.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
