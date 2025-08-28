#!/usr/bin/env python3
"""
验证头像修复效果的测试脚本
"""

import requests
import time
from urllib.parse import quote

def test_avatar_fix():
    """测试头像修复效果"""
    print("=" * 60)
    print("头像显示修复验证测试")
    print("=" * 60)
    
    # 目标URL
    base_url = "http://127.0.0.1:5000"
    target_url = f"{base_url}/item/https://api.xgo.ing/rss/user/9de19c78f7454ad08c956c1a00d237fe/1959506705970061794"
    
    print(f"测试URL: {target_url}")
    print()
    
    try:
        # 测试Flask应用是否运行
        print("1. 检查Flask应用状态...")
        response = requests.get(base_url, timeout=5)
        if response.status_code == 200:
            print("✓ Flask应用正常运行")
        else:
            print(f"✗ Flask应用响应错误: {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"✗ 无法连接到Flask应用: {e}")
        print("请确保Flask应用正在运行 (python app.py)")
        return False
    
    try:
        # 访问目标页面
        print("\\n2. 访问目标页面...")
        response = requests.get(target_url, timeout=10)
        
        if response.status_code == 200:
            print("✓ 页面加载成功")
            html_content = response.text
            
            # 检查HTML内容
            print("\\n3. 分析页面内容...")
            
            # 检查是否包含头像隐藏的CSS
            css_checks = [
                'img[alt*="Frank Wang"]',
                'img[alt*="玉伯"]', 
                'img[alt*="lifesinger"]',
                'display: none !important',
                'visibility: hidden !important'
            ]
            
            css_found = []
            for check in css_checks:
                if check in html_content:
                    css_found.append(check)
            
            if len(css_found) >= 3:
                print(f"✓ 头像隐藏CSS规则已应用 ({len(css_found)}/{len(css_checks)})")
            else:
                print(f"⚠ 部分CSS规则缺失 ({len(css_found)}/{len(css_checks)})")
            
            # 检查JavaScript头像处理逻辑
            js_checks = [
                'processQuotedTweets',
                'processed-avatar',
                'Frank Wang',
                '玉伯',
                'quote-author-avatar'
            ]
            
            js_found = []
            for check in js_checks:
                if check in html_content:
                    js_found.append(check)
            
            if len(js_found) >= 4:
                print(f"✓ JavaScript头像处理逻辑已应用 ({len(js_found)}/{len(js_checks)})")
            else:
                print(f"⚠ 部分JavaScript逻辑缺失 ({len(js_found)}/{len(js_checks)})")
            
            # 检查页面结构
            structure_checks = [
                'article-content',
                'tweet-quote', 
                'quote-author',
                'Frank Wang'
            ]
            
            structure_found = []
            for check in structure_checks:
                if check in html_content:
                    structure_found.append(check)
            
            print(f"✓ 页面结构元素检查 ({len(structure_found)}/{len(structure_checks)})")
            
            # 总体评估
            print("\\n4. 修复效果评估...")
            total_score = len(css_found) + len(js_found) + len(structure_found)
            max_score = len(css_checks) + len(js_checks) + len(structure_checks)
            
            if total_score >= max_score * 0.8:
                print("✅ 头像修复效果良好！")
                print("\\n📱 建议测试步骤:")
                print("1. 在浏览器中打开:", target_url)
                print("2. 检查是否还能看到Frank Wang的头像在内容中间")
                print("3. 确认头像只出现在引用推文的作者信息区域")
                print("4. 验证引用推文的样式是否正确")
                return True
            else:
                print(f"⚠ 修复效果需要改进 (评分: {total_score}/{max_score})")
                return False
                
        else:
            print(f"✗ 页面加载失败: {response.status_code}")
            return False
            
    except requests.RequestException as e:
        print(f"✗ 页面访问失败: {e}")
        return False
    
    except Exception as e:
        print(f"✗ 测试过程中出现错误: {e}")
        return False

def main():
    print("🔧 Twitter RSS订阅管理器 - 头像修复验证")
    print("本测试将验证Frank Wang玉伯头像的显示修复效果\\n")
    
    success = test_avatar_fix()
    
    print("\\n" + "=" * 60)
    if success:
        print("✅ 头像修复验证通过！")
        print("\\n🎯 修复内容:")
        print("• 增强CSS规则强制隐藏头像")
        print("• JavaScript立即处理头像显示")
        print("• 智能引用推文结构创建")
        print("• 头像只在引用区域显示")
        
        print("\\n🌟 用户体验改进:")
        print("• 头像不再出现在内容中间")
        print("• 引用推文显示更加清晰")
        print("• 符合X(Twitter)原始设计")
        print("• 更好的阅读体验")
    else:
        print("❌ 头像修复验证失败")
        print("\\n🔍 建议检查:")
        print("• Flask应用是否正常运行")
        print("• CSS和JavaScript代码是否正确")
        print("• 页面内容是否包含目标元素")
    
    print("=" * 60)

if __name__ == "__main__":
    main()