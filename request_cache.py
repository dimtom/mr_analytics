import json
import os.path


class RequestCache:
    cache: dict[str, str] = None
    cache_filename_prefix = '.request_cache'
    cache_filename: str

    def __init__(self, name: str = None):
        self.name = name
        self.cache_filename = f"{self.cache_filename_prefix}{self.name}" if self.name else self.cache_filename_prefix
        self.cache = dict[str, str]()

    def get(self, url: str):
        return self.cache[url] if url in self.cache else None

    def put(self, url: str, response: str):
        self.cache[url] = response

    def clear(self):
        self.cache = {}

    def load(self):
        if not os.path.isfile(self.cache_filename):
            print(
                f"### Cache load - invalid path: {self.cache_filename}")
            return

        if not os.path.exists(self.cache_filename):
            print(
                f"### Cache load - file does not exist: {self.cache_filename}")
            return

        with open(self.cache_filename, 'r') as file:
            data = file.read()
        self.cache = json.loads(data)
        print(f"Request cache, loaded items: {len(self.cache)}")

    def save(self):
        print(f"Request cache - saving to file: {self.cache_filename}")

        data = json.dumps(self.cache)
        with open(self.cache_filename, 'w') as file:
            file.write(data)
            print(
                f"Request cache -  successfully saved items: {len(self.cache)}")
