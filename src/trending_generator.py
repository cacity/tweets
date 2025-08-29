"""
热门内容榜单生成器
整合内容评分、AI摘要、分类等功能生成智能榜单
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import asdict
from dotenv import load_dotenv

from feed_manager import FeedManager
from content_ranker import ContentRanker, ContentScore
from gemini_service import GeminiService

# 加载环境变量
load_dotenv()

class TrendingGenerator:
    """热门内容榜单生成器"""
    
    def __init__(self, gemini_api_key: str = None):
        """
        初始化榜单生成器
        
        Args:
            gemini_api_key: Gemini API密钥
        """
        self.feed_manager = FeedManager()
        self.content_ranker = ContentRanker()
        self.gemini_service = GeminiService(gemini_api_key)
        
        # 确保output目录存在
        self.output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'trending_output')
        os.makedirs(self.output_dir, exist_ok=True)
        
        print("热门榜单生成器初始化完成！")
    
    def generate_trending_lists(self, 
                              hours: int = 24, 
                              top_count: int = 20,
                              refresh_feeds: bool = False,
                              use_ai_summary: bool = True) -> Dict[str, Any]:
        """
        生成热门榜单
        
        Args:
            hours: 筛选最近多少小时的内容
            top_count: 每个榜单的条目数
            refresh_feeds: 是否先刷新RSS源
            use_ai_summary: 是否使用AI生成摘要
            
        Returns:
            包含所有榜单的字典
        """
        print("=" * 50)
        print("🚀 开始生成热门榜单")
        print("=" * 50)
        
        # 步骤1: 刷新RSS源（可选）
        if refresh_feeds:
            print("📡 刷新所有RSS源...")
            self.feed_manager.refresh_all_feeds_bulk()
        
        # 步骤2: 获取最近内容
        print(f"📅 获取最近{hours}小时的内容...")
        recent_items = self.feed_manager.get_recent_content(hours)
        print(f"找到 {len(recent_items)} 条最近内容")
        
        if not recent_items:
            print("⚠️ 没有找到最近的内容")
            return self._create_empty_result()
        
        # 步骤3: 内容评分和排序
        print("🎯 进行内容评分和排序...")
        
        # 生成综合榜单
        general_ranking = self.content_ranker.rank_content(recent_items, top_count)
        print(f"生成综合榜单：{len(general_ranking)} 条")
        
        # 生成分类榜单
        category_rankings = self.content_ranker.get_category_rankings(recent_items, top_count)
        print(f"生成分类榜单：{len(category_rankings)} 个分类")
        
        # 步骤4: AI增强（生成摘要）
        if use_ai_summary and self.gemini_service.enabled:
            print("🤖 使用AI生成摘要...")
            general_ranking = self.gemini_service.batch_generate_summaries(general_ranking)
            
            for category, items in category_rankings.items():
                print(f"为 {category} 分类生成摘要...")
                category_rankings[category] = self.gemini_service.batch_generate_summaries(items)
        
        # 步骤5: 生成最终结果
        result = self._create_result(
            general_ranking=general_ranking,
            category_rankings=category_rankings,
            hours=hours,
            total_items=len(recent_items)
        )
        
        # 步骤6: 保存结果
        self._save_result(result)
        
        print("=" * 50)
        print("✅ 热门榜单生成完成！")
        print(f"📊 综合榜单：{len(general_ranking)} 条")
        print(f"📂 分类榜单：{len(category_rankings)} 个分类")
        print("=" * 50)
        
        return result
    
    def _create_result(self, 
                      general_ranking: List[Dict],
                      category_rankings: Dict[str, List[Dict]],
                      hours: int,
                      total_items: int) -> Dict[str, Any]:
        """创建结果字典"""
        
        # 生成标题
        general_title = f"24小时热门资讯 Top{len(general_ranking)}"
        if self.gemini_service.enabled:
            general_title = self.gemini_service.create_trending_title('general', len(general_ranking))
        
        result = {
            'meta': {
                'generated_at': datetime.now().isoformat(),
                'time_range_hours': hours,
                'total_source_items': total_items,
                'ai_summary_enabled': self.gemini_service.enabled
            },
            'general': {
                'title': general_title,
                'description': f"基于{total_items}条内容的智能推荐榜单",
                'items': self._format_ranking_items(general_ranking)
            },
            'categories': {}
        }
        
        # 添加分类榜单
        for category, items in category_rankings.items():
            if items:  # 只添加有内容的分类
                category_title = f"{self._get_category_display_name(category)} Top{len(items)}"
                if self.gemini_service.enabled:
                    category_title = self.gemini_service.create_trending_title(category, len(items))
                
                result['categories'][category] = {
                    'title': category_title,
                    'description': f"{self._get_category_display_name(category)}领域热门内容",
                    'items': self._format_ranking_items(items)
                }
        
        return result
    
    def _format_ranking_items(self, ranking_items: List[Dict]) -> List[Dict]:
        """格式化榜单项目"""
        formatted_items = []
        
        for item_data in ranking_items:
            feed_item = item_data['item']
            score = item_data['score']
            
            formatted_item = {
                'rank': item_data['rank'],
                'title': feed_item.title,
                'link': feed_item.link,
                'description': feed_item.description,
                'summary': item_data.get('summary', ''),
                'published': feed_item.published.isoformat() if feed_item.published else None,
                'author': feed_item.author,
                'source_url': item_data['feed_url'],
                'score': {
                    'total': score.total_score,
                    'freshness': score.freshness_score,
                    'quality': score.quality_score,
                    'popularity': score.popularity_score,
                    'source_weight': score.source_weight,
                    'category': score.category
                }
            }
            
            formatted_items.append(formatted_item)
        
        return formatted_items
    
    def _get_category_display_name(self, category: str) -> str:
        """获取分类的显示名称"""
        names = {
            'ai': '人工智能',
            'tech': '科技资讯',
            'business': '商业资讯', 
            'product': '产品设计',
            'general': '综合资讯'
        }
        return names.get(category, category)
    
    def _create_empty_result(self) -> Dict[str, Any]:
        """创建空结果"""
        return {
            'meta': {
                'generated_at': datetime.now().isoformat(),
                'time_range_hours': 24,
                'total_source_items': 0,
                'ai_summary_enabled': self.gemini_service.enabled
            },
            'general': {
                'title': '暂无热门内容',
                'description': '没有找到最近的内容',
                'items': []
            },
            'categories': {}
        }
    
    def _save_result(self, result: Dict[str, Any]):
        """保存结果到文件"""
        try:
            # 保存完整结果
            result_file = os.path.join(self.output_dir, 'trending_result.json')
            with open(result_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            
            # 保存简化版本（用于前端显示）
            simplified = self._create_simplified_result(result)
            simple_file = os.path.join(self.output_dir, 'trending_simple.json')
            with open(simple_file, 'w', encoding='utf-8') as f:
                json.dump(simplified, f, ensure_ascii=False, indent=2)
            
            print(f"📁 结果已保存到: {self.output_dir}")
            
        except Exception as e:
            print(f"保存结果失败: {e}")
    
    def _create_simplified_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """创建简化的结果（去掉一些详细信息）"""
        simplified = {
            'meta': result['meta'],
            'general': {
                'title': result['general']['title'],
                'items': []
            },
            'categories': {}
        }
        
        # 简化综合榜单项目
        for item in result['general']['items']:
            simplified_item = {
                'rank': item['rank'],
                'title': item['title'],
                'link': item['link'],
                'summary': item.get('summary', item['description'][:150] + "..." if len(item['description']) > 150 else item['description']),
                'published': item['published'],
                'author': item['author'],
                'score': item['score']['total']
            }
            simplified['general']['items'].append(simplified_item)
        
        # 简化分类榜单
        for category, data in result['categories'].items():
            simplified['categories'][category] = {
                'title': data['title'],
                'items': []
            }
            
            for item in data['items']:
                simplified_item = {
                    'rank': item['rank'],
                    'title': item['title'],
                    'link': item['link'],
                    'summary': item.get('summary', item['description'][:100] + "..." if len(item['description']) > 100 else item['description']),
                    'score': item['score']['total']
                }
                simplified['categories'][category]['items'].append(simplified_item)
        
        return simplified
    
    def get_latest_result(self) -> Optional[Dict[str, Any]]:
        """获取最新的榜单结果"""
        try:
            result_file = os.path.join(self.output_dir, 'trending_result.json')
            if os.path.exists(result_file):
                with open(result_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return None
        except Exception as e:
            print(f"读取榜单结果失败: {e}")
            return None
    
    def get_simplified_result(self) -> Optional[Dict[str, Any]]:
        """获取简化的榜单结果"""
        try:
            simple_file = os.path.join(self.output_dir, 'trending_simple.json')
            if os.path.exists(simple_file):
                with open(simple_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return None
        except Exception as e:
            print(f"读取简化榜单结果失败: {e}")
            return None


# 命令行工具函数
def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='生成RSS热门内容榜单')
    parser.add_argument('--hours', type=int, default=24, help='筛选最近多少小时的内容')
    parser.add_argument('--count', type=int, default=20, help='每个榜单的条目数')
    parser.add_argument('--refresh', action='store_true', help='是否先刷新RSS源')
    parser.add_argument('--no-ai', action='store_true', help='不使用AI生成摘要')
    parser.add_argument('--gemini-key', type=str, help='Gemini API密钥')
    
    args = parser.parse_args()
    
    generator = TrendingGenerator(gemini_api_key=args.gemini_key)
    
    result = generator.generate_trending_lists(
        hours=args.hours,
        top_count=args.count,
        refresh_feeds=args.refresh,
        use_ai_summary=not args.no_ai
    )
    
    print(f"\n📈 生成完成！")
    print(f"综合榜单：{len(result['general']['items'])} 条")
    print(f"分类榜单：{len(result['categories'])} 个")


if __name__ == "__main__":
    main()