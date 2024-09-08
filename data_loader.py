# data_loader.py

import json
import os

class DataLoader:
    def __init__(self, url_file='url.json', entries_file='entries.json'):
        self.url_file = url_file
        self.entries_file = entries_file

    def load_url(self):
        """URLをファイルから読み込む"""
        if not os.path.exists(self.url_file):
            return None
        with open(self.url_file, 'r') as f:
            data = json.load(f)
            return data.get('url')

    def load_entries(self):
        """エントリをファイルから読み込む"""
        if not os.path.exists(self.entries_file):
            return []
        with open(self.entries_file, 'r') as f:
            data = json.load(f)
            return [type('Entry', (), entry) for entry in data]
