# RSS智能热门榜单系统

一个基于AI的RSS订阅管理和热门内容智能推荐系统，集成了多维度内容评分、自动分类和AI摘要生成功能。

## 🌟 核心功能

### 📡 RSS订阅源管理
- 添加、编辑、删除RSS订阅源（支持174+订阅源）
- 自动刷新订阅内容，支持批量更新
- OPML格式导入/导出支持
- 现代化响应式Web界面

### 🏆 智能热门榜单系统 ⭐
- **多维度评分算法**：时效性(30%) + 质量(25%) + 热度(25%) + 来源权重(20%)
- **24小时内容筛选**：自动筛选最新内容，可配置时间范围
- **自动内容分类**：AI、科技资讯、商业资讯、产品设计等分类
- **综合榜单**：全平台Top内容智能推荐
- **分类榜单**：按主题分类的专业榜单
- **精美UI展示**：现代化排行榜界面，包含排名徽章、评分显示

### 🤖 AI增强功能
- **Google Gemini 1.5 Pro集成**：智能内容摘要生成
- **批量AI处理**：支持批量生成高质量中文摘要
- **智能分类**：基于关键词和AI分析的自动内容分类
- **动态标题生成**：AI生成榜单标题

### 📰 增强内容展示
- HTML内容渲染：支持富文本格式、图片显示、段落格式
- 图片支持：自动加载和显示内嵌图片
- 展开/收缩：可切换内容显示模式
- 详细内容：可打开单独窗口查看完整内容

## 安装要求

- Python 3.7+
- Flask
- requests
- feedparser
- python-dateutil
- google-generativeai
- python-dotenv

## 快速开始

### 1. 环境配置

创建 `.env` 文件配置Gemini API密钥（用于AI摘要功能）：
```bash
GEMINI_API_KEY=your_api_key_here
```

### 2. 安装依赖

```bash
pip install -r src/requirements.txt
```

### 3. 运行程序

```bash
python src/app.py
```

然后在浏览器中访问 `http://127.0.0.1:5001`

### 4. 核心页面
- **主页**：`http://127.0.0.1:5001/` - RSS源管理
- **热门榜单**：`http://127.0.0.1:5001/trending` - 智能推荐榜单 ⭐

## 使用说明

### 🏆 热门榜单系统 (主要功能)

#### 生成智能榜单
1. 访问 `/trending` 页面
2. 点击 "生成最新榜单" 按钮
3. 配置参数：
   - **时间范围**：筛选最近24小时内容（可调整）
   - **榜单长度**：Top 20条目（可调整）
   - **是否刷新RSS源**：建议勾选以获取最新内容
   - **AI摘要**：启用Gemini AI生成智能摘要

#### 查看榜单
- **综合榜单**：全平台最热门内容推荐
- **分类榜单**：
  - 🤖 **人工智能**：AI、机器学习、大模型相关
  - 💻 **科技资讯**：技术趋势、开发工具、区块链
  - 💼 **商业资讯**：投资融资、市场分析、电商
  - 🎨 **产品设计**：产品管理、用户体验、设计

#### API接口
```bash
# 生成榜单
POST /api/generate_trending
{
  "hours": 24,
  "count": 20, 
  "refresh": true,
  "use_ai": true
}

# 获取榜单状态
GET /api/trending_status
```

### 📡 RSS订阅源管理

#### 添加订阅源
1. 点击"添加订阅源"
2. 输入RSS URL
3. 点击"测试"验证有效性
4. 确认添加

#### 批量管理
- **刷新全部**：更新所有174+订阅源
- **导入OPML**：批量添加订阅源
- **导出OPML**：备份订阅列表

### 查看内容详情
- 📰 条目标题和链接
- 🕒 发布时间和作者信息  
- 🖼️ 富文本内容渲染（HTML、图片、段落）
- 🔍 详细内容弹窗
- 🔗 原文链接跳转

## 📊 技术架构与算法

### 🎯 多维度评分算法
```python
总分 = 时效性评分 × 0.3 + 质量评分 × 0.25 + 热度评分 × 0.25 + 来源权重 × 0.2
```

- **时效性评分**：基于发布时间的新鲜度计算
- **质量评分**：分析标题长度、内容结构、作者信息
- **热度评分**：匹配AI、科技、商业等热门关键词
- **来源权重**：不同RSS源的权威性权重

### 🤖 AI增强流程
1. **内容筛选**：24小时内最新内容
2. **智能评分**：多维度算法排序
3. **自动分类**：基于关键词匹配
4. **AI摘要**：Gemini 1.5 Pro生成150字中文摘要
5. **榜单生成**：综合榜单 + 分类榜单

### 📈 性能指标
- **评分速度**：单条内容 < 1ms
- **榜单生成**：100条内容 < 30秒（无AI摘要）
- **AI摘要**：20条内容约2-3分钟
- **支持规模**：174+RSS源，数千条内容

## 💾 数据与文件

### 核心数据文件
- `feeds_data.json`：RSS订阅源数据和缓存内容
- `trending_output/trending_result.json`：完整榜单结果
- `trending_output/trending_simple.json`：简化榜单（用于前端）
- `.env`：API密钥配置（需手动创建）

### 示例文件
- `static/samples/sample_feeds.opml` - 基础RSS订阅源
- `static/samples/twitter_ai_feeds.opml` - AI专家订阅源

## 🛠️ 技术栈

- **后端框架**：Flask
- **前端框架**：Bootstrap 5 + 现代化UI设计
- **AI服务**：Google Gemini 1.5 Pro
- **HTTP请求**：requests
- **RSS解析**：feedparser
- **日期处理**：python-dateutil
- **环境管理**：python-dotenv
- **数据存储**：JSON文件
- **模板引擎**：Jinja2

## 🔧 故障排除

### Gemini API相关
- 确认`.env`文件中API密钥正确
- 检查API密钥是否有效且有足够额度
- AI摘要功能可关闭，不影响基础榜单生成

### 榜单生成问题
- 确认RSS源中有24小时内的内容
- 检查网络连接，某些RSS源可能需要代理
- 生成时间较长属正常现象（特别是启用AI摘要时）

### 性能问题
- RSS源过多可能导致刷新时间长
- 建议分批处理或使用API参数控制
- 可通过调整评分权重优化结果质量

### 常见错误
- **端口占用**：应用运行在5001端口，避免与其他服务冲突
- **依赖缺失**：确保安装所有`requirements.txt`中的依赖
- **模板错误**：已修复Jinja2字典访问语法问题

## 📁 项目结构

```
tweets/
├── .env                    # API密钥配置 (需创建)
├── .gitignore             # Git忽略规则
├── feeds_data.json        # RSS数据存储
├── trending_output/       # 榜单结果输出目录
│   ├── trending_result.json    # 完整榜单数据
│   └── trending_simple.json    # 简化榜单数据
├── src/                   # 源代码目录
│   ├── app.py            # Flask Web应用主文件
│   ├── feed_manager.py   # RSS订阅管理器
│   ├── content_ranker.py # 内容评分算法
│   ├── gemini_service.py # Gemini AI服务
│   ├── trending_generator.py # 榜单生成核心
│   ├── models.py         # 数据模型定义
│   └── requirements.txt  # Python依赖包
├── templates/            # Jinja2模板文件
│   ├── base.html         # 基础布局模板
│   ├── index.html        # RSS管理主页
│   ├── trending.html     # 热门榜单页面 ⭐
│   ├── trending_category.html # 分类榜单页面
│   ├── feed_detail.html  # RSS源详情页
│   ├── item_detail.html  # 条目详情页
│   ├── add_feed.html     # 添加订阅源
│   └── import_opml.html  # OPML导入页
├── static/               # 静态资源文件
│   ├── css/style.css     # 自定义样式（含榜单UI）
│   ├── js/app.js         # JavaScript交互功能
│   └── samples/          # 示例OPML文件
│       ├── sample_feeds.opml
│       └── twitter_ai_feeds.opml
├── SYSTEM_SUMMARY.md     # 系统功能总结
├── TRENDING_README.md    # 详细技术文档
└── README.md            # 项目说明 (本文件)
```

## 🚀 核心特色

### ⭐ 智能推荐算法
结合时效性、内容质量、热度趋势和来源权威性的多维度评分系统，确保推荐内容的准确性和时效性。

### 🤖 AI驱动摘要
集成Google Gemini 1.5 Pro，自动生成高质量中文摘要，提升阅读效率。

### 🎯 自动内容分类
基于关键词匹配和语义分析，智能将内容分类到AI、科技、商业、产品设计等专业领域。

### 🎨 现代化界面
响应式设计，精美的排行榜展示，支持桌面和移动端访问。

### 📊 实时数据处理
支持174+RSS源的批量处理，能够处理数千条内容的实时分析和排序。

## 📞 技术支持

- **文档**：详见 `SYSTEM_SUMMARY.md` 和 `TRENDING_README.md`
- **问题反馈**：欢迎提交 Issue
- **功能建议**：欢迎提交 Pull Request

## 📄 许可证

本项目采用 MIT 许可证开源。

---

🎉 **立即体验智能RSS推荐系统！**  
访问 `http://127.0.0.1:5001/trending` 开始使用热门榜单功能。