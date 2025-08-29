#!/usr/bin/env python3
"""
刷新RSS数据，更新空的GUID值
"""

import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from feed_manager import FeedManager

def main():
    """刷新所有RSS源的数据"""
    feed_manager = FeedManager()
    
    print("正在刷新所有RSS源...")
    results = feed_manager.refresh_all_feeds()
    
    success_count = 0
    for url, result in results.items():
        if result['success']:
            success_count += 1
            print(f"✓ {url}: {result['message']}")
        else:
            print(f"✗ {url}: {result['message']}")
    
    print(f"\n刷新完成: {success_count}/{len(results)} 个RSS源成功刷新")

if __name__ == "__main__":
    main()