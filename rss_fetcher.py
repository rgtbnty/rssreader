# rss_fetcher.py

import feedparser

class RSSFetcher:
    @staticmethod
    def fetch_rss_feed(url):
        """指定されたURLからRSSフィードを取得する"""
        feed = feedparser.parse(url)
        entries = feed.entries
        return entries
