import shutil
import typer

class WelcomeScreen:
    def __init__(self):
        self.terminal_width = shutil.get_terminal_size().columns

    def _center_message(self, message: str) -> str:
        return message.center(self.terminal_width)

    def _create_screen(self, welcome_message: str, info_message: str, color: str) -> str:
        border = "=" * self.terminal_width
        empty_line = " " * self.terminal_width
        
        centered_welcome = self._center_message(welcome_message)
        centered_info = self._center_message(info_message)
        
        full_message = f"{color}{border}\033[0m\n" \
                       f"{color}{empty_line}\033[0m\n" \
                       f"{color}{centered_welcome}\033[0m\n" \
                       f"{color}{empty_line}\033[0m\n" \
                       f"{color}{centered_info}\033[0m\n" \
                       f"{color}{empty_line}\033[0m\n" \
                       f"{color}{border}\033[0m"
        
        return full_message

    def show(self, download_type: str):
        if download_type.lower() == 'mp4':
            welcome_message = "!! YouTube Downloader !!"
            info_message = "Download your favorite videos in MP4 format with ease."
            color = "\033[1;32m"
        elif download_type.lower() == 'mp3':
            welcome_message = "!! YouTube Downloader !!"
            info_message = "Download your favorite audio in MP3 format with ease."
            color = "\033[1;34m"
        elif download_type == "":
            welcome_message = "!! Welcome to YouTube Downloader !!"
            info_message = "A CLI App for downloading any video in MP3 and MP4 format."
            color = "\033[1;35m"
        else:
            raise ValueError("Unsupported download type")
        
        full_message = self._create_screen(welcome_message, info_message, color)
        
        typer.echo(full_message)