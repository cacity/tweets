"""
智能内容评分和排序系统
根据多个维度对RSS内容进行评分排序
"""

import re
import math
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from models import FeedItem

@dataclass
class ContentScore:
    """内容评分结果"""
    total_score: float
    freshness_score: float  # 时效性
    quality_score: float    # 内容质量
    popularity_score: float # 热度
    source_weight: float    # 来源权重
    category: str          # 内容分类

class ContentRanker:
    """内容评分器"""
    
    def __init__(self):
        # 热点关键词配置
        self.hot_keywords = {
            'ai': ['AI', '人工智能', 'ChatGPT', 'GPT', 'Claude', 'Gemini', '机器学习', '深度学习', 'LLM', '大模型', 
                   'OpenAI', 'Google', 'Anthropic', '自动驾驶', '机器人', 'AGI', 'Transformer', 'AI应用'],
            'tech': ['科技', '技术', '互联网', '区块链', '云计算', '5G', '6G', '物联网', 'IoT', 'AR', 'VR', 'MR',
                     '量子计算', '芯片', '半导体', 'CPU', 'GPU', '算法', 'API', '开源', 'GitHub'],
            'business': ['商业', '创业', '投资', '融资', 'IPO', '上市', '收购', '并购', '估值', 'VC', 'PE',
                         '独角兽', '市场', '营收', '利润', '股价', '财报', '电商', '新零售'],
            'product': ['产品', '产品经理', 'PM', 'UX', 'UI', '设计', '用户体验', '产品设计', '需求分析',
                        '数据分析', '增长', '运营', 'KPI', 'OKR', 'MVP', '敏捷', 'Scrum']
        }
        
        # 来源权重配置（可以根据RSS源的权威性调整）
        self.source_weights = {
            # 知名科技媒体
            'techcrunch': 1.0,
            'wired': 1.0,
            'theverge': 1.0,
            'hacker': 0.9,
            # 中文科技媒体
            '36kr': 0.9,
            'geekpark': 0.8,
            'ifanr': 0.8,
            # 个人博客/自媒体
            'bestblogs': 0.7,  # 包含wechat2rss.bestblogs.dev等
            # 默认权重
            'default': 0.6
        }
    
    def score_content(self, item: FeedItem, feed_url: str = "") -> ContentScore:
        """对单个内容进行综合评分"""
        
        # 时效性评分
        freshness_score = self._score_freshness(item.published)
        
        # 内容质量评分
        quality_score = self._score_quality(item)
        
        # 热度评分
        popularity_score = self._score_popularity(item)
        
        # 来源权重
        source_weight = self._get_source_weight(feed_url)
        
        # 内容分类
        category = self._classify_content(item)
        
        # 综合评分计算
        total_score = (
            freshness_score * 0.3 +      # 时效性占30%
            quality_score * 0.25 +       # 质量占25%
            popularity_score * 0.25 +     # 热度占25%
            source_weight * 0.2           # 来源权重占20%
        )
        
        return ContentScore(
            total_score=round(total_score, 2),
            freshness_score=round(freshness_score, 2),
            quality_score=round(quality_score, 2),
            popularity_score=round(popularity_score, 2),
            source_weight=round(source_weight, 2),
            category=category
        )
    
    def _score_freshness(self, published: Optional[datetime]) -> float:
        """计算时效性评分（0-1）"""
        if not published:
            return 0.1
        
        now = datetime.now()
        if published.tzinfo is None:
            # 如果没有时区信息，假设是本地时间
            published = published.replace(tzinfo=now.tzinfo)
        elif now.tzinfo is None:
            # 统一时区
            now = now.replace(tzinfo=published.tzinfo)
        
        time_diff = now - published
        hours_ago = time_diff.total_seconds() / 3600
        
        # 时效性评分：越新越高分
        if hours_ago <= 1:      # 1小时内
            return 1.0
        elif hours_ago <= 6:    # 6小时内
            return 0.9
        elif hours_ago <= 24:   # 24小时内
            return 0.7
        elif hours_ago <= 48:   # 48小时内
            return 0.5
        elif hours_ago <= 168:  # 一周内
            return 0.3
        else:
            return 0.1
    
    def _score_quality(self, item: FeedItem) -> float:
        """计算内容质量评分（0-1）"""
        score = 0.0
        
        # 标题质量评分
        title = item.title or ""
        if len(title) >= 10:
            score += 0.2
        if len(title) >= 20:
            score += 0.1
        if len(title) <= 100:  # 标题不宜过长
            score += 0.1
        
        # 内容质量评分
        description = item.description or ""
        clean_desc = re.sub(r'<[^>]+>', '', description)  # 去除HTML标签
        
        if len(clean_desc) >= 100:
            score += 0.2
        if len(clean_desc) >= 500:
            score += 0.1
        if len(clean_desc) >= 1000:
            score += 0.1
        
        # 是否有链接
        if item.link:
            score += 0.1
        
        # 是否有作者信息
        if item.author:
            score += 0.1
        
        # 检查内容结构质量
        if self._has_good_structure(description):
            score += 0.1
        
        return min(score, 1.0)
    
    def _score_popularity(self, item: FeedItem) -> float:
        """计算热度评分（0-1）"""
        score = 0.0
        text = f"{item.title} {item.description}".lower()
        
        # 检查每个类别的关键词
        for category, keywords in self.hot_keywords.items():
            category_matches = sum(1 for keyword in keywords 
                                 if keyword.lower() in text)
            if category_matches > 0:
                # 根据匹配数量给分，但有上限
                category_score = min(category_matches * 0.15, 0.5)
                score += category_score
        
        # 检查是否包含数字（通常数据类内容更具价值）
        if re.search(r'\d+%|\d+\.\d+|\d+万|\d+亿|\$\d+', text):
            score += 0.1
        
        # 检查是否包含引人注目的词汇
        attention_words = ['突破', '首次', '重大', '震撼', '爆料', '独家', '最新', 
                          '发布', '上线', '更新', '升级', '革命性', '颠覆']
        if any(word in text for word in attention_words):
            score += 0.1
        
        return min(score, 1.0)
    
    def _get_source_weight(self, feed_url: str) -> float:
        """获取来源权重"""
        url_lower = feed_url.lower()
        
        for source, weight in self.source_weights.items():
            if source in url_lower:
                return weight
        
        return self.source_weights['default']
    
    def _classify_content(self, item: FeedItem) -> str:
        """内容分类"""
        text = f"{item.title} {item.description}".lower()
        category_scores = {}
        
        for category, keywords in self.hot_keywords.items():
            score = sum(1 for keyword in keywords if keyword.lower() in text)
            if score > 0:
                category_scores[category] = score
        
        if category_scores:
            return max(category_scores, key=category_scores.get)
        
        return 'general'
    
    def _has_good_structure(self, content: str) -> bool:
        """检查内容是否有良好结构"""
        if not content:
            return False
        
        # 检查是否有段落结构
        paragraphs = content.count('<p>')
        if paragraphs >= 2:
            return True
        
        # 检查是否有列表结构
        if '<ul>' in content or '<ol>' in content or '<li>' in content:
            return True
        
        # 检查是否有标题结构
        if any(tag in content for tag in ['<h1>', '<h2>', '<h3>', '<h4>']):
            return True
        
        return False
    
    def filter_recent_content(self, items: List[Tuple[FeedItem, str]], hours: int = 24) -> List[Tuple[FeedItem, str]]:
        """筛选指定时间内的内容"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        recent_items = []
        
        for item, feed_url in items:
            if item.published and item.published > cutoff_time:
                recent_items.append((item, feed_url))
            elif not item.published:
                # 如果没有发布时间，也包含进来（可能是最新的）
                recent_items.append((item, feed_url))
        
        return recent_items
    
    def rank_content(self, items: List[Tuple[FeedItem, str]], limit: int = 20, category: str = None) -> List[Dict[str, Any]]:
        """对内容进行排序并返回排行榜"""
        scored_items = []
        
        for item, feed_url in items:
            score = self.score_content(item, feed_url)
            
            # 如果指定了分类，只保留该分类的内容
            if category and score.category != category:
                continue
            
            scored_items.append({
                'item': item,
                'feed_url': feed_url,
                'score': score,
                'rank': 0  # 将在排序后设置
            })
        
        # 按总分降序排序
        scored_items.sort(key=lambda x: x['score'].total_score, reverse=True)
        
        # 设置排名并限制数量
        for i, scored_item in enumerate(scored_items[:limit]):
            scored_item['rank'] = i + 1
        
        return scored_items[:limit]
    
    def get_category_rankings(self, items: List[Tuple[FeedItem, str]], limit: int = 20) -> Dict[str, List[Dict[str, Any]]]:
        """获取各分类的排行榜"""
        rankings = {}
        
        # 为每个分类生成排行榜
        for category in list(self.hot_keywords.keys()) + ['general']:
            category_ranking = self.rank_content(items, limit, category)
            if category_ranking:  # 只保留有内容的分类
                rankings[category] = category_ranking
        
        return rankings