"""
测试HTML内容清理功能
"""

from feed_manager import FeedManager

def test_css_cleaning():
    """测试CSS代码清理功能"""
    print("测试HTML内容清理功能...")
    
    manager = FeedManager()
    
    # 测试包含CSS代码的HTML内容（模拟问题场景）
    test_html = """
    <p>我的创业搭档姚老师的提示词合集。基本都是实战检验过的提示词，而且离日常工作和商业非常近。强烈推荐收藏，GEO生成提示词也在里面。地址见评论区</p>
    
    <p>#ffffff; border: 1px solid #e1e8ed; padding: 0; line-height: 1.5;"></p>
    
    <div>#0f1419; margin-bottom: 16px; white-space: pre-wrap;">我的创业搭档姚老师的提示词合集。</div>
    
    <p>基本都是实战检验过的提示词，而且离日常工作和商业非常近。</p>
    
    <p>强烈推荐收藏，GEO生成提示词也在里面。</p>
    
    <p>地址见评论区</p>
    
    <div>#e1e8ed; overflow: hidden;"></div>
    
    <img src="https://example.com/image.jpg" alt="测试图片">
    
    <a href="https://example.com">测试链接</a>
    """
    
    print("\\n原始HTML内容:")
    print("-" * 50)
    print(test_html)
    
    # 清理HTML内容
    cleaned_html = manager._clean_and_enhance_html(test_html)
    
    print("\\n清理后的HTML内容:")
    print("-" * 50)
    print(cleaned_html)
    
    # 检查清理效果
    print("\\n清理效果检查:")
    print("-" * 50)
    
    if '#ffffff' not in cleaned_html and '#e1e8ed' not in cleaned_html:
        print("✓ CSS颜色代码已清除")
    else:
        print("✗ CSS颜色代码未完全清除")
    
    if 'border:' not in cleaned_html and 'padding:' not in cleaned_html:
        print("✓ CSS属性代码已清除")
    else:
        print("✗ CSS属性代码未完全清除")
    
    if 'target="_blank"' in cleaned_html:
        print("✓ 链接新窗口属性已添加")
    else:
        print("✗ 链接新窗口属性未添加")
    
    if 'loading="lazy"' in cleaned_html:
        print("✓ 图片懒加载属性已添加")
    else:
        print("✗ 图片懒加载属性未添加")
    
    # 检查内容完整性
    if "我的创业搭档姚老师的提示词合集" in cleaned_html:
        print("✓ 核心内容保持完整")
    else:
        print("✗ 核心内容可能被误删")

def test_real_feed_content():
    """测试真实RSS订阅源的内容清理"""
    print("\\n\\n测试真实RSS内容清理...")
    print("-" * 50)
    
    manager = FeedManager()
    feeds = manager.get_all_feeds()
    
    if not feeds:
        print("⚠ 暂无RSS订阅源数据")
        return
    
    # 查找包含问题HTML的条目
    problem_found = False
    for feed in feeds:
        for item in feed.items:
            if item.description and ('#' in item.description or 'border:' in item.description or 'padding:' in item.description):
                print(f"发现包含CSS代码的条目: {item.title}")
                print(f"订阅源: {feed.title}")
                print(f"原始内容长度: {len(item.description)}")
                
                # 重新清理内容
                cleaned = manager._clean_and_enhance_html(item.description)
                print(f"清理后内容长度: {len(cleaned)}")
                
                # 显示部分内容对比
                print("\\n原始内容前200字符:")
                print(repr(item.description[:200]))
                print("\\n清理后内容前200字符:")
                print(repr(cleaned[:200]))
                
                problem_found = True
                break
        if problem_found:
            break
    
    if not problem_found:
        print("✓ 未发现包含CSS代码的条目，或已被成功清理")

def main():
    print("=" * 60)
    print("Twitter RSS订阅管理器 - HTML内容清理测试")
    print("=" * 60)
    
    try:
        test_css_cleaning()
        test_real_feed_content()
        
        print("\\n" + "=" * 60)
        print("✓ HTML清理功能测试完成！")
        print("\\n🔧 清理功能:")
        print("• 移除内联CSS样式代码")
        print("• 过滤CSS属性字符串")
        print("• 清除颜色值代码")
        print("• 保持核心文本内容")
        print("• 增强图片和链接属性")
        
        print("\\n💡 使用建议:")
        print("1. 重新访问之前显示CSS代码的页面")
        print("2. 检查内容是否已正确显示")
        print("3. 如有必要，手动刷新相关订阅源")
        
    except Exception as e:
        print(f"✗ 测试过程中出现错误: {e}")
    
    print("=" * 60)

if __name__ == "__main__":
    main()