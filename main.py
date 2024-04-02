import os.path as path

from download_file_handler import DownloadFileHandler
from time import sleep
from watchdog.observers import Observer


file_path = '/Users/daisyma/Downloads/'
        


if __name__ == "__main__":
    print("program started")
    path = file_path
    event_handler = DownloadFileHandler(file_path=path, threshold=85)
    observer = Observer()
    observer.schedule(event_handler, path)
    observer.start()
    try:
        while True:
            sleep(20)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()