"""
Twitter RSS订阅管理器 - Flask Web应用
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import os
import json
from datetime import datetime
from feed_manager import FeedManager
from models import Feed, FeedItem
from trending_generator import TrendingGenerator

# 获取项目根目录路径
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)

app = Flask(__name__, 
           template_folder=os.path.join(project_root, 'templates'),
           static_folder=os.path.join(project_root, 'static'))
app.secret_key = 'twitter_rss_manager_secret_key_2024'

# 初始化RSS管理器
feed_manager = FeedManager()

# 初始化热门榜单生成器
trending_generator = TrendingGenerator()

@app.route('/')
def index():
    """主页 - 显示所有订阅源"""
    feeds = feed_manager.get_all_feeds()
    return render_template('index.html', feeds=feeds)

@app.route('/feeds/<path:feed_url>')
def view_feed(feed_url):
    """查看特定订阅源的内容"""
    feed = feed_manager.get_feed_by_url(feed_url)
    if not feed:
        flash('订阅源不存在', 'error')
        return redirect(url_for('index'))
    
    return render_template('feed_detail.html', feed=feed)

@app.route('/add_feed', methods=['GET', 'POST'])
def add_feed():
    """添加新的订阅源"""
    if request.method == 'POST':
        url = request.form.get('url', '').strip()
        title = request.form.get('title', '').strip()
        
        if not url:
            flash('请输入RSS URL', 'error')
            return render_template('add_feed.html')
        
        success, message = feed_manager.add_feed_from_url(url, title)
        
        if success:
            flash(message, 'success')
            return redirect(url_for('index'))
        else:
            flash(message, 'error')
            return render_template('add_feed.html', url=url, title=title)
    
    return render_template('add_feed.html')

@app.route('/api/test_feed', methods=['POST'])
def test_feed():
    """API - 测试RSS订阅源有效性"""
    data = request.get_json()
    url = data.get('url', '').strip()
    
    if not url:
        return jsonify({'success': False, 'message': '请输入RSS URL'})
    
    try:
        import requests
        import feedparser
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        parsed_feed = feedparser.parse(response.content)
        
        if parsed_feed.bozo:
            return jsonify({'success': False, 'message': '无效的RSS格式'})
        
        title = parsed_feed.feed.get('title', 'Unknown Feed')
        return jsonify({
            'success': True, 
            'message': 'RSS订阅源有效',
            'title': title
        })
        
    except requests.RequestException as e:
        return jsonify({'success': False, 'message': f'网络错误: {str(e)}'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'测试失败: {str(e)}'})

@app.route('/api/refresh_feed/<path:feed_url>', methods=['POST'])
def refresh_feed(feed_url):
    """API - 刷新指定订阅源"""
    success, message = feed_manager.refresh_feed(feed_url)
    return jsonify({'success': success, 'message': message})

@app.route('/api/refresh_all', methods=['POST'])
def refresh_all_feeds():
    """API - 刷新所有订阅源"""
    results = feed_manager.refresh_all_feeds()
    success_count = sum(1 for r in results.values() if r['success'])
    total_count = len(results)
    
    return jsonify({
        'success': True,
        'message': f'刷新完成: {success_count}/{total_count} 成功',
        'results': results
    })

@app.route('/api/remove_feed/<path:feed_url>', methods=['DELETE'])
def remove_feed(feed_url):
    """API - 删除订阅源"""
    success = feed_manager.remove_feed(feed_url)
    if success:
        return jsonify({'success': True, 'message': '订阅源已删除'})
    else:
        return jsonify({'success': False, 'message': '删除失败'})

@app.route('/api/clear_all_feeds', methods=['DELETE'])
def clear_all_feeds():
    """API - 删除所有订阅源"""
    feeds = feed_manager.get_all_feeds()
    if not feeds:
        return jsonify({'success': False, 'message': '暂无订阅源可删除'})
    
    success = feed_manager.clear_all_feeds()
    if success:
        return jsonify({
            'success': True, 
            'message': f'已成功删除 {len(feeds)} 个订阅源'
        })
    else:
        return jsonify({'success': False, 'message': '删除失败'})

@app.route('/import_opml', methods=['GET', 'POST'])
def import_opml():
    """导入OPML文件"""
    if request.method == 'POST':
        if 'opml_file' not in request.files:
            flash('请选择OPML文件', 'error')
            return render_template('import_opml.html')
        
        file = request.files['opml_file']
        if file.filename == '':
            flash('请选择OPML文件', 'error')
            return render_template('import_opml.html')
        
        if file and (file.filename.endswith('.opml') or file.filename.endswith('.xml')):
            try:
                opml_content = file.read().decode('utf-8')
                success_count, total_count, error_messages = feed_manager.import_opml(opml_content)
                
                if total_count > 0:
                    flash(f'导入完成：{success_count}/{total_count} 个订阅源添加成功', 'success')
                    if error_messages:
                        flash(f'部分失败: {len(error_messages)} 个订阅源导入失败', 'warning')
                else:
                    flash('未找到有效的RSS订阅源', 'error')
                
                return redirect(url_for('index'))
                
            except Exception as e:
                flash(f'导入失败: {str(e)}', 'error')
        else:
            flash('请选择有效的OPML文件 (.opml 或 .xml)', 'error')
    
    return render_template('import_opml.html')

@app.route('/export_opml')
def export_opml():
    """导出OPML文件"""
    feeds = feed_manager.get_all_feeds()
    if not feeds:
        flash('暂无订阅源可导出', 'error')
        return redirect(url_for('index'))
    
    opml_content = feed_manager.export_opml()
    
    from flask import Response
    return Response(
        opml_content,
        mimetype='application/xml',
        headers={'Content-Disposition': 'attachment; filename=feeds.opml'}
    )

@app.route('/item')
def view_item():
    """查看单个RSS条目的详细内容"""
    feed_url = request.args.get('feed_url')
    item_guid = request.args.get('item_guid')
    
    # 调试信息
    print(f"Debug: feed_url = {feed_url}")
    print(f"Debug: item_guid = {item_guid}")
    
    if not feed_url or not item_guid:
        flash('参数错误', 'error')
        return redirect(url_for('index'))
    
    feed = feed_manager.get_feed_by_url(feed_url)
    if not feed:
        flash('订阅源不存在', 'error')
        return redirect(url_for('index'))
    
    # 查找指定的条目
    item = None
    for feed_item in feed.items:
        if feed_item.guid == item_guid:
            item = feed_item
            break
    
    if not item:
        flash('条目不存在', 'error')
        return redirect(url_for('view_feed', feed_url=feed_url))
    
    return render_template('item_detail.html', item=item, feed=feed)

@app.template_filter('format_datetime')
def format_datetime(value):
    """格式化日期时间"""
    if value is None:
        return "未知时间"
    
    if isinstance(value, str):
        try:
            value = datetime.fromisoformat(value)
        except:
            return value
    
    return value.strftime('%Y年%m月%d日 %H:%M')

@app.template_filter('clean_html')
def clean_html(text):
    """清理HTML标签，用于摘要显示"""
    import re
    if not text:
        return ""
    
    # 移除HTML标签
    clean = re.compile('<.*?>')
    text = re.sub(clean, '', text)
    
    # 移除多余的空白字符
    text = ' '.join(text.split())
    
    # 截断长文本
    if len(text) > 200:
        text = text[:200] + "..."
    
    return text

@app.route('/trending')
def trending():
    """热门榜单页面"""
    try:
        # 获取最新的榜单结果
        result = trending_generator.get_simplified_result()
        
        if not result:
            # 如果没有结果，显示空状态
            result = {
                'meta': {
                    'generated_at': None, 
                    'ai_summary_enabled': False,
                    'time_range_hours': 24,
                    'total_source_items': 0
                },
                'general': {
                    'title': '暂无热门内容',
                    'description': '点击生成最新榜单按钮开始创建',
                    'items': []
                },
                'categories': {}
            }
        
        # 确保result结构正确 - 使用字典访问而不是对象属性
        if not isinstance(result, dict):
            result = {'general': {'items': []}, 'categories': {}}
        
        if 'general' not in result:
            result['general'] = {'title': '暂无热门内容', 'items': []}
        
        if not isinstance(result['general'], dict):
            result['general'] = {'title': '暂无热门内容', 'items': []}
            
        if 'items' not in result['general']:
            result['general']['items'] = []
            
        if not isinstance(result['general']['items'], list):
            result['general']['items'] = []
            
        if 'categories' not in result:
            result['categories'] = {}
            
        if not isinstance(result['categories'], dict):
            result['categories'] = {}
        
        # 调试信息
        print(f"Debug: result类型: {type(result)}")
        if result:
            print(f"Debug: result结构: {list(result.keys()) if isinstance(result, dict) else 'not dict'}")
            if isinstance(result, dict) and 'general' in result:
                print(f"Debug: result.general类型: {type(result['general'])}")
                if isinstance(result['general'], dict) and 'items' in result['general']:
                    items = result['general']['items']
                    print(f"Debug: result.general.items类型: {type(items)}")
                    print(f"Debug: result.general.items长度: {len(items) if hasattr(items, '__len__') else 'no len'}")
                    print(f"Debug: items实际内容: {repr(items)[:200]}")
        
        return render_template('trending.html', result=result)
        
    except Exception as e:
        print(f"trending页面错误: {e}")
        print(f"错误类型: {type(e)}")
        import traceback
        traceback.print_exc()
        
        # 发生错误时返回最基本的结构
        error_result = {
            'meta': {'generated_at': None, 'ai_summary_enabled': False},
            'general': {'title': '页面加载出错', 'items': []},
            'categories': {}
        }
        
        print(f"Error result type: {type(error_result)}")
        print(f"Error result general items type: {type(error_result['general']['items'])}")
        
        return render_template('trending.html', result=error_result)

@app.route('/trending/<category>')
def trending_category(category):
    """分类榜单页面"""
    try:
        result = trending_generator.get_simplified_result()
        
        if not result or not isinstance(result, dict):
            flash('榜单数据不存在', 'error')
            return redirect(url_for('trending'))
        
        if 'categories' not in result or not isinstance(result['categories'], dict):
            flash('分类数据不存在', 'error')
            return redirect(url_for('trending'))
            
        if category not in result['categories']:
            flash('未找到指定分类的榜单', 'error')
            return redirect(url_for('trending'))
        
        category_data = result['categories'][category]
        
        # 确保category_data结构正确
        if not isinstance(category_data, dict):
            flash('分类数据格式错误', 'error')
            return redirect(url_for('trending'))
            
        if 'items' not in category_data:
            category_data['items'] = []
            
        if not isinstance(category_data['items'], list):
            category_data['items'] = []
        
        return render_template('trending_category.html', 
                             category=category, 
                             category_data=category_data,
                             result=result)
                             
    except Exception as e:
        print(f"分类榜单页面错误: {e}")
        flash('页面加载出错', 'error')
        return redirect(url_for('trending'))

@app.route('/api/generate_trending', methods=['POST'])
def api_generate_trending():
    """API - 生成热门榜单"""
    try:
        data = request.get_json() or {}
        hours = data.get('hours', 24)
        top_count = data.get('count', 20)
        refresh_feeds = data.get('refresh', False)
        use_ai_summary = data.get('use_ai', True)
        
        # 生成榜单
        result = trending_generator.generate_trending_lists(
            hours=hours,
            top_count=top_count,
            refresh_feeds=refresh_feeds,
            use_ai_summary=use_ai_summary
        )
        
        return jsonify({
            'success': True,
            'message': '热门榜单生成完成',
            'data': {
                'general_count': len(result['general']['items']),
                'categories_count': len(result['categories']),
                'generated_at': result['meta']['generated_at']
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'生成失败: {str(e)}'
        })

@app.route('/api/trending_status')
def api_trending_status():
    """API - 获取榜单状态"""
    result = trending_generator.get_simplified_result()
    
    if result:
        return jsonify({
            'success': True,
            'data': {
                'has_data': True,
                'generated_at': result['meta']['generated_at'],
                'general_count': len(result['general']['items']),
                'categories_count': len(result['categories']),
                'ai_enabled': result['meta']['ai_summary_enabled']
            }
        })
    else:
        return jsonify({
            'success': True,
            'data': {
                'has_data': False,
                'generated_at': None,
                'general_count': 0,
                'categories_count': 0,
                'ai_enabled': False
            }
        })

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5001)