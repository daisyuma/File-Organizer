import os
import re
from watchdog.events import FileSystemEventHandler

temp_file_names = [".crdownload", ".com.google.Chrome"]

 # inherits all functions in FileSystemEventHandler
class DownloadFileHandler(FileSystemEventHandler):  
    def __init__(self, file_path):
        self.file_path = file_path
        
    def on_modified(self, event):
        src_path = event.src_path
        if (any(name in src_path for name in temp_file_names) or self.file_path == src_path):
            print("ignored")
            return
        print(f"new file -  {src_path} created!")
        

    
    def get_files(self):
        entries = os.scandir(self.file_path)
        for entry in entries:
            print(entry)


        