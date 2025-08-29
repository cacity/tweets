#!/usr/bin/env python3
"""
测试URL生成的脚本
"""

import sys
import os

# 添加src目录到Python路径
script_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(script_dir, 'src')
sys.path.insert(0, src_dir)

from flask import url_for
import app

def test_url_generation():
    with app.app.test_request_context():
        # 测试URL生成
        test_feed_url = "https://wechat2rss.bestblogs.dev/feed/8747ed0f8c6cf5c6e94785fff7d8dd6eb8abfe68.xml"
        test_guid = "1959258871861838124"
        
        # 使用url_for生成URL
        generated_url = url_for('view_item', feed_url=test_feed_url, item_guid=test_guid)
        print(f"生成的URL: {generated_url}")
        
        # 手动生成URL用于比较
        manual_url = f"/item?feed_url={test_feed_url}&item_guid={test_guid}"
        print(f"手动生成的URL: {manual_url}")

if __name__ == "__main__":
    test_url_generation()
