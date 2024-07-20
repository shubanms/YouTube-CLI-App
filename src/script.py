import typer
import time

from utils.welcome import WelcomeScreen
from utils.utils import DownloadType, Progress, file_reader
from utils.downloader import Downloader
from utils import constants

# TODO - Add in a function to create the links and download folder if does not exist already then create it

app = typer.Typer()
welcome_screen = WelcomeScreen()

@app.command(help = "Main screen of the CLI app and use instructions")
def start() -> None:
    welcome_screen.show("")
    time.sleep(2)

@app.command(help = "Download YouTube videos in MP3 or MP4 format with TYPE")
def download(link: str, type: DownloadType = DownloadType.video, show_progress: Progress = Progress.true) -> None:
    welcome_screen.show(type)
    time.sleep(2)
    
    if type == DownloadType.video:
        downloader = Downloader(video_links = [link], show_progress = show_progress)
        downloader.download_video()
    else:
        downloader = Downloader(audio_links = [link], show_progress = show_progress)
        downloader.download_audio()

@app.command(help = "Download a batch of Youtube videos in MP3 or MP4 format with TYPE")
def bulk_download(type: DownloadType = DownloadType.video, show_progress: Progress = Progress.true) -> None:
    welcome_screen.show(type)
    time.sleep(2)
    
    if type == DownloadType.video:
        downloader = Downloader(video_links = file_reader(constants.video_links), show_progress = show_progress)
        downloader.download_video()
    else:
        downloader = Downloader(audio_links = file_reader(constants.audio_links), show_progress = show_progress)
        downloader.download_audio()
 
if __name__ == "__main__":
    app()
