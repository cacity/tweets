"""
订阅源对话框
用于添加和编辑RSS订阅源
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QTextEdit, QMessageBox,
                             QProgressBar, QFileDialog)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import requests


class FeedTestThread(QThread):
    """测试RSS订阅源的线程"""
    
    result_ready = pyqtSignal(bool, str, str)  # success, title, message
    
    def __init__(self, url):
        super().__init__()
        self.url = url
    
    def run(self):
        try:
            import feedparser
            
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
            
            parsed_feed = feedparser.parse(response.content)
            
            if parsed_feed.bozo:
                self.result_ready.emit(False, "", "无效的RSS格式")
                return
            
            title = parsed_feed.feed.get('title', 'Unknown Feed')
            self.result_ready.emit(True, title, "RSS订阅源有效")
            
        except requests.RequestException as e:
            self.result_ready.emit(False, "", f"网络错误: {str(e)}")
        except Exception as e:
            self.result_ready.emit(False, "", f"测试失败: {str(e)}")


class AddFeedDialog(QDialog):
    """添加订阅源对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("添加RSS订阅源")
        self.setModal(True)
        self.resize(500, 300)
        
        self.feed_data = None
        self.test_thread = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """设置界面"""
        layout = QVBoxLayout(self)
        
        # URL输入
        url_layout = QHBoxLayout()
        url_layout.addWidget(QLabel("RSS URL:"))
        self.url_edit = QLineEdit()
        self.url_edit.setPlaceholderText("请输入RSS订阅源的URL")
        url_layout.addWidget(self.url_edit)
        
        # 测试按钮
        self.test_btn = QPushButton("测试")
        self.test_btn.clicked.connect(self.test_feed)
        url_layout.addWidget(self.test_btn)
        
        layout.addLayout(url_layout)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # 标题输入
        title_layout = QHBoxLayout()
        title_layout.addWidget(QLabel("标题:"))
        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("RSS订阅源标题（可选，留空自动获取）")
        title_layout.addWidget(self.title_edit)
        layout.addLayout(title_layout)
        
        # 描述输入
        layout.addWidget(QLabel("描述:"))
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(100)
        self.description_edit.setPlaceholderText("RSS订阅源描述（可选）")
        layout.addWidget(self.description_edit)
        
        # 按钮
        button_layout = QHBoxLayout()
        
        # 导入OPML按钮
        self.import_btn = QPushButton("导入OPML")
        self.import_btn.clicked.connect(self.import_opml)
        button_layout.addWidget(self.import_btn)
        
        button_layout.addStretch()
        
        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)
        
        self.ok_btn = QPushButton("确定")
        self.ok_btn.clicked.connect(self.accept_feed)
        self.ok_btn.setEnabled(False)
        button_layout.addWidget(self.ok_btn)
        
        layout.addLayout(button_layout)
        
        # 连接信号
        self.url_edit.textChanged.connect(self.validate_input)
    
    def test_feed(self):
        """测试RSS订阅源"""
        url = self.url_edit.text().strip()
        if not url:
            QMessageBox.warning(self, "错误", "请先输入RSS URL")
            return
        
        self.test_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # 不确定进度
        
        self.test_thread = FeedTestThread(url)
        self.test_thread.result_ready.connect(self.on_test_result)
        self.test_thread.start()
    
    def on_test_result(self, success, title, message):
        """处理测试结果"""
        self.test_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        if success:
            if title and not self.title_edit.text():
                self.title_edit.setText(title)
            QMessageBox.information(self, "成功", message)
            self.ok_btn.setEnabled(True)
        else:
            QMessageBox.warning(self, "错误", message)
            self.ok_btn.setEnabled(False)
    
    def validate_input(self):
        """验证输入"""
        url = self.url_edit.text().strip()
        if url and (url.startswith('http://') or url.startswith('https://')):
            self.ok_btn.setEnabled(True)
        else:
            self.ok_btn.setEnabled(False)
    
    def accept_feed(self):
        """确认添加订阅源"""
        url = self.url_edit.text().strip()
        title = self.title_edit.text().strip()
        description = self.description_edit.toPlainText().strip()
        
        if not url:
            QMessageBox.warning(self, "错误", "请输入RSS URL")
            return
        
        self.feed_data = {
            'url': url,
            'title': title,
            'description': description
        }
        
        self.accept()
    
    def import_opml(self):
        """导入OPML文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择OPML文件", "", "OPML Files (*.opml *.xml);;All Files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    opml_content = f.read()
                
                # 发送导入信号给父窗口
                if hasattr(self.parent(), 'import_opml_content'):
                    self.parent().import_opml_content(opml_content)
                    self.reject()  # 关闭对话框
                
            except Exception as e:
                QMessageBox.critical(self, "错误", f"导入OPML文件失败: {str(e)}")
    
    def get_feed_data(self):
        """获取订阅源数据"""
        return self.feed_data


class EditFeedDialog(AddFeedDialog):
    """编辑订阅源对话框"""
    
    def __init__(self, feed, parent=None):
        super().__init__(parent)
        self.setWindowTitle("编辑RSS订阅源")
        
        # 填充现有数据
        self.url_edit.setText(feed.url)
        self.title_edit.setText(feed.title)
        self.description_edit.setPlainText(feed.description)
        
        # 禁用URL编辑
        self.url_edit.setEnabled(False)
        self.test_btn.setEnabled(False)
        
        # 启用确定按钮
        self.ok_btn.setEnabled(True)