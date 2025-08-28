from feed_manager import FeedManager

print("刷新订阅源...")
fm = FeedManager()
success, msg = fm.refresh_feed('https://api.xgo.ing/rss/user/9de19c78f7454ad08c956c1a00d237fe')
print(f"刷新结果: {success}, {msg}")

print("\n检查刷新后的内容...")
feed = fm.get_feed_by_url('https://api.xgo.ing/rss/user/9de19c78f7454ad08c956c1a00d237fe')
if feed:
    target_item = next((i for i in feed.items if '1959258871861838124' in i.guid), None)
    if target_item:
        css_indicators = ['#ffffff', '#e1e8ed', 'border: 1px solid', 'padding: 0']
        found_css = [ind for ind in css_indicators if ind in target_item.description]
        
        print(f"内容长度: {len(target_item.description)}")
        print(f"发现CSS代码: {found_css}")
        
        if not found_css:
            print("✅ CSS代码已成功清理！")
        else:
            print("⚠ 仍有CSS代码存在")
            
        print(f"\n内容前200字符:")
        print(repr(target_item.description[:200]))
    else:
        print("未找到目标条目")
else:
    print("未找到订阅源")