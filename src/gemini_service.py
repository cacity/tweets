"""
Google Gemini API服务
用于生成内容摘要和分析
"""

import os
import re
import time
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
import google.generativeai as genai
from models import FeedItem

# 加载环境变量
load_dotenv()

class GeminiService:
    """Gemini API服务类"""
    
    def __init__(self, api_key: str = None):
        """
        初始化Gemini服务
        
        Args:
            api_key: Google Gemini API密钥，如果不提供会从环境变量GEMINI_API_KEY获取
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        
        if not self.api_key:
            print("警告: 未设置Gemini API密钥。请设置环境变量GEMINI_API_KEY或在初始化时提供api_key参数")
            self.enabled = False
            return
        
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-pro')  # 使用gemini-1.5-pro模型
            self.enabled = True
            print("Gemini API服务初始化成功 - 使用gemini-1.5-pro模型")
        except Exception as e:
            print(f"Gemini API初始化失败: {e}")
            self.enabled = False
    
    def generate_summary(self, content: str, max_length: int = 150) -> Optional[str]:
        """
        生成内容摘要
        
        Args:
            content: 原始内容
            max_length: 摘要最大长度
            
        Returns:
            摘要文本，如果生成失败返回None
        """
        if not self.enabled:
            return None
        
        try:
            # 清理HTML标签
            clean_content = re.sub(r'<[^>]+>', '', content)
            clean_content = re.sub(r'\s+', ' ', clean_content).strip()
            
            # 如果内容太短，直接返回
            if len(clean_content) <= max_length:
                return clean_content
            
            # 构建提示词
            prompt = f"""
请为以下内容生成一个简洁、准确的中文摘要，要求：
1. 摘要长度不超过{max_length}个字符
2. 抓住核心信息和关键点
3. 语言简洁明了，适合快速阅读
4. 保持客观中性的语调

原文内容：
{clean_content[:2000]}  # 限制输入长度避免超过token限制

摘要：
"""
            
            response = self.model.generate_content(prompt)
            summary = response.text.strip()
            
            # 确保摘要长度合适
            if len(summary) > max_length:
                summary = summary[:max_length-3] + "..."
            
            return summary
            
        except Exception as e:
            print(f"生成摘要失败: {e}")
            return None
    
    def batch_generate_summaries(self, items: List[Dict[str, Any]], max_length: int = 150, delay: float = 0.5) -> List[Dict[str, Any]]:
        """
        批量生成摘要
        
        Args:
            items: 包含内容的字典列表
            max_length: 摘要最大长度
            delay: 请求间隔（秒），避免API限制
            
        Returns:
            添加了摘要的内容列表
        """
        if not self.enabled:
            print("Gemini API未启用，跳过摘要生成")
            return items
        
        print(f"开始批量生成{len(items)}个内容的摘要...")
        
        for i, item in enumerate(items, 1):
            try:
                feed_item = item['item']
                content = f"{feed_item.title}\n\n{feed_item.description or ''}"
                
                summary = self.generate_summary(content, max_length)
                item['summary'] = summary
                
                print(f"已生成 {i}/{len(items)} 个摘要")
                
                # 添加延迟避免API限制
                if i < len(items):
                    time.sleep(delay)
                    
            except Exception as e:
                print(f"生成第{i}个摘要时出错: {e}")
                item['summary'] = None
        
        print("批量摘要生成完成！")
        return items
    
    def analyze_content_category(self, content: str) -> Optional[str]:
        """
        分析内容类别
        
        Args:
            content: 内容文本
            
        Returns:
            内容类别
        """
        if not self.enabled:
            return None
        
        try:
            prompt = f"""
请分析以下内容的主要类别，从以下选项中选择最合适的一个：
- ai: 人工智能相关
- tech: 科技技术相关  
- business: 商业投资相关
- product: 产品设计相关
- general: 其他通用内容

只回答类别名称，不要其他解释。

内容：{content[:500]}

类别：
"""
            
            response = self.model.generate_content(prompt)
            category = response.text.strip().lower()
            
            # 验证返回的类别是否有效
            valid_categories = ['ai', 'tech', 'business', 'product', 'general']
            if category in valid_categories:
                return category
            else:
                return 'general'
                
        except Exception as e:
            print(f"分析内容类别失败: {e}")
            return None
    
    def enhance_content_with_ai(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        使用AI增强内容信息
        
        Args:
            items: 内容列表
            
        Returns:
            增强后的内容列表
        """
        if not self.enabled:
            return items
        
        print("使用AI增强内容信息...")
        
        for i, item in enumerate(items, 1):
            try:
                feed_item = item['item']
                content = f"{feed_item.title}\n\n{feed_item.description or ''}"
                
                # 生成摘要
                if 'summary' not in item or not item['summary']:
                    item['summary'] = self.generate_summary(content)
                
                # 分析类别（如果需要更准确的分类）
                if item['score'].category == 'general':
                    ai_category = self.analyze_content_category(content)
                    if ai_category:
                        item['score'].category = ai_category
                
                print(f"已增强 {i}/{len(items)} 个内容")
                
                # 添加延迟
                time.sleep(0.3)
                
            except Exception as e:
                print(f"增强第{i}个内容时出错: {e}")
        
        return items
    
    def create_trending_title(self, category: str, item_count: int) -> str:
        """
        为热榜创建标题
        
        Args:
            category: 内容类别
            item_count: 内容数量
            
        Returns:
            热榜标题
        """
        if not self.enabled:
            return self._get_default_title(category, item_count)
        
        try:
            category_names = {
                'ai': '人工智能',
                'tech': '科技资讯', 
                'business': '商业资讯',
                'product': '产品设计',
                'general': '综合资讯'
            }
            
            category_name = category_names.get(category, '热门资讯')
            
            prompt = f"""
请为一个包含{item_count}条{category_name}内容的热榜创建一个吸引人的标题。
要求：
1. 标题简洁有力，不超过20个字
2. 体现时效性和热度
3. 符合中文表达习惯
4. 突出{category_name}的特色

示例格式：
- 今日AI热点Top{item_count}
- {category_name}周刊·{item_count}条必读
- 最新{category_name}趋势解读

标题：
"""
            
            response = self.model.generate_content(prompt)
            title = response.text.strip()
            
            # 确保标题长度合适
            if len(title) > 30:
                title = title[:27] + "..."
            
            return title
            
        except Exception as e:
            print(f"生成热榜标题失败: {e}")
            return self._get_default_title(category, item_count)
    
    def _get_default_title(self, category: str, item_count: int) -> str:
        """获取默认标题"""
        category_names = {
            'ai': '人工智能热榜',
            'tech': '科技资讯热榜', 
            'business': '商业资讯热榜',
            'product': '产品设计热榜',
            'general': '综合资讯热榜'
        }
        
        category_name = category_names.get(category, '热门资讯')
        return f"{category_name} Top{item_count}"