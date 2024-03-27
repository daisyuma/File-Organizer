import os
import re
from watchdog.events import FileSystemEventHandler
from thefuzz import fuzz

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


    # get all the files in the directory and check for similary with new_file
    # return all the similar file names
    #TODO: implement!!
    def get_similar_files(self, new_file):
        entries = os.scandir(self.file_path)
        similar_files = []
        for entry in entries:
            if (self.check_file(new_file, entry.name)):
                similar_files.append(entry)
        print(similar_files)
        return similar_files

    
    # use fuzzy string matching to compare two file paths
    # if similarity is > threshold, return true
    def check_file(self, file_1, file_2):
        similarity = fuzz.ratio(file_1, file_2)
        print(f"Similarity score {file_1} | {file_2}: {similarity}")
        return similarity >= self.threshold
    
    # extract file name from the full path in src_path
    def get_filename(self, src_path):
        result = src_path.split(self.file_path)[1]
        print(f"file name: {result}")
        return result
    
    #TODO: extract keyword from a list of similar file names
    def get_keyword(self, similar_files):
        return




        