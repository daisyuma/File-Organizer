import os, errno
import re
import shutil
import filecmp

from numpy import loadtxt
from watchdog.events import FileSystemEventHandler
from thefuzz import fuzz
from pathlib import Path
from shutil import move

temp_file_names = [".crdownload", ".com.google.Chrome", ".DS_Store"]
newly_created_folders = "new_folders.txt"

 # inherits all functions in FileSystemEventHandler
class DownloadFileHandler(FileSystemEventHandler):  
    file_cache = set()
    def __init__(self, file_path, threshold):
        self.file_path = file_path
        self.threshold = threshold
        
    def on_modified(self, event):
        src_path = event.src_path
        if (any(name in src_path for name in temp_file_names) or src_path in self.file_path or src_path in self.file_cache):
            # ignore temporary files
            return
        print(f"new file -  {src_path} downloaded!")
        file_name = self.get_filename(src_path)
        similar_files = self.get_similar_files(file_name)
        self.file_cache.add(src_path)
        if (len(similar_files) > 1): # if there are multiple similar files that need to be organized
            print(f"similar files: {similar_files} found in {self.file_path}")
            keyword = self.get_keyword(similar_files)
            dest_folder = self.file_path + keyword
            is_folder_created = self.is_folder_created(file_name)
            try:
                if (is_folder_created == ""): #folder has not been created
                    self.create_folder(keyword)
                    print(f"new folder {dest_folder} created!")
                    self.move_files(similar_files, dest_folder)
                    #write new folder name to new_folders.txt
                    self.write_folder(keyword)
                else: #folder is already created, move file to this folder
                    self.move_files([src_path], dest_folder)
                print(f"{file_name} organized into {dest_folder}")
            except shutil.Error as e:
                duplicate_file = self.extract_duplicate_file(e.args[0], dest_folder)
                # print(f"duplicate file: {duplicate_file}")
                if (filecmp.cmp(self.file_path + duplicate_file, dest_folder + "/" + duplicate_file)):
                    # print("line 46")
                    inp = input(f"duplicate files {duplicate_file} found in {self.file_path} and {dest_folder}, delete the one in Downloads? [y]/[n]\n")
                    while (inp not in ["y", "n"]):
                        print("please input one of [y] or [n]")
                        inp = input()
                    if (inp == 'y'):
                        self.remove_file(self.file_path + duplicate_file)
                        print(f"{self.file_path + duplicate_file} deleted")   
        else:
            print("this is the first file of its kind, nothing to organize yet")   
        return
    
    def extract_duplicate_file(self, err_msg, dest_folder):
        duplicate_filename = re.sub(rf"^Destination path '{dest_folder}/|' already exists$", "", err_msg)
        return duplicate_filename

    def remove_file(self, file_name):
        try:
            os.remove(file_name)
        except OSError as e: 
            if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
                raise # re-raise exception if a different error occurred
    
    # append newly created folder name to the end of new_folders.txt
    # use ',' as delimiter
    def write_folder(self, folder_name):
        with open(newly_created_folders, "a") as fp:
            fp.write(folder_name + ',')
    
    # move all file entries to dest if dest exists   
    # if does not exist, throw an error          
    def move_files(self, entries, dest):
        if os.path.exists(dest):
            for entry in entries:
                move(entry, dest)
    
    # create a folder in the directory with folder_name
    def create_folder(self, folder_name):
        # ensure first letter is upper case
        folder_name = folder_name.capitalize()
        Path(self.file_path + folder_name).mkdir(parents=True, exist_ok=True)
        return 


    # read all newly created folders from new_folders.txt and store it in an array. return this array
    def read_folders(self):
        folders = loadtxt(newly_created_folders, delimiter=",", dtype=str)
        return folders


    # checks if a sub folder is already created for this file
    # loops through all newly created folder in new_folders.txt and check its content for similarity
    # similarity between a file and a folder is determined by:
    # average fuzz similarity score between new file and each existing file in the directory 
    # if avg score > threshold -> belongs to that folder 
    # if there is no such folder return an empty string
    # this function lazily returns the first similar folder it finds, not necessarily the MOST similar
    def is_folder_created(self, new_file):
        new_folders = self.read_folders()
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
        # print(f"similar_files: {similar_files}")
        return similar_files

    
    # use fuzzy string matching to compare two file paths
    # if similarity is > threshold, return true
    def check_similarity(self, file_1, file_2):
        similarity = fuzz.ratio(file_1, file_2)
        return similarity >= self.threshold
    
    # extract file name from the full path in src_path
    def get_filename(self, src_path):
        result = src_path.split(self.file_path)[1]
        # print(f"file name: {result}")
        return result
    
    # extract keyword from a list of similar file names
    # finds the most common substring and returns it
    # remove non-alphanumeric characters at beginning or end
    def get_keyword(self, similar_files):
        #need to convert all file names to lower case for accurate keyword
        similar_files = [s.name.lower() for s in similar_files]
        n = len(similar_files)
        # use first filename as reference
        s = similar_files[0]
        l = len(s)
        result = ""
        for i in range(l): 
            for j in range(i + 1, l + 1):
                # generate all possible substrings from s
                substr = s[i:j]
                common_files = 1
                for k in range(1, n):
                    # Check if the substring is common to filenames
                    if substr not in similar_files[k]:
                        break
                    else:
                        common_files += 1   
                # If current substring is present in all filenames and is longer than current result
                if (common_files == n and len(result) < len(substr)):
                    result = substr
            # remove non-alphanumeric characters from beginning or end
        result = re.sub(r"^\W+|\W+$", "", result)
        return result
        