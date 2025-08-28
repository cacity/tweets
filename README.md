# Twitter RSS订阅管理器

一个用于管理和查看Twitter RSS订阅源的Flask Web应用程序。

## 功能特性

- 📡 **RSS订阅源管理**：添加、编辑、删除RSS订阅源
- 🔄 **自动刷新**：定时或手动刷新订阅内容
- 📰 **增强内容展示**：美观地显示RSS条目，包括标题、作者、时间、摘要
  - ✨ **HTML内容渲染**：支持富文本格式、图片显示、段落格式
  - 🖼️ **图片支持**：自动加载和显示内嵌图片
  - 📖 **展开/收缩**：可切换内容显示模式
  - 🔍 **详细内容**：可打开单独窗口查看完整内容
- 📁 **OPML支持**：导入和导出OPML格式的订阅源文件
- 🌐 **链接跳转**：点击条目可直接跳转到原文链接
- 💾 **数据持久化**：本地保存订阅源数据和内容
- 🎨 **现代化Web界面**：基于Bootstrap 5的响应式设计，支持桌面和移动设备

## 安装要求

- Python 3.7+
- Flask
- requests
- feedparser
- python-dateutil

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

或者手动安装：

```bash
pip install Flask requests feedparser python-dateutil
```

### 2. 运行程序

```bash
python app.py
```

然后在浏览器中访问 `http://127.0.0.1:5000`

## 使用说明

### 添加RSS订阅源

1. 点击左侧面板的"添加订阅源"按钮
2. 输入RSS订阅源的URL
3. 可选：输入自定义标题和描述
4. 点击"测试"按钮验证RSS源的有效性
5. 点击"确定"完成添加

### 管理订阅源

- **查看内容**：点击左侧列表中的订阅源，右侧面板会显示该源的所有条目
- **刷新**：选中订阅源后点击"刷新选中"，或点击"刷新全部"更新所有订阅源
- **编辑**：选中订阅源后点击"编辑订阅源"修改标题和描述
- **删除**：选中订阅源后点击"删除订阅源"移除该订阅源

### 导入/导出OPML

- **导入**：菜单栏选择"文件" > "导入OPML"，选择OPML文件批量添加订阅源
- **导出**：菜单栏选择"文件" > "导出OPML"，将当前所有订阅源导出为OPML文件

### 查看内容

右侧面板会显示选中订阅源的所有条目，包括：
- 📰 **条目标题**：显示清晰的标题信息
- 🕒 **发布时间和作者信息**：带有图标的时间和作者显示
- 🖼️ **富文本内容**：支持HTML格式、图片、段落等内容渲染
- 📖 **展开/收缩按钮**：可切换内容显示模式
- 🔍 **"详细内容"按钮**：打开单独窗口查看完整内容
- 🔗 **"查看原文"按钮**：点击跳转到原始链接

#### 内容渲染特性
- ✨ **HTML解析**：支持段落、标题、列表、链接等格式
- 🖼️ **图片显示**：自动加载并显示内嵌图片
- 📝 **引用块**：特殊样式显示引用内容
- 💻 **代码高亮**：代码块的特殊显示效果

## 示例RSS订阅源

由于Twitter官方已不再提供RSS支持，本应用支持使用第三方服务：

### xgo.ing API服务
项目中包含的`twitter_ai_feeds.opml`文件包含了众多AI领域专家的Twitter RSS订阅源：
- OpenAI、Anthropic等AI公司
- Sam Altman、Andrej Karpathy等AI专家  
- Google AI、Hugging Face等研究机构

### 其他RSS服务
```
- Nitter实例：https://nitter.net/用户名/rss
- RSS Bridge：通过RSS Bridge转换
- 其他Twitter RSS代理服务
```

### OPML文件
项目包含以下OPML示例文件：
- `sample_feeds.opml` - 基本示例订阅源
- `twitter_ai_feeds.opml` - AI专家Twitter订阅源

## 配置文件

应用程序会在运行目录下创建以下文件：

- `feeds_data.json`：存储所有订阅源数据和缓存的内容

## 故障排除

### 无法添加订阅源
- 检查URL是否正确
- 确认网络连接正常
- 验证RSS源是否有效（可在浏览器中打开测试）

### 刷新失败
- 检查网络连接
- RSS源可能暂时不可用，稍后再试
- 某些RSS源可能需要特殊的请求头或认证

### 程序启动失败
- 确认已安装所有必需的依赖库
- 检查Python版本是否符合要求
- 查看错误信息中的详细说明

## 技术架构

- **Web框架**：Flask
- **前端框架**：Bootstrap 5
- **HTTP请求**：requests
- **RSS解析**：feedparser  
- **日期处理**：python-dateutil
- **数据存储**：JSON文件
- **模板引擎**：Jinja2

## 项目结构

```
tweets/
├── app.py              # Flask应用主文件
├── feed_manager.py      # RSS订阅管理器
├── models.py            # 数据模型
├── templates/           # HTML模板
│   ├── base.html        # 基础模板
│   ├── index.html       # 主页
│   ├── feed_detail.html # 订阅源详情
│   ├── item_detail.html # 条目详情
│   ├── add_feed.html    # 添加订阅源
│   └── import_opml.html # 导入OPML
├── static/              # 静态文件
│   ├── css/style.css    # 自定义样式
│   ├── js/app.js        # JavaScript功能
│   └── samples/         # 示例OPML文件
├── requirements.txt     # 依赖列表
└── README.md           # 说明文档
```

## 许可证

本项目采用MIT许可证。

## 贡献

欢迎提交Issue和Pull Request来改进这个项目！