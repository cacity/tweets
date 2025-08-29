# 🔥 RSS热门榜单系统

基于智能算法的RSS内容聚合推荐系统，支持AI智能摘要和多维度内容评分。

## ✨ 主要功能

### 1. 智能内容评分
- **时效性评分**: 根据内容发布时间计算新鲜度
- **质量评分**: 分析内容长度、结构、作者信息等
- **热度评分**: 基于关键词匹配计算受关注程度
- **来源权重**: 根据RSS源的权威性调整评分

### 2. AI增强功能
- 使用Google Gemini 1.5 Pro模型生成智能摘要
- 自动内容分类和标签
- 智能标题生成

### 3. 多维度榜单
- **综合榜单**: 基于全维度评分的Top内容
- **分类榜单**: 按主题分类的专业榜单
  - 🤖 人工智能
  - 💻 科技资讯
  - 💼 商业资讯
  - 📦 产品设计

### 4. 灵活的时间筛选
- 支持24小时、48小时或自定义时间范围
- 自动识别最新发布的内容

## 🚀 快速开始

### 环境要求
- Python 3.8+
- Google Gemini API密钥

### 安装依赖
```bash
pip install -r src/requirements.txt
```

### 配置环境变量
创建 `.env` 文件:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

### 启动应用
```bash
python src/app.py
```

访问: http://127.0.0.1:5001

## 🌐 Web界面使用

### 主要页面
- **首页**: 管理RSS订阅源
- **热门榜单**: 查看智能推荐内容
- **分类榜单**: 按主题浏览专业内容

### 生成榜单
1. 访问热门榜单页面
2. 点击"生成最新榜单"按钮
3. 系统将自动:
   - 刷新所有RSS源
   - 筛选24小时内容
   - 进行智能评分排序
   - 生成AI摘要
   - 创建分类榜单

## 🛠 命令行工具

### 直接生成榜单
```bash
# 基本生成
python src/trending_generator.py

# 自定义参数
python src/trending_generator.py --hours 48 --count 30 --refresh --gemini-key YOUR_KEY

# 不使用AI摘要
python src/trending_generator.py --no-ai
```

### 参数说明
- `--hours`: 筛选最近多少小时的内容 (默认24)
- `--count`: 每个榜单的条目数 (默认20) 
- `--refresh`: 是否先刷新RSS源
- `--no-ai`: 不使用AI生成摘要
- `--gemini-key`: 指定Gemini API密钥

## 📊 评分算法

综合评分 = 时效性(30%) + 质量(25%) + 热度(25%) + 来源权重(20%)

### 时效性评分
- 1小时内: 1.0分
- 6小时内: 0.9分
- 24小时内: 0.7分
- 48小时内: 0.5分
- 一周内: 0.3分

### 质量评分
基于以下因素:
- 标题长度和完整性
- 内容长度和结构
- 是否有作者信息
- 是否有原文链接
- HTML结构质量

### 热度评分
匹配以下关键词获得加分:
- AI/人工智能相关
- 科技技术相关
- 商业投资相关  
- 产品设计相关
- 包含数字和数据
- 引人注目的词汇

## 🎯 内容分类

系统自动将内容分为以下类别:

- **ai**: 人工智能、机器学习、大模型等
- **tech**: 科技资讯、技术趋势、开发工具等
- **business**: 商业资讯、投资融资、市场分析等
- **product**: 产品设计、用户体验、产品管理等
- **general**: 其他综合内容

## 📁 输出格式

榜单结果保存在 `trending_output/` 目录:

- `trending_result.json`: 完整结果(包含详细评分)
- `trending_simple.json`: 简化结果(用于前端显示)

### 结果结构
```json
{
  "meta": {
    "generated_at": "2025-08-29T14:30:00",
    "time_range_hours": 24,
    "total_source_items": 150,
    "ai_summary_enabled": true
  },
  "general": {
    "title": "24小时热门资讯 Top20",
    "items": [
      {
        "rank": 1,
        "title": "文章标题",
        "link": "原文链接",
        "summary": "AI生成的摘要",
        "score": 8.5,
        "category": "ai"
      }
    ]
  },
  "categories": {
    "ai": {
      "title": "人工智能热榜 Top20",
      "items": [...]
    }
  }
}
```

## 🔧 自定义配置

### 修改评分权重
编辑 `src/content_ranker.py`:
```python
total_score = (
    freshness_score * 0.3 +    # 时效性权重
    quality_score * 0.25 +     # 质量权重
    popularity_score * 0.25 +   # 热度权重
    source_weight * 0.2         # 来源权重
)
```

### 添加新的关键词
编辑热点关键词配置:
```python
self.hot_keywords = {
    'ai': ['AI', '人工智能', '新增关键词'],
    'custom': ['自定义分类关键词']
}
```

### 调整来源权重
```python
self.source_weights = {
    'your_domain.com': 0.9,  # 高权重源
    'default': 0.6
}
```

## 🚦 API接口

### 生成榜单
```http
POST /api/generate_trending
Content-Type: application/json

{
  "hours": 24,
  "count": 20,
  "refresh": true,
  "use_ai": true
}
```

### 获取榜单状态
```http
GET /api/trending_status
```

## ❓ 常见问题

### Q: 为什么没有生成摘要?
A: 请检查:
1. 是否设置了正确的Gemini API密钥
2. 网络连接是否正常
3. API配额是否充足

### Q: 榜单为空怎么办?
A: 可能原因:
1. RSS源中没有24小时内的新内容
2. 可以尝试增加时间范围(48-72小时)
3. 检查RSS源是否正常更新

### Q: 如何添加更多RSS源?
A: 通过Web界面的"添加订阅源"或"导入OPML"功能添加

### Q: 可以部署到服务器吗?
A: 可以，建议使用Gunicorn等WSGI服务器:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 src.app:app
```

## 📄 许可证

此项目为开源项目，遵循MIT许可证。

---

🎉 享受智能RSS阅读体验！如有问题请提交Issue。