from typing import List
from enum import Enum

class DownloadType(str, Enum):
    audio = "MP3"
    video = "MP4"
    
class Progress(str, Enum):
    true = True
    false = False

def file_reader(file_path: str) -> List[str]:
    links = list()
    
    try:
        with open(file_path, 'r') as file:
            for line in file:
                links.append(line.strip())
    except FileNotFoundError:
        print(f"Error: The file at {file_path} does not exist.")
    except IOError:
        print(f"Error: An I/O error occurred while reading the file at {file_path}.")
    
    return links