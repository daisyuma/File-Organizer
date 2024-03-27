import os.path as path

from download_file_handler import DownloadFileHandler
from time import sleep
from watchdog.observers import Observer


file_path = '/Users/daisyma/Downloads'
        


# ! NO NEED TO CHANGE BELOW CODE
if __name__ == "__main__":
    print("program started")
    path = file_path
    event_handler = DownloadFileHandler(file_path=path)
    event_handler.get_files()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            print("line 10")
            sleep(15)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()