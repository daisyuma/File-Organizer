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
    # return all the similar file entries
    def get_similar_files(self, new_file):
        entries = os.scandir(self.file_path)
        similar_files = []
        for entry in entries:
            if (self.check_file(new_file, entry.name)):
                similar_files.append(entry)
        print(f"similar_files: {similar_files}")
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




        