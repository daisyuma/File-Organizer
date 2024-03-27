import os
import re
from watchdog.events import FileSystemEventHandler

temp_file_names = [".crdownload", ".com.google.Chrome"]

 # inherits all functions in FileSystemEventHandler
class DownloadFileHandler(FileSystemEventHandler):  
    def __init__(self, file_path, threshold):
        self.file_path = file_path
        self.threshold = threshold
        
    def on_modified(self, event):
        src_path = event.src_path
        if (any(name in src_path for name in temp_file_names) or self.file_path == src_path):
            print("ignored")
            return
        print(f"new file -  {src_path} created!")


    # get all the files in the directory and check for similary with src_path
    # return all the similar file names
    #TODO: implement!!
    def get_similar_files(self, src_path):
        entries = os.scandir(self.file_path)
        similar_files = []
        for entry in entries:
            if (self.check_file(src_path, entry.name)):
                similar_files.append(entry)
        return similar_files

    
    # use fuzzy string matching to compare two file paths
    # if similarity is > threshold, return true
    #TODO: add fuzzy match implementation
    def check_file(self, path_1, path_2):
        return True


        