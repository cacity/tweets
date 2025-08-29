"""
订阅内容显示组件
用于渲染和显示RSS订阅内容
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTextBrowser, QSplitter, QListWidget,
                             QListWidgetItem, QFrame, QScrollArea, QTextEdit,
                             QDialog, QDialogButtonBox)
from PyQt5.QtCore import Qt, pyqtSignal, QUrl
from PyQt5.QtGui import QFont, QDesktopServices, QPixmap
from datetime import datetime
import webbrowser
import re
import html
import requests
from io import BytesIO

from models import Feed, FeedItem


class DetailedContentDialog(QDialog):
    """详细内容查看对话框"""
    
    def __init__(self, item: FeedItem, parent=None):
        super().__init__(parent)
        self.item = item
        self.setWindowTitle(f"详细内容 - {item.title[:50]}...")
        self.setModal(True)
        self.resize(800, 600)
        self.setup_ui()
    
    def setup_ui(self):
        """设置界面"""
        layout = QVBoxLayout(self)
        
        # 标题区域
        title_label = QLabel(self.item.title)
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(14)
        title_label.setFont(title_font)
        title_label.setWordWrap(True)
        title_label.setStyleSheet("""
            QLabel {
                color: #1a1a1a;
                padding: 10px;
                background-color: #f8f9fa;
                border-radius: 6px;
                margin-bottom: 10px;
            }
        """)
        layout.addWidget(title_label)
        
        # 信息区域
        info_layout = QHBoxLayout()
        if self.item.author:
            author_label = QLabel(f"📝 作者: {self.item.author}")
            author_label.setStyleSheet("color: #6c757d; font-size: 10pt; padding: 5px;")
            info_layout.addWidget(author_label)
        
        if self.item.published:
            time_str = self.item.published.strftime("%Y年%m月%d日 %H:%M")
            time_label = QLabel(f"🕒 发布时间: {time_str}")
            time_label.setStyleSheet("color: #6c757d; font-size: 10pt; padding: 5px;")
            info_layout.addStretch()
            info_layout.addWidget(time_label)
        
        if info_layout.count() > 0:
            layout.addLayout(info_layout)
        
        # 内容区域
        self.content_browser = QTextBrowser()
        self.content_browser.setStyleSheet("""
            QTextBrowser {
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                padding: 15px;
                background-color: white;
                font-size: 11pt;
                line-height: 1.6;
            }
        """)
        
        if self.item.description:
            processed_content = self._process_detailed_content(self.item.description)
            self.content_browser.setHtml(processed_content)
        
        layout.addWidget(self.content_browser)
        
        # 按钮区域
        button_box = QDialogButtonBox()
        
        if self.item.link:
            open_link_btn = QPushButton("🔗 打开原文链接")
            open_link_btn.clicked.connect(self.open_original_link)
            button_box.addButton(open_link_btn, QDialogButtonBox.ActionRole)
        
        close_btn = button_box.addButton("关闭", QDialogButtonBox.RejectRole)
        close_btn.clicked.connect(self.reject)
        
        layout.addWidget(button_box)
    
    def _process_detailed_content(self, html_content):
        """处理详细内容的HTML"""
        processed = html.unescape(html_content)
        
        css_style = """
        <style>
        body {
            font-family: 'Segoe UI', 'Microsoft YaHei', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.8;
            color: #333;
            margin: 0;
            padding: 0;
        }
        p {
            margin: 12px 0;
            text-align: justify;
            text-indent: 2em;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #2c3e50;
            margin: 20px 0 10px 0;
        }
        img {
            max-width: 100%;
            height: auto;
            border-radius: 6px;
            margin: 15px auto;
            display: block;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        a {
            color: #007bff;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        blockquote {
            border-left: 4px solid #007bff;
            margin: 20px 0;
            padding: 15px 20px;
            background-color: #f8f9fa;
            border-radius: 6px;
            font-style: italic;
        }
        code {
            background-color: #f1f3f4;
            padding: 3px 6px;
            border-radius: 4px;
            font-family: 'Consolas', 'Monaco', monospace;
        }
        pre {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 6px;
            overflow-x: auto;
            border: 1px solid #e9ecef;
        }
        ul, ol {
            padding-left: 30px;
        }
        li {
            margin: 5px 0;
        }
        </style>
        """
        
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            {css_style}
        </head>
        <body>
            {processed}
        </body>
        </html>
        """
        
        return full_html
    
    def open_original_link(self):
        """打开原文链接"""
        if self.item.link:
            webbrowser.open(self.item.link)


class EnhancedFeedItemWidget(QFrame):
    """增强版RSS条目显示组件 - 支持HTML内容和图片"""
    
    item_clicked = pyqtSignal(FeedItem)
    
    def __init__(self, item: FeedItem, parent=None):
        super().__init__(parent)
        self.item = item
        self.setup_ui()
        self.setFrameStyle(QFrame.Box)
        self.setLineWidth(1)
        self.setStyleSheet("""
            EnhancedFeedItemWidget {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                margin: 5px;
            }
            EnhancedFeedItemWidget:hover {
                background-color: #e9ecef;
                border-color: #007bff;
            }
        """)
    
    def setup_ui(self):
        """设置界面"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 12, 15, 12)
        layout.setSpacing(8)
        
        # 标题
        title_label = QLabel(self.item.title)
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(11)
        title_label.setFont(title_font)
        title_label.setWordWrap(True)
        title_label.setStyleSheet("""
            QLabel {
                color: #1a1a1a;
                margin-bottom: 5px;
            }
        """)
        layout.addWidget(title_label)
        
        # 作者和时间信息
        info_layout = QHBoxLayout()
        if self.item.author:
            author_label = QLabel(f"📝 {self.item.author}")
            author_label.setStyleSheet("color: #6c757d; font-size: 9pt;")
            info_layout.addWidget(author_label)
        
        if self.item.published:
            time_str = self.item.published.strftime("%Y-%m-%d %H:%M")
            time_label = QLabel(f"🕒 {time_str}")
            time_label.setStyleSheet("color: #6c757d; font-size: 9pt;")
            info_layout.addStretch()
            info_layout.addWidget(time_label)
        
        if info_layout.count() > 0:
            layout.addLayout(info_layout)
        
        # 使用QTextBrowser来显示富文本内容
        if self.item.description:
            self.content_browser = QTextBrowser()
            self.content_browser.setMaximumHeight(300)
            self.content_browser.setStyleSheet("""
                QTextBrowser {
                    border: 1px solid #e0e0e0;
                    border-radius: 4px;
                    padding: 8px;
                    background-color: white;
                    font-size: 9pt;
                    line-height: 1.4;
                }
            """)
            
            # 处理HTML内容
            processed_content = self._process_html_content(self.item.description)
            self.content_browser.setHtml(processed_content)
            
            # 禁用链接点击（避免在组件内部导航）
            self.content_browser.setOpenLinks(False)
            
            layout.addWidget(self.content_browser)
        
        # 操作按钮区域
        button_layout = QHBoxLayout()
        
        if self.item.link:
            link_btn = QPushButton("🔗 查看原文")
            link_btn.setStyleSheet("""
                QPushButton {
                    background-color: #007bff;
                    color: white;
                    border: none;
                    padding: 6px 12px;
                    border-radius: 4px;
                    font-size: 9pt;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #0056b3;
                }
                QPushButton:pressed {
                    background-color: #004085;
                }
            """)
            link_btn.clicked.connect(self.open_link)
            button_layout.addWidget(link_btn)
        
        # 展开/收缩按钮
        self.toggle_btn = QPushButton("📖 展开内容")
        self.toggle_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                font-size: 9pt;
            }
            QPushButton:hover {
                background-color: #545b62;
            }
        """)
        self.toggle_btn.clicked.connect(self.toggle_content)
        button_layout.addWidget(self.toggle_btn)
        
        # 详细内容按钮
        detail_btn = QPushButton("🔍 详细内容")
        detail_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                font-size: 9pt;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        detail_btn.clicked.connect(self.show_detailed_content)
        button_layout.addWidget(detail_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # 初始状态：收缩内容
        if hasattr(self, 'content_browser'):
            self.content_browser.setMaximumHeight(80)
            self.content_expanded = False
    
    def _process_html_content(self, html_content):
        """处理HTML内容，提取图片、段落等"""
        # 清理和处理HTML
        processed = html.unescape(html_content)
        
        # 添加基本样式
        css_style = """
        <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            margin: 0;
            padding: 0;
        }
        p {
            margin: 8px 0;
            text-align: justify;
        }
        img {
            max-width: 100%;
            height: auto;
            border-radius: 4px;
            margin: 8px 0;
            display: block;
        }
        a {
            color: #007bff;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        blockquote {
            border-left: 4px solid #007bff;
            margin: 16px 0;
            padding-left: 16px;
            background-color: #f8f9fa;
            border-radius: 4px;
        }
        code {
            background-color: #f1f3f4;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: monospace;
        }
        </style>
        """
        
        # 处理图片链接，确保可以显示
        img_pattern = r'<img[^>]*src=["\']([^"\'>]+)["\'][^>]*>'
        
        def replace_img(match):
            img_url = match.group(1)
            # 如果是相对路径，尝试转换为绝对路径
            if not img_url.startswith(('http://', 'https://')):
                return f'<p>[图片: {img_url}]</p>'
            return match.group(0)
        
        processed = re.sub(img_pattern, replace_img, processed)
        
        # 包装完整的HTML
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            {css_style}
        </head>
        <body>
            {processed}
        </body>
        </html>
        """
        
        return full_html
    
    def toggle_content(self):
        """切换内容展开/收缩状态"""
        if hasattr(self, 'content_browser'):
            if self.content_expanded:
                self.content_browser.setMaximumHeight(80)
                self.toggle_btn.setText("📖 展开内容")
                self.content_expanded = False
            else:
                self.content_browser.setMaximumHeight(400)
                self.toggle_btn.setText("📚 收起内容")
                self.content_expanded = True
    
    def show_detailed_content(self):
        """显示详细内容对话框"""
        dialog = DetailedContentDialog(self.item, self)
        dialog.exec_()
    
    def open_link(self):
        """打开链接"""
        if self.item.link:
            webbrowser.open(self.item.link)
    
    def mousePressEvent(self, event):
        """鼠标点击事件"""
        if event.button() == Qt.LeftButton:
            self.item_clicked.emit(self.item)
        super().mousePressEvent(event)


class FeedViewer(QWidget):
    """订阅源内容查看器"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_feed = None
        self.setup_ui()
    
    def setup_ui(self):
        """设置界面"""
        layout = QVBoxLayout(self)
        
        # 订阅源信息区域
        self.feed_info_label = QLabel("选择一个订阅源查看内容")
        self.feed_info_label.setStyleSheet("""
            QLabel {
                background-color: #e9ecef;
                padding: 10px;
                border-radius: 4px;
                font-weight: bold;
            }
        """)
        layout.addWidget(self.feed_info_label)
        
        # 内容显示区域
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(5)
        
        self.scroll_area.setWidget(self.content_widget)
        layout.addWidget(self.scroll_area)
        
        # 初始状态
        self.show_empty_state()
    
    def show_empty_state(self):
        """显示空状态"""
        self.clear_content()
        
        empty_label = QLabel("暂无内容\n\n请添加RSS订阅源或选择现有订阅源")
        empty_label.setAlignment(Qt.AlignCenter)
        empty_label.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-size: 12pt;
                padding: 50px;
            }
        """)
        self.content_layout.addWidget(empty_label)
        self.content_layout.addStretch()
    
    def clear_content(self):
        """清空内容"""
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
    
    def show_feed(self, feed: Feed):
        """显示订阅源内容"""
        self.current_feed = feed
        
        # 更新订阅源信息
        info_text = f"{feed.title} ({len(feed.items)} 条)"
        if feed.last_updated:
            info_text += f" - 最后更新: {feed.last_updated.strftime('%Y-%m-%d %H:%M')}"
        self.feed_info_label.setText(info_text)
        
        # 清空现有内容
        self.clear_content()
        
        if not feed.items:
            no_items_label = QLabel("此订阅源暂无内容")
            no_items_label.setAlignment(Qt.AlignCenter)
            no_items_label.setStyleSheet("color: #6c757d; padding: 20px;")
            self.content_layout.addWidget(no_items_label)
        else:
            # 按时间排序（最新的在前）
            sorted_items = sorted(feed.items, 
                                key=lambda x: x.published or datetime.min, 
                                reverse=True)
            
            # 添加条目（使用增强版组件）
            for item in sorted_items:
                item_widget = EnhancedFeedItemWidget(item)
                item_widget.item_clicked.connect(self.on_item_clicked)
                self.content_layout.addWidget(item_widget)
        
        self.content_layout.addStretch()
    
    def on_item_clicked(self, item: FeedItem):
        """条目点击处理 - 显示详细内容"""
        dialog = DetailedContentDialog(item, self)
        dialog.exec_()
    
    def refresh_current_feed(self, updated_feed: Feed):
        """刷新当前显示的订阅源"""
        if self.current_feed and self.current_feed.url == updated_feed.url:
            self.show_feed(updated_feed)