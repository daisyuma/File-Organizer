import os.path as path
import time

from download_file_handler import DownloadFileHandler
from watchdog.observers import Observer


file_path = '/Users/daisyma/Downloads/'
        


if __name__ == "__main__":
    print("program started")
    path = file_path
    event_handler = DownloadFileHandler(file_path=path, threshold=85)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(10)
            print(f"event handler cache: {event_handler.file_cache}")
    except KeyboardInterrupt:
        observer.stop()
    observer.join()