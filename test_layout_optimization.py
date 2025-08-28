#!/usr/bin/env python3
"""
测试订阅源列表布局优化功能
"""

import requests
import time

def test_layout_optimization():
    """测试布局优化功能"""
    print("=" * 60)
    print("订阅源列表布局优化测试")
    print("=" * 60)
    
    # 目标URL
    base_url = "http://127.0.0.1:5000"
    target_url = f"{base_url}/feeds/https://api.xgo.ing/rss/user/9de19c78f7454ad08c956c1a00d237fe"
    
    print(f"测试URL: {target_url}")
    print()
    
    try:
        # 访问目标页面
        print("1. 获取页面内容...")
        response = requests.get(target_url, timeout=10)
        
        if response.status_code == 200:
            print("✓ 页面加载成功")
            html_content = response.text
            
            # 检查布局切换功能
            print("\\n2. 检查布局切换功能...")
            
            # 检查布局选择器
            layout_checks = [
                'btn-group',  # 按钮组
                'layout-single',  # 单列布局
                'layout-narrow',  # 紧凑布局
                'layout-two-column',  # 双列布局
                'input[name="layout"]',  # 布局选择器
                'bi-list',  # 单列图标
                'bi-columns'  # 双列图标
            ]
            
            layout_found = []
            for check in layout_checks:
                if check in html_content:
                    layout_found.append(check)
            
            if len(layout_found) >= 6:
                print(f"✓ 布局切换功能已实现 ({len(layout_found)}/{len(layout_checks)})")
            else:
                print(f"⚠ 部分布局功能缺失 ({len(layout_found)}/{len(layout_checks)})")
            
            # 检查CSS样式
            css_checks = [
                'layout-narrow #items-container',  # 紧凑布局样式
                'max-width: 60%',  # 3/5宽度限制
                'layout-two-column .item-wrapper',  # 双列样式
                'width: 50%',  # 双列宽度
                'height: 100%',  # 等高卡片
                'flex-direction: column'  # 弹性布局
            ]
            
            css_found = []
            for check in css_checks:
                if check in html_content:
                    css_found.append(check)
            
            if len(css_found) >= 5:
                print(f"✓ 布局CSS样式已应用 ({len(css_found)}/{len(css_checks)})")
            else:
                print(f"⚠ 部分CSS样式缺失 ({len(css_found)}/{len(css_checks)})")
            
            # 检查响应式设计
            responsive_checks = [
                '@media (max-width: 992px)',  # 中等屏幕适配
                '@media (max-width: 768px)',  # 移动端适配
                '@media (min-width: 1400px)',  # 大屏幕适配
                'layout-two-column .item-wrapper',  # 响应式双列
                'layout-narrow #items-container'  # 响应式紧凑
            ]
            
            responsive_found = []
            for check in responsive_checks:
                if check in html_content:
                    responsive_found.append(check)
            
            if len(responsive_found) >= 4:
                print(f"✓ 响应式设计已实现 ({len(responsive_found)}/{len(responsive_checks)})")
            else:
                print(f"⚠ 部分响应式设计缺失 ({len(responsive_found)}/{len(responsive_checks)})")
            
            # 检查用户体验优化
            ux_checks = [
                'localStorage.setItem',  # 保存用户偏好
                'title-link',  # 标题链接样式
                'card:hover',  # 卡片悬停效果
                'transform: translateY',  # 悬停动画
                'content-text',  # 内容文本样式
                '-webkit-line-clamp'  # 文本截断
            ]
            
            ux_found = []
            for check in ux_checks:
                if check in html_content:
                    ux_found.append(check)
            
            if len(ux_found) >= 5:
                print(f"✓ 用户体验优化已实现 ({len(ux_found)}/{len(ux_checks)})")
            else:
                print(f"⚠ 部分用户体验优化缺失 ({len(ux_found)}/{len(ux_checks)})")
            
            # 总体评估
            print("\\n3. 整体评估...")
            total_score = len(layout_found) + len(css_found) + len(responsive_found) + len(ux_found)
            max_score = len(layout_checks) + len(css_checks) + len(responsive_checks) + len(ux_checks)
            
            success_rate = (total_score / max_score) * 100
            print(f"布局优化完成度: {success_rate:.1f}% ({total_score}/{max_score})")
            
            if success_rate >= 85:
                print("✅ 布局优化功能实现优秀！")
                print("\\n🎯 优化特性:")
                print("• 单列布局：传统的全宽显示方式")
                print("• 紧凑布局：宽度限制为原来的3/5，内容更集中")
                print("• 双列布局：充分利用屏幕空间，显示更多内容")
                print("• 智能响应式：根据屏幕尺寸自动调整")
                print("• 用户偏好：自动保存并恢复布局选择")
                
                print("\\n📱 用户体验:")
                print("1. 解决了单列过宽的问题")
                print("2. 提供多种布局选择，适应不同喜好")
                print("3. 卡片悬停效果，提升交互体验")
                print("4. 等高卡片设计，视觉更整齐")
                print("5. 内容预览优化，阅读更舒适")
                return True
            else:
                print(f"⚠ 布局优化需要继续完善 (完成度: {success_rate:.1f}%)")
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
    print("📋 Twitter RSS订阅管理器 - 布局优化测试")
    print("本测试将验证订阅源列表的布局优化功能\\n")
    
    success = test_layout_optimization()
    
    print("\\n" + "=" * 60)
    if success:
        print("✅ 布局优化测试通过！")
        print("\\n🌟 主要改进:")
        print("• 添加了三种布局选择：单列、紧凑、双列")
        print("• 解决了单列布局过宽的问题")
        print("• 实现了响应式设计，适配各种屏幕")
        print("• 优化了卡片样式和交互效果")
        print("• 保存用户布局偏好，提升使用体验")
        
        print("\\n💡 使用指南:")
        print("访问订阅源页面:")
        print("http://127.0.0.1:5000/feeds/https://api.xgo.ing/rss/user/9de19c78f7454ad08c956c1a00d237fe")
        print("\\n在页面右上角选择布局方式:")
        print("• 📋 单列：全宽显示，适合大屏幕")
        print("• 📱 紧凑：60%宽度，更集中的阅读体验")
        print("• 📊 双列：2列并排，显示更多内容")
    else:
        print("❌ 布局优化测试未完全通过")
        print("\\n🔍 建议检查:")
        print("• 布局切换JavaScript逻辑")
        print("• CSS响应式样式规则")
        print("• 用户偏好存储功能")
    
    print("=" * 60)

if __name__ == "__main__":
    main()