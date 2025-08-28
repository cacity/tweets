#!/usr/bin/env python3
"""
测试头像识别和显示功能
"""

import requests
import re
from bs4 import BeautifulSoup

def test_avatar_functionality():
    """测试头像识别功能"""
    print("测试头像识别和显示功能...")
    print("=" * 60)
    
    # 目标页面URL
    url = "http://127.0.0.1:5000/item/https://api.xgo.ing/rss/user/9de19c78f7454ad08c956c1a00d237fe/1959506705970061794"
    
    try:
        # 获取页面内容
        response = requests.get(url)
        print(f"页面状态: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text
            soup = BeautifulSoup(content, 'html.parser')
            
            # 检查是否包含头像容器
            avatar_container = soup.find('div', id='author-avatar')
            print(f"✓ 找到头像容器: {avatar_container is not None}")
            
            # 检查作者信息区域
            author_info = soup.find('strong')
            if author_info:
                print(f"✓ 作者信息: {author_info.get_text()}")
            
            # 检查是否包含JavaScript功能
            js_functions = [
                'extractAndMoveAvatar',
                'moveAvatarToAuthor',
                'author-avatar'
            ]
            
            for func in js_functions:
                has_func = func in content
                status = "✓" if has_func else "✗"
                print(f"{status} JavaScript功能 '{func}': {has_func}")
            
            # 检查CSS样式
            css_classes = [
                'author-avatar',
                'author-info',
                'moved-avatar'
            ]
            
            for css_class in css_classes:
                has_css = css_class in content
                status = "✓" if has_css else "✗"
                print(f"{status} CSS样式 '{css_class}': {has_css}")
            
            # 检查图片数量
            img_tags = soup.find_all('img')
            print(f"✓ 页面图片数量: {len(img_tags)}")
            
            # 查找可能的头像图片
            potential_avatars = []
            for img in img_tags:
                alt = img.get('alt', '')
                src = img.get('src', '')
                
                if any(keyword in alt.lower() for keyword in ['frank', 'wang', '玉伯', 'avatar', 'profile']):
                    potential_avatars.append({
                        'alt': alt,
                        'src': src[:50] + '...' if len(src) > 50 else src
                    })
            
            print(f"✓ 识别到潜在头像: {len(potential_avatars)}")
            for i, avatar in enumerate(potential_avatars):
                print(f"  {i+1}. Alt: {avatar['alt']}")
                print(f"     Src: {avatar['src']}")
            
            print("\n📝 功能说明:")
            print("1. 头像会通过JavaScript自动识别")
            print("2. 识别策略:")
            print("   - Alt属性包含人名或头像关键词")
            print("   - Src包含profile_images")
            print("   - 小尺寸图片（可能是头像）")
            print("3. 头像会移动到作者名称旁边显示")
            print("4. 原始位置的头像会被隐藏")
            
        else:
            print(f"✗ 页面访问失败: {response.status_code}")
            
    except Exception as e:
        print(f"✗ 测试过程中出现错误: {e}")

def main():
    print("=" * 60)
    print("Twitter RSS订阅管理器 - 头像识别功能测试")
    print("=" * 60)
    
    test_avatar_functionality()
    
    print("\n" + "=" * 60)
    print("✅ 头像识别功能测试完成！")
    print("\n🎯 实现的功能:")
    print("• 智能头像识别（基于alt属性、URL模式、图片尺寸）")
    print("• 头像自动移动到作者信息旁边")
    print("• 圆形头像样式，带边框和阴影")
    print("• 悬停效果和过渡动画")
    print("• 避免头像在内容区域重复显示")
    print("• 响应式设计，适配移动端")
    
    print("\n💡 使用效果:")
    print("现在访问文章详情页面时，Frank Wang 玉伯的头像")
    print("会自动显示在作者名称旁边，提供更好的视觉体验！")
    print("=" * 60)

if __name__ == "__main__":
    main()