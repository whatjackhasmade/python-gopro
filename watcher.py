import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

import os

def clear_terminal():
    os.system('clear')  # Use 'clear' command to clear the console on macOS and Linux

class MyHandler(FileSystemEventHandler):
    def __init__(self):
        self.initial_run = True

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            print(f"Changes detected in {event.src_path}.")
            if self.initial_run:
                print("Initial run complete. Re-running the script...")
            else:
                print("Re-running the script...")
            clear_terminal()
            subprocess.run([sys.executable, "main.py"])
            self.initial_run = False

if __name__ == "__main__":
    path = "."  # Current directory
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    print("Starting script")
    subprocess.run([sys.executable, "main.py"])
    event_handler.initial_run = False

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
