<!-- ABOUT THE PROJECT -->
## Table of contents

* [About This Project](#about-this-project)
    * [Built With](#built-with)
* [Running Script Locally](#running-script-locally)
* [Usage](#usage) 
* [Roadmap](#roadmap)
* [Ackowledgements](#acknowledgments)


## About This Project
Do you often find yourself downloading multiple related or identical documents on the same topic repeatedly, only to have them clutter your Downloads directory and consume valuable disk space? As a student frequently downloading assignment documents and lecture notes, I've certainly encountered this issue, which disrupts the organization of my Downloads folder. 
<img src="media/unorganized_folder.png">
Like the example above, I downloaded multiple files for my CS317 course, which should ideally be organized into the same folder titled "CS317".

To tackle this inconvenience and automate the process, I developed a python script. This script efficiently manages newly downloaded files by automatically gathering similar ones and neatly organizing them into a designated folder. Furthermore, it actively identifies duplicate files and prompts users for deletion, streamlining file management and optimizing disk space usage.

### Built With
* <i class="fa-brands fa-python"></i> Python


## Running Script Locally
1) install [Python 3](https://www.python.org/downloads/)
2) install any missing libraries like watchdog, shutil, thefuzz ...etc
```
$ pip install watchdog shutil thefuzz
```
4) modify the directory you want to organize
5) adjust the similarity `threshold` (1-100) here to specify the level of similarity required for file names to be grouped into the same folder. Notice here we are using **[fuzzy string matching](https://www.datacamp.com/tutorial/fuzzy-string-python)** to determine the closeness of two file names. For example, if I have a series of files named: *CPSC317-01-Intro.pdf, CPSC317-02-Security.pdf, CPSC317-03-Transport.pdf...etc*, then the threshold should probably be set lower than a series of files named *PHIL-lecture1, PHIL-lecture2, PHIL-lecture 3...*
3) in the project directory command line, run 
```
main.py
```

<!-- USAGE EXAMPLES -->
## Usage
<!-- TODO: insert gif of how the program works -->
Here is a video demo of this project!
[https://youtu.be/3MEt3rxmeFc](https://youtu.be/3MEt3rxmeFc)

<!-- ROADMAP -->
## Roadmap

- [x] Find a way to listen to new file downloaded
- [x]  Ignore temporary files created during download (solution:`temp_file_names`)
- [x]  add unit tests
- [x]  deal with duplicate watchdog event when a file is downloaded (solution:`file_cache`)
- [x]  keep track of a list of new folders created in a `.txt` file on disk
- [x]  iterate through the folder to find similar names (need to come up with a way to define “similar”)
    - https://www.alldup.de/alldup_help/search_similar_file_name.php
    - fuzzy match in python: https://www.datacamp.com/tutorial/fuzzy-string-python
- [x]  find a way to extract “keyword”
- [x]  check if folder exists for the file or not
- [x]  if a folder already exists → add that file to folder and check duplicate. if identical file exists ask if user wants to delete
- [x]  ⭐if not exist → create new folder with keyword → move all files with similar name inside
- [x]  test and add try-catch to deal with problems
- [ ] ux improvements(in progress)
- [ ] maybe create a simple UI for this

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

These are some resources I would like to give credit to.