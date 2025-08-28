"""
数据模型类
定义RSS订阅源和订阅条目的数据结构
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class FeedItem:
    """RSS订阅条目"""
    title: str
    link: str
    description: str
    published: Optional[datetime] = None
    author: str = ""
    guid: str = ""
    
    def __str__(self):
        return f"{self.title} - {self.author}"


@dataclass
class Feed:
    """RSS订阅源"""
    title: str
    url: str
    description: str = ""
    link: str = ""
    last_updated: Optional[datetime] = None
    items: List[FeedItem] = None
    
    def __post_init__(self):
        if self.items is None:
            self.items = []
    
    def __str__(self):
        return f"{self.title} ({len(self.items)} items)"


class FeedStore:
    """订阅源存储管理"""
    
    def __init__(self):
        self.feeds: List[Feed] = []
    
    def add_feed(self, feed: Feed) -> bool:
        """添加订阅源"""
        # 检查是否已存在相同URL的订阅源
        for existing_feed in self.feeds:
            if existing_feed.url == feed.url:
                return False
        self.feeds.append(feed)
        return True
    
    def remove_feed(self, url: str) -> bool:
        """移除订阅源"""
        for i, feed in enumerate(self.feeds):
            if feed.url == url:
                del self.feeds[i]
                return True
        return False
    
    def get_feed_by_url(self, url: str) -> Optional[Feed]:
        """根据URL获取订阅源"""
        for feed in self.feeds:
            if feed.url == url:
                return feed
        return None
    
    def get_all_feeds(self) -> List[Feed]:
        """获取所有订阅源"""
        return self.feeds.copy()
    
    def update_feed(self, url: str, updated_feed: Feed) -> bool:
        """更新订阅源"""
        for i, feed in enumerate(self.feeds):
            if feed.url == url:
                self.feeds[i] = updated_feed
                return True
        return False
    
    def clear_all(self) -> bool:
        """清空所有订阅源"""
        if self.feeds:
            self.feeds.clear()
            return True
        return False