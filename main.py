import os.path as path
import time
import logging

from download_file_handler import DownloadFileHandler
from watchdog.observers import Observer


file_path = '/Users/daisyma/Downloads/'
        


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    print("program starts!")
    seconds = time.time()
    path = file_path
    event_handler = DownloadFileHandler(file_path=path, threshold=85)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(10)
            if (time.time() - seconds > 500):
                # clear cache every 500 seconds
                event_handler.file_cache = []
                seconds = time.time()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()