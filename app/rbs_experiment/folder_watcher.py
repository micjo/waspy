import time
import os
import threading

class FolderWatcher:
    def __init__(self, path):
        self._path = path

    def _run(self):
        while True:
            for file in os.listdir(self._path):
                print(file)
            time.sleep(1)

    def _run_in_background(self):
        task = threading.Thread(target=self._run)
        task.start()



