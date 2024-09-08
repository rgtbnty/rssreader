import tkinter as tk
from tkinter import scrolledtext
import feedparser

def fetch_rss_feed(url):
    feed = feedparser.parse(url)
    entries = feed.entries
    return entries

class RSSReader(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("RSS Reader")
        self.geometry("600x400")

        self.url_label = tk.Label(self, text="RSS Feed URL:")
        self.url_label.pack(pady=5)

        self.url_entry = tk.Entry(self, width=80)
        self.url_entry.pack(pady=5)

        self.fetch_button = tk.Button(self, text="Fetch", command=self.fetch_feed)
        self.fetch_button.pack(pady=5)

        self.text_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, height=15)
        self.text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def fetch_feed(self):
        url = self.url_entry.get()
        entries = fetch_rss_feed(url)
        
        self.text_area.delete(1.0, tk.END)  # Clear previous entries

        for entry in entries:
            self.text_area.insert(tk.END, f"Title: {entry.title}\n")
            self.text_area.insert(tk.END, f"Link: {entry.link}\n")
            self.text_area.insert(tk.END, f"Published: {entry.published}\n")
            self.text_area.insert(tk.END, f"Summary: {entry.summary}\n")
            self.text_area.insert(tk.END, "-"*40 + "\n")

if __name__ == "__main__":
    app = RSSReader()
    app.mainloop()
