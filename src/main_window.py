"""
主窗口界面
整合所有组件，提供完整的RSS订阅管理功能
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QSplitter, QListWidget, QListWidgetItem, QPushButton,
                             QMenuBar, QStatusBar, QMessageBox, QProgressBar,
                             QToolBar, QAction, QFileDialog, QInputDialog,
                             QLabel, QFrame)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QIcon, QFont
import sys
import os

from feed_manager import FeedManager
from feed_dialog import AddFeedDialog, EditFeedDialog
from feed_viewer import FeedViewer
from models import Feed


class RefreshThread(QThread):
    """刷新RSS订阅源的线程"""
    
    progress_updated = pyqtSignal(str)  # 进度消息
    feed_refreshed = pyqtSignal(str, bool, str)  # url, success, message
    all_finished = pyqtSignal(dict)  # 所有刷新结果
    
    def __init__(self, feed_manager, feed_urls=None):
        super().__init__()
        self.feed_manager = feed_manager
        self.feed_urls = feed_urls  # 如果为None则刷新所有
    
    def run(self):
        if self.feed_urls is None:
            # 刷新所有订阅源
            self.progress_updated.emit("开始刷新所有订阅源...")
            results = self.feed_manager.refresh_all_feeds()
            self.all_finished.emit(results)
        else:
            # 刷新指定订阅源
            results = {}
            for url in self.feed_urls:
                feed = self.feed_manager.get_feed_by_url(url)
                if feed:
                    self.progress_updated.emit(f"正在刷新: {feed.title}")
                    success, message = self.feed_manager.refresh_feed(url)
                    results[url] = {'success': success, 'message': message}
                    self.feed_refreshed.emit(url, success, message)
            
            self.all_finished.emit(results)


class FeedListWidget(QListWidget):
    """订阅源列表组件"""
    
    feed_selected = pyqtSignal(Feed)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlternatingRowColors(True)
        self.itemClicked.connect(self.on_item_clicked)
    
    def add_feed(self, feed: Feed):
        """添加订阅源到列表"""
        item = QListWidgetItem()
        item.setText(f"{feed.title} ({len(feed.items)})")
        item.setData(Qt.UserRole, feed)
        
        # 设置工具提示
        tooltip = f"标题: {feed.title}\nURL: {feed.url}"
        if feed.description:
            tooltip += f"\n描述: {feed.description}"
        if feed.last_updated:
            tooltip += f"\n最后更新: {feed.last_updated.strftime('%Y-%m-%d %H:%M')}"
        item.setToolTip(tooltip)
        
        self.addItem(item)
    
    def update_feed(self, feed: Feed):
        """更新订阅源显示"""
        for i in range(self.count()):
            item = self.item(i)
            item_feed = item.data(Qt.UserRole)
            if item_feed.url == feed.url:
                item.setText(f"{feed.title} ({len(feed.items)})")
                item.setData(Qt.UserRole, feed)
                
                # 更新工具提示
                tooltip = f"标题: {feed.title}\nURL: {feed.url}"
                if feed.description:
                    tooltip += f"\n描述: {feed.description}"
                if feed.last_updated:
                    tooltip += f"\n最后更新: {feed.last_updated.strftime('%Y-%m-%d %H:%M')}"
                item.setToolTip(tooltip)
                break
    
    def remove_feed(self, url: str):
        """从列表中移除订阅源"""
        for i in range(self.count()):
            item = self.item(i)
            feed = item.data(Qt.UserRole)
            if feed.url == url:
                self.takeItem(i)
                break
    
    def clear_feeds(self):
        """清空列表"""
        self.clear()
    
    def on_item_clicked(self, item):
        """列表项点击事件"""
        feed = item.data(Qt.UserRole)
        if feed:
            self.feed_selected.emit(feed)
    
    def get_selected_feed(self):
        """获取当前选中的订阅源"""
        current_item = self.currentItem()
        if current_item:
            return current_item.data(Qt.UserRole)
        return None


class MainWindow(QMainWindow):
    """主窗口"""
    
    def __init__(self):
        super().__init__()
        self.feed_manager = FeedManager()
        self.refresh_thread = None
        
        self.setWindowTitle("Twitter RSS订阅管理器")
        self.setGeometry(100, 100, 1200, 800)
        
        self.setup_ui()
        self.load_feeds()
        
        # 设置自动刷新定时器（可选）
        self.auto_refresh_timer = QTimer()
        self.auto_refresh_timer.timeout.connect(self.refresh_all_feeds)
        # self.auto_refresh_timer.start(30 * 60 * 1000)  # 30分钟自动刷新
    
    def setup_ui(self):
        """设置界面"""
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QHBoxLayout(central_widget)
        
        # 创建分割器
        splitter = QSplitter(Qt.Horizontal)
        
        # 左侧面板 - 订阅源列表
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)
        
        # 右侧面板 - 内容显示
        self.feed_viewer = FeedViewer()
        splitter.addWidget(self.feed_viewer)
        
        # 设置分割器比例
        splitter.setSizes([300, 900])
        
        main_layout.addWidget(splitter)
        
        # 创建菜单栏
        self.create_menu_bar()
        
        # 创建工具栏
        self.create_toolbar()
        
        # 创建状态栏
        self.create_status_bar()
    
    def create_left_panel(self):
        """创建左侧面板"""
        panel = QFrame()
        panel.setFrameStyle(QFrame.StyledPanel)
        layout = QVBoxLayout(panel)
        
        # 标题
        title_label = QLabel("RSS订阅源")
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(12)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("padding: 10px; background-color: #007bff; color: white;")
        layout.addWidget(title_label)
        
        # 订阅源列表
        self.feed_list = FeedListWidget()
        self.feed_list.feed_selected.connect(self.on_feed_selected)
        layout.addWidget(self.feed_list)
        
        # 按钮区域
        button_layout = QVBoxLayout()
        
        self.add_btn = QPushButton("添加订阅源")
        self.add_btn.clicked.connect(self.add_feed)
        button_layout.addWidget(self.add_btn)
        
        self.edit_btn = QPushButton("编辑订阅源")
        self.edit_btn.clicked.connect(self.edit_feed)
        self.edit_btn.setEnabled(False)
        button_layout.addWidget(self.edit_btn)
        
        self.refresh_btn = QPushButton("刷新选中")
        self.refresh_btn.clicked.connect(self.refresh_selected_feed)
        self.refresh_btn.setEnabled(False)
        button_layout.addWidget(self.refresh_btn)
        
        self.refresh_all_btn = QPushButton("刷新全部")
        self.refresh_all_btn.clicked.connect(self.refresh_all_feeds)
        button_layout.addWidget(self.refresh_all_btn)
        
        self.remove_btn = QPushButton("删除订阅源")
        self.remove_btn.clicked.connect(self.remove_feed)
        self.remove_btn.setEnabled(False)
        self.remove_btn.setStyleSheet("QPushButton { background-color: #dc3545; color: white; }")
        button_layout.addWidget(self.remove_btn)
        
        layout.addLayout(button_layout)
        
        return panel
    
    def create_menu_bar(self):
        """创建菜单栏"""
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu("文件")
        
        import_action = QAction("导入OPML", self)
        import_action.triggered.connect(self.import_opml)
        file_menu.addAction(import_action)
        
        export_action = QAction("导出OPML", self)
        export_action.triggered.connect(self.export_opml)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("退出", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 订阅源菜单
        feed_menu = menubar.addMenu("订阅源")
        
        add_action = QAction("添加订阅源", self)
        add_action.triggered.connect(self.add_feed)
        feed_menu.addAction(add_action)
        
        refresh_action = QAction("刷新所有", self)
        refresh_action.triggered.connect(self.refresh_all_feeds)
        feed_menu.addAction(refresh_action)
        
        # 帮助菜单
        help_menu = menubar.addMenu("帮助")
        
        about_action = QAction("关于", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def create_toolbar(self):
        """创建工具栏"""
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        # 添加按钮
        add_action = QAction("添加", self)
        add_action.triggered.connect(self.add_feed)
        toolbar.addAction(add_action)
        
        # 刷新按钮
        refresh_action = QAction("刷新", self)
        refresh_action.triggered.connect(self.refresh_all_feeds)
        toolbar.addAction(refresh_action)
        
        toolbar.addSeparator()
        
        # 导入按钮
        import_action = QAction("导入", self)
        import_action.triggered.connect(self.import_opml)
        toolbar.addAction(import_action)
        
        # 导出按钮
        export_action = QAction("导出", self)
        export_action.triggered.connect(self.export_opml)
        toolbar.addAction(export_action)
    
    def create_status_bar(self):
        """创建状态栏"""
        self.status_bar = self.statusBar()
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.status_bar.addPermanentWidget(self.progress_bar)
        
        # 状态标签
        self.status_label = QLabel("就绪")
        self.status_bar.addWidget(self.status_label)
    
    def load_feeds(self):
        """加载订阅源"""
        feeds = self.feed_manager.get_all_feeds()
        self.feed_list.clear_feeds()
        
        for feed in feeds:
            self.feed_list.add_feed(feed)
        
        self.status_label.setText(f"已加载 {len(feeds)} 个订阅源")
        
        if not feeds:
            self.feed_viewer.show_empty_state()
    
    def on_feed_selected(self, feed: Feed):
        """订阅源选中事件"""
        self.feed_viewer.show_feed(feed)
        
        # 启用相关按钮
        self.edit_btn.setEnabled(True)
        self.refresh_btn.setEnabled(True)
        self.remove_btn.setEnabled(True)
    
    def add_feed(self):
        """添加订阅源"""
        dialog = AddFeedDialog(self)
        if dialog.exec_() == dialog.Accepted:
            data = dialog.get_feed_data()
            if data:
                self.status_label.setText("正在添加订阅源...")
                
                success, message = self.feed_manager.add_feed_from_url(
                    data['url'], data['title']
                )
                
                if success:
                    # 重新加载列表
                    self.load_feeds()
                    QMessageBox.information(self, "成功", message)
                else:
                    QMessageBox.warning(self, "错误", message)
                
                self.status_label.setText("就绪")
    
    def edit_feed(self):
        """编辑订阅源"""
        selected_feed = self.feed_list.get_selected_feed()
        if not selected_feed:
            return
        
        dialog = EditFeedDialog(selected_feed, self)
        if dialog.exec_() == dialog.Accepted:
            data = dialog.get_feed_data()
            if data:
                # 更新订阅源信息
                selected_feed.title = data['title']
                selected_feed.description = data['description']
                
                # 更新显示
                self.feed_list.update_feed(selected_feed)
                self.feed_viewer.refresh_current_feed(selected_feed)
                
                # 保存数据
                self.feed_manager.save_feeds()
                
                QMessageBox.information(self, "成功", "订阅源信息已更新")
    
    def remove_feed(self):
        """删除订阅源"""
        selected_feed = self.feed_list.get_selected_feed()
        if not selected_feed:
            return
        
        reply = QMessageBox.question(
            self, "确认删除",
            f"确定要删除订阅源 '{selected_feed.title}' 吗？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.feed_manager.remove_feed(selected_feed.url):
                self.feed_list.remove_feed(selected_feed.url)
                self.feed_viewer.show_empty_state()
                
                # 禁用相关按钮
                self.edit_btn.setEnabled(False)
                self.refresh_btn.setEnabled(False)
                self.remove_btn.setEnabled(False)
                
                QMessageBox.information(self, "成功", "订阅源已删除")
    
    def refresh_selected_feed(self):
        """刷新选中的订阅源"""
        selected_feed = self.feed_list.get_selected_feed()
        if not selected_feed:
            return
        
        self.start_refresh([selected_feed.url])
    
    def refresh_all_feeds(self):
        """刷新所有订阅源"""
        feeds = self.feed_manager.get_all_feeds()
        if not feeds:
            QMessageBox.information(self, "提示", "暂无订阅源需要刷新")
            return
        
        self.start_refresh()
    
    def start_refresh(self, feed_urls=None):
        """开始刷新操作"""
        if self.refresh_thread and self.refresh_thread.isRunning():
            QMessageBox.warning(self, "提示", "正在刷新中，请稍候...")
            return
        
        # 禁用刷新按钮
        self.refresh_btn.setEnabled(False)
        self.refresh_all_btn.setEnabled(False)
        
        # 显示进度条
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        
        # 创建并启动刷新线程
        self.refresh_thread = RefreshThread(self.feed_manager, feed_urls)
        self.refresh_thread.progress_updated.connect(self.on_refresh_progress)
        self.refresh_thread.feed_refreshed.connect(self.on_feed_refreshed)
        self.refresh_thread.all_finished.connect(self.on_refresh_finished)
        self.refresh_thread.start()
    
    def on_refresh_progress(self, message):
        """刷新进度更新"""
        self.status_label.setText(message)
    
    def on_feed_refreshed(self, url, success, message):
        """单个订阅源刷新完成"""
        if success:
            feed = self.feed_manager.get_feed_by_url(url)
            if feed:
                self.feed_list.update_feed(feed)
                self.feed_viewer.refresh_current_feed(feed)
    
    def on_refresh_finished(self, results):
        """所有刷新操作完成"""
        # 隐藏进度条
        self.progress_bar.setVisible(False)
        
        # 重新启用按钮
        self.refresh_btn.setEnabled(True)
        self.refresh_all_btn.setEnabled(True)
        
        # 统计结果
        success_count = sum(1 for r in results.values() if r['success'])
        total_count = len(results)
        
        self.status_label.setText(f"刷新完成: {success_count}/{total_count} 成功")
        
        # 如果有失败的，显示详细信息
        if success_count < total_count:
            failed_feeds = [url for url, r in results.items() if not r['success']]
            QMessageBox.warning(
                self, "刷新完成",
                f"刷新完成，{success_count}/{total_count} 成功\n\n"
                f"失败的订阅源：\n" + "\n".join(failed_feeds[:5])
            )
    
    def import_opml(self):
        """导入OPML文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择OPML文件", "", "OPML Files (*.opml *.xml);;All Files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    opml_content = f.read()
                
                self.import_opml_content(opml_content)
                
            except Exception as e:
                QMessageBox.critical(self, "错误", f"导入OPML文件失败: {str(e)}")
    
    def import_opml_content(self, opml_content):
        """导入OPML内容"""
        self.status_label.setText("正在导入OPML...")
        
        # 显示进度条
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        
        success_count, total_count, error_messages = self.feed_manager.import_opml(opml_content)
        
        # 隐藏进度条
        self.progress_bar.setVisible(False)
        
        self.load_feeds()  # 重新加载列表
        
        self.status_label.setText("就绪")
        
        if total_count > 0:
            message = f"导入完成：{success_count}/{total_count} 个订阅源添加成功"
            
            # 如果有错误，显示详细信息
            if error_messages:
                detailed_errors = "\n".join(error_messages[:10])  # 最多显示10个错误
                if len(error_messages) > 10:
                    detailed_errors += f"\n\n... 还有 {len(error_messages) - 10} 个错误"
                
                msg_box = QMessageBox(self)
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setWindowTitle("导入完成")
                msg_box.setText(message)
                msg_box.setDetailedText(detailed_errors)
                msg_box.exec_()
            else:
                QMessageBox.information(self, "导入成功", message)
        else:
            QMessageBox.warning(self, "导入失败", "未找到有效的RSS订阅源")
    
    def export_opml(self):
        """导出OPML文件"""
        feeds = self.feed_manager.get_all_feeds()
        if not feeds:
            QMessageBox.information(self, "提示", "暂无订阅源可导出")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存OPML文件", "feeds.opml", "OPML Files (*.opml);;All Files (*)"
        )
        
        if file_path:
            try:
                opml_content = self.feed_manager.export_opml()
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(opml_content)
                
                QMessageBox.information(self, "成功", f"OPML文件已保存到: {file_path}")
                
            except Exception as e:
                QMessageBox.critical(self, "错误", f"导出OPML文件失败: {str(e)}")
    
    def show_about(self):
        """显示关于信息"""
        QMessageBox.about(
            self, "关于",
            "Twitter RSS订阅管理器\n\n"
            "一个用于管理和查看Twitter RSS订阅源的PyQt应用程序\n\n"
            "功能特性：\n"
            "• 添加和管理RSS订阅源\n"
            "• 自动获取和解析RSS内容\n"
            "• 支持OPML格式导入导出\n"
            "• 实时刷新订阅内容\n"
            "• 友好的用户界面"
        )
    
    def closeEvent(self, event):
        """关闭事件"""
        if self.refresh_thread and self.refresh_thread.isRunning():
            reply = QMessageBox.question(
                self, "确认退出",
                "正在刷新订阅源，确定要退出吗？",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.refresh_thread.terminate()
                self.refresh_thread.wait()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()