from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os

class FileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith("balance.txt"):
            print(f"{event.src_path} has been modified!")
            run_my_function()

def run_my_function():
    sum = 0
    print("File changed! Running my function...")
    with open("balance.txt", 'r') as file :
        winnings = file.read().splitlines()
    for i in winnings :
        sum -= int(i)
    with open("total_pl.txt", "w") as pl :
        pl.write(str(sum))

if __name__ == "__main__":
    path = os.path.dirname(os.path.abspath("balance.txt"))  # Get the directory of the file
    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)

    print(f"Watching for changes in {path}\\balance.txt...")
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
