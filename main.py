# importing the module
import threading
import time
from pytube import YouTube
import re

# script for downloading youtube video or audio


##################  parameters  #########################

# link of the video to be downloaded

# type = "audio" or "video"
type = "audio"
# destination folder
output_path = "D:\Music\Downloads"
video_resolution = 0  # 0 for lowest resolution ; 1 for highest resolution





class ytDownloader:
    def __init__(self,link,  output_path , type='audio', video_resolution =0):
        self.type = type
        print('type = ', type)
        self.video_resolution = video_resolution
        self.output_path = output_path
        self.filename = ''
        self.yt = None
        self.stream = None
        self.link = link

    def create(self):
        # object creation using YouTube
        try:
            self.yt = YouTube(self.link)
        except Exception as e:
            print(e)  # to handle exception

        # downloading the video/audio

    def get_stream(self):
        try:
            if type == 'audio':
                self.stream = self.yt.streams.get_audio_only()

            else:
                self.stream = self.yt.streams.get_lowest_resolution() if self.video_resolution==0 else self.yt.streams.get_highest_resolution()

            print("got stream")

        except Exception as e:
            print(e)

    def download(self):

        extension = ".wav" if type == "audio" else ".mp4"
        try :
            self.stream.download(output_path=self.output_path, filename=self.filename + extension)
            print('file saved!')
        except Exception as e:
            print(e)

    def run(self):
        self.create()
        # replace file system error inducing characters
        self.filename = re.sub('\W+', ' ', self.yt.title)
        print("filename : " , self.filename)
        self.get_stream()
        self.download()
    """
    # filter depending on type
    
    if type == "audio" :
        # filters audio files
        audiofiles = yt.streams.filter(only_audio=True)
    else :
        # filters out all the files with "mp4" extension
        mp4files = yt.streams.filter(file_extension='mp4')
    """


# read input file
file1 = open('links.txt', 'r')
links = file1.readlines()

######### single thread
"""print("######### single thread ##################")

start = time.perf_counter()
for link in links :
    downloader = ytDownloader(link, output_path, type )
    downloader.run()
finish = time.perf_counter()

print(f'DONE in {finish - start} secs' )"""



######### multithreading
print("######### multi threading ##################")
start = time.perf_counter()
# start independent threads

pool=[]
for link in links :
    downloader = ytDownloader(link, output_path, type )
    t = threading.Thread(target=downloader.run)
    t.start()
    pool.append(t)

for t in pool :
    t.join()
finish = time.perf_counter()

print(f'DONE in {finish - start} secs')