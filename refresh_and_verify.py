#!/usr/bin/env python3
"""
刷新特定订阅源并验证CSS清理效果
"""

from feed_manager import FeedManager
import time

def main():
    print("正在刷新订阅源并验证CSS清理效果...")
    print("=" * 60)
    
    # 初始化管理器
    fm = FeedManager()
    
    # 目标订阅源URL
    target_feed_url = "https://api.xgo.ing/rss/user/9de19c78f7454ad08c956c1a00d237fe"
    target_item_guid = "1959258871861838124"
    
    print(f"目标订阅源: {target_feed_url}")
    print(f"目标条目ID: {target_item_guid}")
    print()
    
    # 获取当前数据
    print("1. 检查当前数据...")
    feed = fm.get_feed_by_url(target_feed_url)
    if feed:
        print(f"✓ 找到订阅源: {feed.title}")
        print(f"  条目数量: {len(feed.items)}")
        
        # 查找目标条目
        target_item = None
        for item in feed.items:
            if target_item_guid in item.guid:
                target_item = item
                break
        
        if target_item:
            print(f"✓ 找到目标条目: {target_item.title}")
            print(f"  原始内容长度: {len(target_item.description)}")
            
            # 检查是否包含CSS
            css_indicators = ['#ffffff', '#e1e8ed', 'border: 1px solid', 'padding: 0', 'line-height: 1.5']
            found_css = [indicator for indicator in css_indicators if indicator in target_item.description]
            
            if found_css:
                print(f"⚠ 发现CSS代码: {found_css}")
                print("\n2. 刷新订阅源...")
                
                # 刷新订阅源
                success, message = fm.refresh_feed(target_feed_url)
                print(f"刷新结果: {success}")
                print(f"刷新消息: {message}")
                
                if success:
                    print("\n3. 检查刷新后的数据...")
                    
                    # 重新获取数据
                    refreshed_feed = fm.get_feed_by_url(target_feed_url)
                    if refreshed_feed:
                        # 查找目标条目
                        refreshed_item = None
                        for item in refreshed_feed.items:
                            if target_item_guid in item.guid:
                                refreshed_item = item
                                break
                        
                        if refreshed_item:
                            print(f"✓ 找到刷新后的条目: {refreshed_item.title}")
                            print(f"  刷新后内容长度: {len(refreshed_item.description)}")
                            
                            # 检查CSS是否已清理
                            found_css_after = [indicator for indicator in css_indicators if indicator in refreshed_item.description]
                            
                            if found_css_after:
                                print(f"✗ 仍发现CSS代码: {found_css_after}")
                                print("\n📝 内容示例:")
                                print(refreshed_item.description[:200] + "...")
                            else:
                                print("✅ CSS代码已成功清理！")
                                print("\n📝 清理后内容示例:")
                                print(refreshed_item.description[:200] + "...")
                        else:
                            print("✗ 刷新后未找到目标条目")
                    else:
                        print("✗ 刷新后未找到订阅源")
                else:
                    print(f"✗ 刷新失败: {message}")
            else:
                print("✅ 未发现CSS代码，内容已清理")
        else:
            print(f"✗ 未找到目标条目ID: {target_item_guid}")
    else:
        print(f"✗ 未找到订阅源: {target_feed_url}")
    
    print("\n" + "=" * 60)
    print("验证完成！")

if __name__ == "__main__":
    main()