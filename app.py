"""
Twitter RSS订阅管理器 - Flask Web应用
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import os
import json
from datetime import datetime
from feed_manager import FeedManager
from models import Feed, FeedItem

app = Flask(__name__)
app.secret_key = 'twitter_rss_manager_secret_key_2024'

# 初始化RSS管理器
feed_manager = FeedManager()

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

@app.route('/item/<path:feed_url>/<item_guid>')
def view_item(feed_url, item_guid):
    """查看单个RSS条目的详细内容"""
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

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)