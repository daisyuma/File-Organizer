import os
import re

from numpy import loadtxt
from watchdog.events import FileSystemEventHandler
from thefuzz import fuzz
from pathlib import Path

temp_file_names = [".crdownload", ".com.google.Chrome"]

 # inherits all functions in FileSystemEventHandler
class DownloadFileHandler(FileSystemEventHandler):  
    def __init__(self, file_path, threshold):
        self.file_path = file_path
        self.threshold = threshold
        
    def on_modified(self, event):
        src_path = event.src_path
        if (any(name in src_path for name in temp_file_names) or self.file_path == src_path):
            # ignore temporary files
            print("ignored")
            return
        print(f"new file -  {src_path} created!")
        file_name = self.get_filename(src_path)
        if (self.is_folder_created == ""): #folder has not been created
            similar_files = self.get_similar_files(file_name)
            keyword = self.get_keyword(similar_files)
            self.create_folder(keyword)
            return
            
    # create a folder in the directory with folder_name
    def create_folder(self, folder_name):
        # ensure first letter is upper case
        folder_name = folder_name.capitalize()
        Path(self.file_path + folder_name).mkdir(parents=True, exist_ok=True)
        return


    # read all newly created folders from new_folders.txt and store it in an array. return this array
    def read_folders(self):
        folders = loadtxt("new_folders.txt", delimiter=",", dtype=str)
        return folders


    # checks if a sub folder is already created for this file
    # loops through all newly created folder in new_folders.txt and check its content for similarity
    # similarity between a file and a folder is determined by:
    # average fuzz similarity score between new file and each existing file in the directory 
    # if avg score > threshold -> belongs to that folder 
    # if there is no such folder return an empty string
    #TODO return the HIGHEST folder similarity score
    def is_folder_created(self, new_file):
        new_folders = self.read_folders()
        print(f"new_folders: {new_folders}")
        for folder in new_folders:
            similarity_score = 0
            folder_size = 0
            entries = os.scandir(self.file_path + folder)
            for entry in entries:
                similarity_score += fuzz.ratio(entry.name, new_file)
                folder_size += 1
            if (similarity_score / folder_size > self.threshold):
                return folder    
        return ""


    
    # get all the files in the directory and check for similary with new_file
    # return all the similar file entries
    def get_similar_files(self, new_file):
        entries = os.scandir(self.file_path)
        similar_files = []
        for entry in entries:
            if (self.check_similarity(new_file, entry.name)):
                similar_files.append(entry)
        print(f"similar_files: {similar_files}")
        return similar_files

    
    # use fuzzy string matching to compare two file paths
    # if similarity is > threshold, return true
    def check_similarity(self, file_1, file_2):
        similarity = fuzz.ratio(file_1, file_2)
        print(f"Similarity score {file_1} | {file_2}: {similarity}")
        return similarity >= self.threshold
    
    # extract file name from the full path in src_path
    def get_filename(self, src_path):
        result = src_path.split(self.file_path)[1]
        print(f"file name: {result}")
        return result
    
    # extract keyword from a list of similar file names
    # finds the most common substring and returns it
    # remove non-alphanumeric characters at beginning or end
    def get_keyword(self, similar_files):
        n = len(similar_files)
        # use first filename as reference
        s = similar_files[0].name
        l = len(s)
        result = ""
        for i in range(l): 
            for j in range(i + 1, l + 1):
                # generate all possible substrings from s
                substr = s[i:j]
                common_files = 1
                for k in range(1, n):
                    # Check if the substring is common to filenames
                    if substr not in similar_files[k].name:
                        break
                    else:
                        common_files += 1   
                # If current substring is present in all filenames and is longer than current result
                if (common_files == n and len(result) < len(substr)):
                    result = substr
            # remove non-alphanumeric characters from beginning or end
        result = re.sub(r"^\W+|\W+$", "", result)
        return result




        