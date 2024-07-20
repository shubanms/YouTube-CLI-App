import os
import sys
import time
import subprocess

from typing import List
from tqdm import tqdm
from pytube import YouTube

from utils.utils import Progress
import utils.constants as constants

# TODO - Need to work on the audio and video merge maybe try to use proxy or switch clients

# ! Do not use the download_video method as they dont merge the video and audio file together

# ? Maybe add in a feature where the links are automatically removed from the text file and perhaps 
# ? stored in another local file future reference


class Downloader:
    def __init__(self, show_progress: Progress, video_links: List[str] = None, audio_links: List[str] = None) -> None:
        self.video_links = video_links if video_links is not None else constants.video_links
        self.audio_links = audio_links if audio_links is not None else constants.audio_links
        
        self.audio_path = constants.audio_download_path
        self.video_path = constants.video_download_path
        
        self.show_progress = show_progress
        
    def download(self) -> None:
        pass
        
    def download_video(self):
        if self.show_progress == Progress.true:
            total_videos = len(self.video_links)
            
            with tqdm(total=total_videos, ncols=100, desc="Downloading videos", position=0, leave=True) as pbar:
                for link in self.video_links:
                    youtube_object = YouTube(link)
                    print(f"\nVideo Title: {youtube_object.title}\n{'-'*80}")
                    
                    video_stream = youtube_object.streams.filter(res="720p", file_extension="webm").first()
                    
                    audio_stream = youtube_object.streams.filter(only_audio=True, file_extension="webm").first()
                    
                    if video_stream is None:
                        print("720p video stream not available. Downloading the highest available quality.")
                        video_stream = youtube_object.streams.filter(file_extension="webm").get_highest_resolution()
            
                    if video_stream and audio_stream:
                        video_temp_path = os.path.join(self.video_path, "temp_video.webm")
                        audio_temp_path = os.path.join(self.video_path, "temp_audio.webm")
                        
                        video_stream.download(output_path=self.video_path, filename="temp_video.webm")
                        audio_stream.download(output_path=self.video_path, filename="temp_audio.webm")
                        
                        output_video_path = os.path.join(self.video_path, f"{youtube_object.title}.mp4")
                        
                        subprocess.run(
                            [
                                'ffmpeg', '-y', '-i', video_temp_path, '-i', audio_temp_path, 
                                '-c:v', 'copy', '-c:a', 'aac', output_video_path
                            ],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL
                        )
                        
                        os.remove(video_temp_path)
                        os.remove(audio_temp_path)
                        
                        print(f"Downloaded and merged: {output_video_path}")
                    
                    sys.stdout.flush()
                    pbar.update(1)
                    
                sys.stdout.write("\r" + " " * 80 + "\r")
                sys.stdout.flush()
                
            print()
            print("\nAll videos downloaded successfully!")
        else:
            for index, link in enumerate(self.video_links):
                youtube_object = YouTube(link)
                sys.stdout.write(f"\rDownloading video {index + 1}/{len(self.video_links)}: {youtube_object.title}")
                sys.stdout.flush()
                time.sleep(0.5)
            print()
            print("\nAll videos downloaded successfully!")      
    
    def download_audio(self):
        if self.show_progress == Progress.true:
            total_audios = len(self.audio_links)
            
            with tqdm(total=total_audios, ncols=100, desc="Downloading audios", position=0, leave=True) as pbar:
                for link in self.audio_links:
                    youtube_object = YouTube(link)
                    print(f"\nAudio Title: {youtube_object.title}\n{'-'*80}")
                    
                    audio_stream = youtube_object.streams.filter(only_audio=True, file_extension="webm").first()
                    
                    if audio_stream:
                        audio_temp_path = os.path.join(self.audio_path, "temp_audio.webm")
                        
                        audio_stream.download(output_path=self.audio_path, filename="temp_audio.webm")
                        
                        output_audio_path = os.path.join(self.audio_path, f"{youtube_object.title}.mp3")
                        
                        subprocess.run(
                            [
                                'ffmpeg', '-y', '-i', audio_temp_path, '-vn', '-codec:a', 'libmp3lame', '-b:a', '320k', output_audio_path
                            ],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL
                        )
                        
                        os.remove(audio_temp_path)
                        
                        print(f"Downloaded and converted: {output_audio_path}")
                    
                    sys.stdout.flush()
                    pbar.update(1)
                    
                sys.stdout.write("\r" + " " * 80 + "\r")
                sys.stdout.flush()
                
            print()
            print("\nAll audios downloaded successfully!")
        else:
            for index, link in enumerate(self.audio_links):
                youtube_object = YouTube(link)
                sys.stdout.write(f"\rDownloading audio {index + 1}/{len(self.audio_links)}: {youtube_object.title}")
                sys.stdout.flush()
                time.sleep(0.5)
            print()
            print("\nAll audios downloaded successfully!")

