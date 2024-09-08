# main.py

from gui import RSSReader
from rss_fetcher import RSSFetcher
from data_saver import DataSaver
from data_loader import DataLoader

def main():
    data_saver = DataSaver()
    data_loader = DataLoader()
    app = RSSReader(RSSFetcher.fetch_rss_feed, data_saver, data_loader)
    app.mainloop()

if __name__ == "__main__":
    main()
