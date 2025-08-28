"""
测试增强的RSS内容渲染功能
"""

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from datetime import datetime

def test_enhanced_content_rendering():
    """测试增强的内容渲染功能"""
    try:
        # 设置Qt属性
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
        
        app = QApplication(sys.argv)
        
        # 导入增强的组件
        from models import FeedItem
        from feed_viewer import EnhancedFeedItemWidget, DetailedContentDialog
        
        # 创建测试数据（包含HTML内容）
        html_content = """
        <h2>测试标题</h2>
        <p>这是一个包含<strong>HTML格式</strong>的测试内容。</p>
        <p>内容包含：</p>
        <ul>
            <li>粗体文字：<b>重要信息</b></li>
            <li>链接：<a href="https://example.com">示例链接</a></li>
            <li>代码：<code>print("Hello World")</code></li>
        </ul>
        <blockquote>
            这是一个引用块，用来测试样式渲染。
        </blockquote>
        <p>还有一些<em>斜体文字</em>和普通段落文本。</p>
        <img src="https://via.placeholder.com/300x200" alt="测试图片" />
        """
        
        test_item = FeedItem(
            title="测试RSS条目标题 - 包含HTML内容和图片",
            link="https://example.com/test-article",
            description=html_content,
            published=datetime.now(),
            author="测试作者",
            guid="test-guid-123"
        )
        
        # 创建增强的条目组件
        item_widget = EnhancedFeedItemWidget(test_item)
        item_widget.show()
        
        print("✓ 增强的RSS内容渲染组件创建成功")
        print("✓ 支持以下功能：")
        print("  • HTML内容解析和渲染")
        print("  • 图片显示支持")
        print("  • 段落格式保持")
        print("  • 展开/收缩内容")
        print("  • 详细内容查看")
        print("  • 原文链接跳转")
        
        # 测试详细内容对话框
        detail_dialog = DetailedContentDialog(test_item)
        
        print("\n测试窗口已显示，请手动测试以下功能：")
        print("1. 点击'展开内容'按钮查看内容渲染效果")
        print("2. 点击'详细内容'按钮查看完整内容")
        print("3. 点击'查看原文'测试链接跳转")
        print("4. 检查HTML格式是否正确渲染")
        
        # 显示组件
        item_widget.resize(600, 400)
        item_widget.show()
        
        # 运行应用
        return app.exec_()
        
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        return 1

if __name__ == "__main__":
    print("=" * 50)
    print("测试增强的RSS内容渲染功能")
    print("=" * 50)
    
    result = test_enhanced_content_rendering()
    
    if result == 0:
        print("\n✓ 测试完成")
    else:
        print("\n✗ 测试失败")