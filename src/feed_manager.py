"""
RSS订阅管理器
负责RSS内容的获取、解析和管理
"""

import json
import os
from datetime import datetime
from typing import List, Optional
import xml.etree.ElementTree as ET

import feedparser
import requests
from dateutil.parser import parse as date_parse

from models import Feed, FeedItem, FeedStore


class FeedManager:
    """RSS订阅管理器"""
    
    def __init__(self, data_file: str = "feeds_data.json"):
        # 如果是相对路径，确保相对于项目根目录
        if not os.path.isabs(data_file):
            # 获取当前文件所在目录的父目录（项目根目录）
            script_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(script_dir)
            self.data_file = os.path.join(project_root, data_file)
        else:
            self.data_file = data_file
        self.feed_store = FeedStore()
        self.load_feeds()
    
    def add_feed_from_url(self, url: str, title: str = "") -> tuple[bool, str]:
        """从URL添加RSS订阅源"""
        try:
            # 获取RSS内容
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            # 解析RSS内容
            parsed_feed = feedparser.parse(response.content)
            
            if parsed_feed.bozo:
                return False, "无效的RSS格式"
            
            # 创建Feed对象
            feed_title = title or parsed_feed.feed.get('title', 'Unknown Feed')
            feed_description = parsed_feed.feed.get('description', '')
            feed_link = parsed_feed.feed.get('link', '')
            
            feed = Feed(
                title=feed_title,
                url=url,
                description=feed_description,
                link=feed_link,
                last_updated=datetime.now()
            )
            
            # 解析RSS条目
            feed.items = self._parse_feed_items(parsed_feed.entries)
            
            # 添加到存储
            if self.feed_store.add_feed(feed):
                self.save_feeds()
                return True, "订阅源添加成功"
            else:
                return False, "订阅源已存在"
                
        except requests.RequestException as e:
            return False, f"网络错误: {str(e)}"
        except Exception as e:
            return False, f"解析错误: {str(e)}"
    
    def _parse_feed_items(self, entries) -> List[FeedItem]:
        """解析RSS条目"""
        items = []
        for entry in entries[:50]:  # 限制最多50个条目
            # 解析发布时间
            published = None
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                try:
                    published = datetime(*entry.published_parsed[:6])
                except:
                    pass
            elif hasattr(entry, 'published'):
                try:
                    published = date_parse(entry.published)
                except:
                    pass
            
            # 获取内容，优先使用content，然后是summary
            description = ''
            if hasattr(entry, 'content') and entry.content:
                # 如果有多个content条目，选择最长的
                content_parts = [c.get('value', '') for c in entry.content if c.get('value')]
                if content_parts:
                    description = max(content_parts, key=len)
            
            if not description:
                description = entry.get('summary', entry.get('description', ''))
            
            # 清理和增强HTML内容
            description = self._clean_and_enhance_html(description)
            
            # 生成唯一标识符 - 优先使用id或guid，否则基于link或title生成
            guid = entry.get('id', entry.get('guid', ''))
            if not guid:
                # 如果没有id或guid，使用link的hash值作为唯一标识
                link = entry.get('link', '')
                title = entry.get('title', 'No Title')
                if link:
                    guid = str(hash(link))
                else:
                    # 如果连link都没有，使用title和发布时间生成
                    pub_str = published.isoformat() if published else 'no_date'
                    guid = str(hash(f"{title}_{pub_str}"))
            
            item = FeedItem(
                title=entry.get('title', 'No Title'),
                link=entry.get('link', ''),
                description=description,
                published=published,
                author=entry.get('author', ''),
                guid=guid
            )
            items.append(item)
        
        return items
    
    def _clean_and_enhance_html(self, html_content: str) -> str:
        """清理和增强HTML内容"""
        if not html_content:
            return ''
        
        import re
        import html
        
        # 解码HTML实体
        content = html.unescape(html_content)
        
        # 移除完整的style属性（如style="font-family: Arial; color: #333;"）
        content = re.sub(
            r'\s*style\s*=\s*["\'][^"\'>]*["\']',
            '',
            content,
            flags=re.IGNORECASE
        )
        
        # 移除内联CSS样式字符串（如#ffffff; border: 1px solid #e1e8ed; padding: 0; line-height: 1.5;）
        content = re.sub(
            r'#[0-9a-fA-F]{3,6};\s*[^;]*;[^<>]*',
            '',
            content,
            flags=re.IGNORECASE
        )
        
        # 移除单独的CSS属性字符串（如border: 1px solid, padding: 0等）
        content = re.sub(
            r'\b(?:border|padding|margin|color|background|font|width|height|display|position|overflow|line-height|font-size|font-family|white-space)\s*:\s*[^;\n<>]+;?',
            '',
            content,
            flags=re.IGNORECASE
        )
        
        # 移除单独的颜色值（如#ffffff, #e1e8ed等）
        content = re.sub(
            r'\s*#[0-9a-fA-F]{3,6}\s*',
            ' ',
            content
        )
        
        # 移除单独出现的CSS单位（如px, em, %等）
        content = re.sub(
            r'\b\d+(?:px|em|rem|%|pt|vh|vw)\b',
            '',
            content
        )
        
        # 移除空的HTML标签属性（如<div >）
        content = re.sub(
            r'<(\w+)\s+>',
            r'<\1>',
            content
        )
        
        # 移除多余的分号和空白字符
        content = re.sub(r';+', ';', content)
        content = re.sub(r'\s*;\s*', '; ', content)
        content = re.sub(r'\s+', ' ', content)
        
        # 移除单独的分号和只包含空白的段落
        content = re.sub(r'<p[^>]*>\s*;*\s*</p>', '', content, flags=re.IGNORECASE)
        content = re.sub(r'<div[^>]*>\s*;*\s*</div>', '', content, flags=re.IGNORECASE)
        
        # 移除只包含> 符号的标签
        content = re.sub(r'<([^>]+)>\s*>\s*</\1>', '', content, flags=re.IGNORECASE)
        content = re.sub(r'>\s*>', '>', content)
        
        # 确保图片标签有正确的属性
        content = re.sub(
            r'<img([^>]*?)>',
            lambda m: self._fix_img_tag(m.group(0)),
            content,
            flags=re.IGNORECASE
        )
        
        # 确保链接在新窗口打开
        content = re.sub(
            r'<a([^>]*?)href="([^"]*?)"([^>]*?)>',
            r'<a\1href="\2"\3 target="_blank" rel="noopener noreferrer">',
            content,
            flags=re.IGNORECASE
        )
        
        # 处理空白的图片标签
        content = re.sub(
            r'<img[^>]*?src=""[^>]*?>',
            '<div class="image-placeholder"><i class="bi bi-image"></i><p>图片链接无效</p></div>',
            content,
            flags=re.IGNORECASE
        )
        
        # 最后清理：移除空的标签和多余的空白
        content = re.sub(r'<([^>]+)>\s*</\1>', '', content, flags=re.IGNORECASE)
        content = re.sub(r'\s+', ' ', content)
        content = content.strip()
        
        return content
    
    def _fix_img_tag(self, img_tag: str) -> str:
        """修复图片标签，确保有正确的属性"""
        import re
        
        # 如果没有alt属性，添加默认值
        if 'alt=' not in img_tag.lower():
            img_tag = img_tag.replace('>', ' alt="图片">', 1)
        
        # 如果没有loading属性，添加lazy loading
        if 'loading=' not in img_tag.lower():
            img_tag = img_tag.replace('>', ' loading="lazy">', 1)
        
        # 确保有style或class用于响应式
        if 'style=' not in img_tag.lower() and 'class=' not in img_tag.lower():
            img_tag = img_tag.replace('>', ' style="max-width: 100%; height: auto;">', 1)
        
        return img_tag
    
    def refresh_feed(self, url: str) -> tuple[bool, str]:
        """刷新指定的RSS订阅源"""
        feed = self.feed_store.get_feed_by_url(url)
        if not feed:
            return False, "订阅源不存在"
        
        try:
            # 获取最新RSS内容
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            parsed_feed = feedparser.parse(response.content)
            
            if parsed_feed.bozo:
                return False, "无效的RSS格式"
            
            # 更新Feed信息
            feed.description = parsed_feed.feed.get('description', feed.description)
            feed.link = parsed_feed.feed.get('link', feed.link)
            feed.last_updated = datetime.now()
            feed.items = self._parse_feed_items(parsed_feed.entries)
            
            self.feed_store.update_feed(url, feed)
            self.save_feeds()
            
            return True, "刷新成功"
            
        except requests.RequestException as e:
            return False, f"网络错误: {str(e)}"
        except Exception as e:
            return False, f"刷新错误: {str(e)}"
    
    def refresh_all_feeds(self) -> dict:
        """刷新所有RSS订阅源"""
        results = {}
        for feed in self.feed_store.get_all_feeds():
            success, message = self.refresh_feed(feed.url)
            results[feed.url] = {'success': success, 'message': message}
        return results
    
    def remove_feed(self, url: str) -> bool:
        """移除RSS订阅源"""
        if self.feed_store.remove_feed(url):
            self.save_feeds()
            return True
        return False
    
    def clear_all_feeds(self) -> bool:
        """删除所有RSS订阅源"""
        if self.feed_store.clear_all():
            self.save_feeds()
            return True
        return False
    
    def get_all_feeds(self) -> List[Feed]:
        """获取所有RSS订阅源"""
        return self.feed_store.get_all_feeds()
    
    def get_feed_by_url(self, url: str) -> Optional[Feed]:
        """根据URL获取RSS订阅源"""
        return self.feed_store.get_feed_by_url(url)
    
    def import_opml(self, opml_content: str) -> tuple[int, int, List[str]]:
        """导入OPML文件
        返回: (成功数量, 总数量, 错误信息列表)
        """
        try:
            root = ET.fromstring(opml_content)
            success_count = 0
            total_count = 0
            error_messages = []
            
            # 查找所有outline元素
            for outline in root.iter('outline'):
                xml_url = outline.get('xmlUrl')
                if xml_url:
                    total_count += 1
                    # 优先使用title，其次使用text属性
                    title = outline.get('title') or outline.get('text', '')
                    
                    # 清理标题，移除HTML实体编码
                    if title:
                        import html
                        title = html.unescape(title)
                        # 移除Unicode表情符号和特殊字符
                        import re
                        title = re.sub(r'[\U0001F600-\U0001F64F]|[\U0001F300-\U0001F5FF]|[\U0001F680-\U0001F6FF]|[\U0001F1E0-\U0001F1FF]', '', title)
                        title = title.strip()
                    
                    print(f"正在添加: {title} - {xml_url}")
                    
                    success, message = self.add_feed_from_url(xml_url, title)
                    if success:
                        success_count += 1
                        print(f"✓ 成功添加: {title}")
                    else:
                        error_msg = f"添加失败 '{title}': {message}"
                        error_messages.append(error_msg)
                        print(f"✗ {error_msg}")
            
            return success_count, total_count, error_messages
            
        except ET.ParseError as e:
            return 0, 0, [f"OPML文件解析错误: {str(e)}"]
        except Exception as e:
            return 0, 0, [f"导入错误: {str(e)}"]
    
    def export_opml(self) -> str:
        """导出为OPML格式"""
        root = ET.Element('opml', version='2.0')
        root.set('xmlns', 'http://www.opml.org/spec2')
        
        head = ET.SubElement(root, 'head')
        title = ET.SubElement(head, 'title')
        title.text = 'Twitter RSS Feeds Export'
        
        date_created = ET.SubElement(head, 'dateCreated')
        from datetime import datetime
        date_created.text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')
        
        docs = ET.SubElement(head, 'docs')
        docs.text = 'http://www.opml.org/spec2'
        
        body = ET.SubElement(root, 'body')
        
        for feed in self.feed_store.get_all_feeds():
            outline = ET.SubElement(body, 'outline')
            outline.set('text', feed.title)
            outline.set('title', feed.title)
            outline.set('type', 'rss')
            outline.set('xmlUrl', feed.url)
            if feed.link:
                outline.set('htmlUrl', feed.link)
            if feed.description:
                outline.set('description', feed.description[:200])  # 限制描述长度
        
        return ET.tostring(root, encoding='unicode', xml_declaration=True)
    
    def save_feeds(self):
        """保存订阅源数据到文件"""
        try:
            data = []
            for feed in self.feed_store.get_all_feeds():
                feed_data = {
                    'title': feed.title,
                    'url': feed.url,
                    'description': feed.description,
                    'link': feed.link,
                    'last_updated': feed.last_updated.isoformat() if feed.last_updated else None,
                    'items': []
                }
                
                for item in feed.items:
                    item_data = {
                        'title': item.title,
                        'link': item.link,
                        'description': item.description,
                        'published': item.published.isoformat() if item.published else None,
                        'author': item.author,
                        'guid': item.guid
                    }
                    feed_data['items'].append(item_data)
                
                data.append(feed_data)
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"保存数据失败: {e}")
    
    def load_feeds(self):
        """从文件加载订阅源数据"""
        if not os.path.exists(self.data_file):
            return
        
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for feed_data in data:
                # 解析时间
                last_updated = None
                if feed_data.get('last_updated'):
                    try:
                        last_updated = datetime.fromisoformat(feed_data['last_updated'])
                    except:
                        pass
                
                feed = Feed(
                    title=feed_data['title'],
                    url=feed_data['url'],
                    description=feed_data.get('description', ''),
                    link=feed_data.get('link', ''),
                    last_updated=last_updated
                )
                
                # 解析条目
                items = []
                for item_data in feed_data.get('items', []):
                    published = None
                    if item_data.get('published'):
                        try:
                            published = datetime.fromisoformat(item_data['published'])
                        except:
                            pass
                    
                    item = FeedItem(
                        title=item_data['title'],
                        link=item_data['link'],
                        description=item_data.get('description', ''),
                        published=published,
                        author=item_data.get('author', ''),
                        guid=item_data.get('guid', '')
                    )
                    items.append(item)
                
                feed.items = items
                self.feed_store.add_feed(feed)
                
        except Exception as e:
            print(f"加载数据失败: {e}")
    
    def get_all_content_items(self) -> List[tuple]:
        """获取所有RSS源的所有内容项，返回(FeedItem, feed_url)的列表"""
        all_items = []
        
        for feed in self.feed_store.feeds:
            for item in feed.items:
                all_items.append((item, feed.url))
        
        return all_items
    
    def get_recent_content(self, hours: int = 24) -> List[tuple]:
        """获取指定时间内的内容，返回(FeedItem, feed_url)的列表"""
        from datetime import datetime, timedelta
        
        cutoff_time = datetime.now() - timedelta(hours=hours)
        recent_items = []
        
        all_items = self.get_all_content_items()
        for item, feed_url in all_items:
            if item.published and item.published > cutoff_time:
                recent_items.append((item, feed_url))
            elif not item.published:
                # 如果没有发布时间，也包含进来（可能是最新的）
                recent_items.append((item, feed_url))
        
        return recent_items
    
    def refresh_all_feeds_bulk(self) -> dict:
        """批量刷新所有RSS源（用于热榜功能）"""
        print("开始批量刷新所有RSS源...")
        results = {}
        total_feeds = len(self.feed_store.feeds)
        
        for i, feed in enumerate(self.feed_store.feeds, 1):
            print(f"刷新 {i}/{total_feeds}: {feed.title}")
            success, message = self.refresh_feed(feed.url)
            results[feed.url] = {
                'success': success,
                'message': message
            }
        
        self.save_feeds()
        print("批量刷新完成！")
        return results