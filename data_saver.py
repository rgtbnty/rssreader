# data_saver.py

import json

class DataSaver:
    def __init__(self, url_file='url.json', entries_file='entries.json'):
        self.url_file = url_file
        self.entries_file = entries_file

    def save_url(self, url):
        """URLをファイルに保存"""
        with open(self.url_file, 'w') as f:
            json.dump({'url': url}, f, indent=4)

    def save_entries(self, entries):
        """エントリをファイルに保存"""
        with open(self.entries_file, 'w') as f:
            data = [{'title': entry.title,
                     'link': entry.link,
                     'published': entry.published,
                     'summary': entry.summary} for entry in entries]
            json.dump(data, f, indent=4)
