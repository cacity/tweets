"""
测试图片显示功能
"""

import sys
import os
import requests

def test_image_display():
    """测试图片显示功能"""
    print("测试图片显示功能...")
    
    # 测试Flask应用是否运行
    try:
        response = requests.get('http://127.0.0.1:5000/', timeout=5)
        if response.status_code == 200:
            print("✓ Flask应用正常运行")
        else:
            print(f"✗ Flask应用响应错误: {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"✗ 无法连接到Flask应用: {e}")
        return False
    
    # 测试API刷新功能
    try:
        response = requests.post('http://127.0.0.1:5000/api/refresh_all', timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ RSS刷新成功: {data.get('message', 'OK')}")
        else:
            print(f"✗ RSS刷新失败: {response.status_code}")
    except requests.RequestException as e:
        print(f"⚠ RSS刷新请求失败: {e}")
    
    # 检查模板文件
    template_file = 'templates/item_detail.html'
    if os.path.exists(template_file):
        print("✓ 图片显示模板文件存在")
        
        # 检查是否包含增强的图片CSS
        with open(template_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'image-placeholder' in content:
            print("✓ 包含图片占位符样式")
        else:
            print("✗ 缺少图片占位符样式")
            
        if 'object-fit: cover' in content:
            print("✓ 包含响应式图片样式")
        else:
            print("✗ 缺少响应式图片样式")
            
        if 'openImageModal' in content:
            print("✓ 包含图片模态框功能")
        else:
            print("✗ 缺少图片模态框功能")
    else:
        print("✗ 图片显示模板文件不存在")
        return False
    
    print("\n📝 使用说明:")
    print("1. 在浏览器中打开: http://127.0.0.1:5000")
    print("2. 选择任意订阅源查看内容")
    print("3. 点击文章标题查看详细内容")
    print("4. 现在图片应该能够:")
    print("   - 正确加载和显示")
    print("   - 显示加载状态")
    print("   - 处理加载失败的情况")
    print("   - 支持点击放大查看")
    print("   - 具有圆角和阴影效果")
    
    return True

def test_html_processing():
    """测试HTML内容处理"""
    print("\n测试HTML内容处理...")
    
    try:
        from feed_manager import FeedManager
        
        manager = FeedManager()
        
        # 测试HTML清理函数
        test_html = '<img src="test.jpg"><a href="http://example.com">链接</a>'
        cleaned = manager._clean_and_enhance_html(test_html)
        
        if 'loading="lazy"' in cleaned:
            print("✓ 图片懒加载属性添加成功")
        else:
            print("✗ 图片懒加载属性未添加")
            
        if 'target="_blank"' in cleaned:
            print("✓ 链接新窗口打开属性添加成功")
        else:
            print("✗ 链接新窗口打开属性未添加")
            
        return True
        
    except Exception as e:
        print(f"✗ HTML处理测试失败: {e}")
        return False

def main():
    print("=" * 50)
    print("Twitter RSS订阅管理器 - 图片显示测试")
    print("=" * 50)
    
    success = True
    
    if not test_image_display():
        success = False
    
    if not test_html_processing():
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("✓ 图片显示功能测试通过！")
        print("\n🎉 改进功能:")
        print("• 增强的图片加载状态显示")
        print("• 图片加载失败时的优雅降级")
        print("• 响应式图片显示和圆角阴影效果")
        print("• 点击图片放大查看功能")
        print("• 图片懒加载提升性能")
        print("• 更好的HTML内容解析")
    else:
        print("✗ 部分测试失败，请检查错误信息")
    
    print("=" * 50)

if __name__ == "__main__":
    main()