import wget
import os
import re
from .notifier import ProgressBar
from concurrent.futures import ThreadPoolExecutor


class Downloader:
    def __init__(
                self, urls, ext, total_segments,
                max_threads, temp_path=".tmp",
                match=r"\/video(\d+)\.ts$"):
        self.urls = urls
        self.ext = ext
        self.total_segments = total_segments
        self.temp_path = temp_path
        self.match = match
        if max_threads is None:
            max_threads = 128
        self.max_threads = os.cpu_count() * max_threads

    def download(self, url, output):
        retries = 0
        while True:
            try:
                wget.download(url, output, bar=None)
                break
            except Exception:
                if retries > 500:
                    break

    def download_worker(self):
        while self.urls.qsize() > 0:
            try:
                url = self.urls.get_nowait()
            except self.urls.empty():
                break
            try:
                current_num = re.search(self.match, url).group(1)
                output = os.path.join(
                    self.temp_path,
                    f"{current_num}{self.ext}")
                self.download(url, output)
            finally:
                self.urls.task_done()

    def start(self, progress=False):
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            if progress:
                executor.submit(ProgressBar(
                                    self.urls,
                                    self.total_segments,
                                    "Download").run)
            for t in range(self.max_threads):
                executor.submit(self.download_worker)
