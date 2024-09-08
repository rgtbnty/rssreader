# gui.py

import tkinter as tk
from tkinter import scrolledtext
from rss_fetcher import RSSFetcher
from data_saver import DataSaver
from data_loader import DataLoader
import html
import re

class RSSReader(tk.Tk):
    def __init__(self, fetch_feed_callback, data_saver, data_loader):
        super().__init__()

        self.title("RSS Reader")
        self.geometry("1000x600")  # ウィンドウサイズを変更

        self.data_saver = data_saver
        self.data_loader = data_loader
        self.fetch_feed_callback = fetch_feed_callback

        self.font_size = 12  # 初期フォントサイズ

        # GUIコンポーネントの作成
        self.url_label = tk.Label(self, text="RSS Feed URL:")
        self.url_label.pack(pady=5)

        self.url_entry = tk.Entry(self, width=80)
        self.url_entry.pack(pady=5)

        self.fetch_button = tk.Button(self, text="Fetch", command=self.fetch_feed)
        self.fetch_button.pack(pady=5)

        self.font_size_label = tk.Label(self, text="Font Size:")
        self.font_size_label.pack(pady=5)

        # フォントサイズエントリーとボタンのためのフレームを作成
        self.font_frame = tk.Frame(self)
        self.font_frame.pack(pady=5)

        self.font_size_entry = tk.Entry(self.font_frame, width=5)
        self.font_size_entry.insert(0, str(self.font_size))
        self.font_size_entry.bind("<Return>", self.apply_font_size)  # エンターキーでフォントサイズを適用
        self.font_size_entry.grid(row=0, column=0, padx=5)

        self.increase_font_button = tk.Button(self.font_frame, text="Increase Font", command=self.increase_font_size)
        self.increase_font_button.grid(row=0, column=1, padx=5)

        self.decrease_font_button = tk.Button(self.font_frame, text="Decrease Font", command=self.decrease_font_size)
        self.decrease_font_button.grid(row=0, column=2, padx=5)

        self.text_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, height=20, font=("Arial", self.font_size))
        self.text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.load_saved_data()

    def fetch_feed(self):
        """ユーザーが指定したURLからRSSフィードを取得し、テキストエリアに表示するメソッド"""
        url = self.url_entry.get()
        entries = self.fetch_feed_callback(url)
        self.data_saver.save_url(url)
        self.data_saver.save_entries(entries)
        self.display_entries(entries)

    def clean_html(self, text):
        """HTMLタグを取り除き、1文だけを返す"""
        text = html.unescape(text)  # HTMLエンティティをデコード
        text = re.sub(r'<[^>]+>', '', text)  # HTMLタグを取り除く
        sentences = text.split('.')  # ピリオドで分割
        return sentences[0] + '.' if sentences else ''  # 最初の文を返す

    def display_entries(self, entries):
        """エントリをテキストエリアに表示"""
        self.text_area.delete(1.0, tk.END)  # 以前のエントリをクリア

        for entry in entries:
            self.text_area.insert(tk.END, f"Title: {entry.title}\n")
            self.text_area.insert(tk.END, f"Link: {entry.link}\n")
            self.text_area.insert(tk.END, f"Published: {entry.published}\n")
            summary = self.clean_html(entry.summary)  # HTMLタグを取り除き、1文だけを取得
            self.text_area.insert(tk.END, f"Summary: {summary}\n")
            self.text_area.insert(tk.END, "-"*40 + "\n")

    def load_saved_data(self):
        """保存されたデータを読み込んで表示"""
        url = self.data_loader.load_url()
        entries = self.data_loader.load_entries()
        if url and entries:
            self.url_entry.insert(0, url)
            self.display_entries(entries)

    def apply_font_size(self, event=None):
        """数値フィールドからフォントサイズを適用"""
        try:
            size = int(float(self.font_size_entry.get()))  # フォントサイズを整数に変換
            if size > 0:
                self.font_size = size
                self.text_area.config(font=("Arial", self.font_size))
                self.font_size_entry.delete(0, tk.END)
                self.font_size_entry.insert(0, str(self.font_size))
        except ValueError:
            pass

    def increase_font_size(self):
        """フォントサイズを1ポイント増加"""
        self.font_size += 1
        self.font_size_entry.delete(0, tk.END)
        self.font_size_entry.insert(0, str(self.font_size))
        self.text_area.config(font=("Arial", self.font_size))

    def decrease_font_size(self):
        """フォントサイズを1ポイント減少"""
        if self.font_size > 1:  # フォントサイズが1未満にならないように
            self.font_size -= 1
            self.font_size_entry.delete(0, tk.END)
            self.font_size_entry.insert(0, str(self.font_size))
            self.text_area.config(font=("Arial", self.font_size))
