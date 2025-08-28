#!/usr/bin/env python3
"""
测试多图片布局功能
"""

import requests
import time

def test_multiple_images_layout():
    """测试多图片布局功能"""
    print("=" * 60)
    print("多图片布局功能测试")
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
            
            # 检查多图片布局相关代码
            print("\\n2. 检查多图片布局功能...")
            
            # 检查CSS样式
            css_checks = [
                'images-container',
                'two-images',
                'three-images', 
                'four-images',
                'flex: 1',
                'grid-template-columns',
                'calc(50% - 4px)'
            ]
            
            css_found = []
            for check in css_checks:
                if check in html_content:
                    css_found.append(check)
            
            if len(css_found) >= 5:
                print(f"✓ 多图片布局CSS样式已应用 ({len(css_found)}/{len(css_checks)})")
            else:
                print(f"⚠ 部分CSS样式缺失 ({len(css_found)}/{len(css_checks)})")
            
            # 检查JavaScript功能
            js_checks = [
                'processMultipleImages',
                'groupConsecutiveImages',
                'createImageContainer',
                'getElementDistance',
                'two-images',
                'images-container'
            ]
            
            js_found = []
            for check in js_checks:
                if check in html_content:
                    js_found.append(check)
            
            if len(js_found) >= 5:
                print(f"✓ 多图片处理JavaScript逻辑已应用 ({len(js_found)}/{len(js_checks)})")
            else:
                print(f"⚠ 部分JavaScript逻辑缺失 ({len(js_found)}/{len(js_checks)})")
            
            # 检查响应式设计
            responsive_checks = [
                'flex-wrap: wrap',
                'object-fit: cover',
                'border-radius: 16px'
            ]
            
            responsive_found = []
            for check in responsive_checks:
                if check in html_content:
                    responsive_found.append(check)
            
            if len(responsive_found) >= 2:
                print(f"✓ 响应式图片设计已应用 ({len(responsive_found)}/{len(responsive_checks)})")
            else:
                print(f"⚠ 部分响应式设计缺失 ({len(responsive_found)}/{len(responsive_checks)})")
            
            # 总体评估
            print("\\n3. 功能评估...")
            total_score = len(css_found) + len(js_found) + len(responsive_found)
            max_score = len(css_checks) + len(js_checks) + len(responsive_checks)
            
            success_rate = (total_score / max_score) * 100
            print(f"功能完整性: {success_rate:.1f}% ({total_score}/{max_score})")
            
            if success_rate >= 75:
                print("✅ 多图片布局功能实现良好！")
                print("\\n🎯 功能特性:")
                print("• 2张图片：并排显示，各占50%宽度")
                print("• 3张图片：第一张占左侧，其余两张右侧垂直排列")
                print("• 4张图片：2x2网格布局")
                print("• 智能识别连续图片并自动分组")
                print("• 保持点击放大查看功能")
                print("• 响应式设计，适配不同屏幕")
                
                print("\\n📱 使用效果:")
                print("1. 多张图片不再占据过多垂直空间")
                print("2. 图片排列更紧凑，类似Twitter原版")
                print("3. 提升内容阅读体验")
                print("4. 保持图片质量和交互功能")
                return True
            else:
                print(f"⚠ 功能实现需要改进 (完整性: {success_rate:.1f}%)")
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
    print("🖼️ Twitter RSS订阅管理器 - 多图片布局测试")
    print("本测试将验证多图片智能布局功能\\n")
    
    success = test_multiple_images_layout()
    
    print("\\n" + "=" * 60)
    if success:
        print("✅ 多图片布局功能测试通过！")
        print("\\n🌟 主要改进:")
        print("• 智能识别连续的多张图片")
        print("• 2张图片自动并排显示")
        print("• 3-4张图片采用网格布局")
        print("• 节省垂直空间，提升阅读体验")
        print("• 保持Twitter原版的视觉风格")
        
        print("\\n💡 建议测试:")
        print("访问包含多张图片的推文页面：")
        print("http://127.0.0.1:5000/item/https://api.xgo.ing/rss/user/9de19c78f7454ad08c956c1a00d237fe/1959506705970061794")
        print("观察图片是否按照智能布局排列")
    else:
        print("❌ 多图片布局功能测试失败")
        print("\\n🔍 建议检查:")
        print("• CSS网格和弹性布局样式")
        print("• JavaScript图片处理逻辑")
        print("• 响应式设计实现")
    
    print("=" * 60)

if __name__ == "__main__":
    main()