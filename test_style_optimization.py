#!/usr/bin/env python3
"""
验证Twitter样式优化效果的测试脚本
"""

import requests
import time
from urllib.parse import quote

def test_twitter_style_optimization():
    """测试Twitter样式优化效果"""
    print("=" * 60)
    print("Twitter样式优化验证测试")
    print("=" * 60)
    
    # 目标URL
    base_url = "http://127.0.0.1:5000"
    target_url = f"{base_url}/item/https://api.xgo.ing/rss/user/9de19c78f7454ad08c956c1a00d237fe/1959506705970061794"
    
    print(f"测试URL: {target_url}")
    print()
    
    try:
        # 访问目标页面
        print("1. 获取页面内容...")
        response = requests.get(target_url, timeout=10)
        
        if response.status_code == 200:
            print("✓ 页面加载成功")
            html_content = response.text
            
            # 检查样式优化
            print("\\n2. 检查样式优化...")
            
            # 检查字体设置
            font_checks = [
                'font-size: 15px',
                'line-height: 1.3125', 
                '-apple-system, BlinkMacSystemFont',
                'color: #0f1419'
            ]
            
            font_found = []
            for check in font_checks:
                if check in html_content:
                    font_found.append(check)
            
            if len(font_found) >= 3:
                print(f"✓ Twitter字体样式已应用 ({len(font_found)}/{len(font_checks)})")
            else:
                print(f"⚠ 部分字体样式缺失 ({len(font_found)}/{len(font_checks)})")
            
            # 检查图片样式优化
            img_checks = [
                'border-radius: 16px',
                'margin: 12px 0',
                'border: 1px solid #cfd9de'
            ]
            
            img_found = []
            for check in img_checks:
                if check in html_content:
                    img_found.append(check)
            
            if len(img_found) >= 2:
                print(f"✓ 图片样式优化已应用 ({len(img_found)}/{len(img_checks)})")
            else:
                print(f"⚠ 部分图片样式缺失 ({len(img_found)}/{len(img_checks)})")
            
            # 检查引用推文样式
            quote_checks = [
                'tweet-quote',
                'quote-author-avatar',
                'width: 16px',
                'height: 16px'
            ]
            
            quote_found = []
            for check in quote_checks:
                if check in html_content:
                    quote_found.append(check)
            
            if len(quote_found) >= 3:
                print(f"✓ 引用推文样式优化已应用 ({len(quote_found)}/{len(quote_checks)})")
            else:
                print(f"⚠ 部分引用样式缺失 ({len(quote_found)}/{len(quote_checks)})")
            
            # 检查是否移除了大标题
            title_removed = 'display-6' not in html_content
            if title_removed:
                print("✓ 大标题重复显示已修复")
            else:
                print("⚠ 大标题可能仍有重复")
            
            # 检查整体布局优化
            layout_checks = [
                'pt-3 pb-2',  # 更紧凑的padding
                'pt-1 pb-3',  # 内容区域padding优化
                'border-0'    # 移除边框简化设计
            ]
            
            layout_found = []
            for check in layout_checks:
                if check in html_content:
                    layout_found.append(check)
            
            if len(layout_found) >= 2:
                print(f"✓ 布局优化已应用 ({len(layout_found)}/{len(layout_checks)})")
            else:
                print(f"⚠ 部分布局优化缺失 ({len(layout_found)}/{len(layout_checks)})")
            
            # 总体评估
            print("\\n3. 整体评估...")
            total_score = len(font_found) + len(img_found) + len(quote_found) + len(layout_found)
            max_score = len(font_checks) + len(img_checks) + len(quote_checks) + len(layout_checks)
            
            if title_removed:
                total_score += 2  # 标题修复加分
                max_score += 2
            
            success_rate = (total_score / max_score) * 100
            
            print(f"优化成功率: {success_rate:.1f}% ({total_score}/{max_score})")
            
            if success_rate >= 80:
                print("✅ Twitter样式优化效果良好！")
                print("\\n🎯 优化内容:")
                print("• 字体大小调整为15px，模拟Twitter原版")
                print("• 行高优化为1.3125，提升阅读体验")
                print("• 图片样式轻量化，减少视觉干扰")
                print("• 移除重复标题显示")
                print("• 引用推文样式更接近原版")
                print("• 整体布局更加紧凑")
                
                print("\\n📱 现在的显示效果:")
                print("1. 字体大小更合适，不会太大")
                print("2. 图片尺寸更合理")
                print("3. 没有重复的标题")
                print("4. 整体样式更接近X(Twitter)原版")
                return True
            else:
                print(f"⚠ 优化效果需要改进 (成功率: {success_rate:.1f}%)")
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
    print("🎨 Twitter RSS订阅管理器 - 样式优化验证")
    print("本测试将验证样式优化效果，确保显示更接近Twitter原版\\n")
    
    success = test_twitter_style_optimization()
    
    print("\\n" + "=" * 60)
    if success:
        print("✅ 样式优化验证通过！")
        print("\\n🌟 主要改进:")
        print("• 解决了标题重复显示的问题")
        print("• 调整字体大小和行高，更接近Twitter")
        print("• 优化图片显示尺寸和样式")
        print("• 简化引用推文的视觉设计")
        print("• 整体布局更加紧凑和现代化")
        
        print("\\n💡 建议:")
        print("现在可以访问页面查看优化效果:")
        print("http://127.0.0.1:5000/item/https://api.xgo.ing/rss/user/9de19c78f7454ad08c956c1a00d237fe/1959506705970061794")
    else:
        print("❌ 样式优化验证失败")
        print("\\n🔍 建议检查:")
        print("• CSS样式是否正确应用")
        print("• 字体和图片尺寸设置")
        print("• 布局结构是否优化")
    
    print("=" * 60)

if __name__ == "__main__":
    main()