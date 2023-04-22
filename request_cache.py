import json
import os.path


class RequestCache:
    cache: dict[str, str] = None
    request_cache_filename = '.request_cache'

    def __init__(self):
        self.cache = dict[str, str]()

    def get(self, url: str):
        return self.cache[url] if url in self.cache else None

    def put(self, url: str, response: str):
        self.cache[url] = response

    def clear(self):
        self.cache = {}

    def load(self):
        if not os.path.isfile(self.request_cache_filename):
            print(
                f"### Cache load - invalid path: {self.request_cache_filename}")
            return

        if not os.path.exists(self.request_cache_filename):
            print(
                f"### Cache load - file does not exist: {self.request_cache_filename}")
            return

        with open(self.request_cache_filename, 'r') as file:
            data = file.read()
        self.cache = json.loads(data)
        print(f"Request cache, loaded items: {len(self.cache)}")

    def save(self):
        print(f"Request cache - saving to file: {self.request_cache_filename}")

        data = json.dumps(self.cache)
        with open(self.request_cache_filename, 'w') as file:
            file.write(data)
            print(
                f"Request cache -  successfully saved items: {len(self.cache)}")
