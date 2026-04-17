# Ecommerce Agent - 电商全链路运营Agent

> 基于OpenClaw和AI大模型的电商运营自动化工具，支持选品挖掘、内容创作、数据分析、平台上架等完整链路

## 项目结构

```
ecommerce-agent/
├── frontend/                    # Vue3前端
│   └── src/
│       ├── views/Ecommerce.vue  # 电商运营页面
│       └── services/ecommerce.js  # API服务
├── backend/
│   └── openclaw/               # OpenClaw核心（Node.js）
│       ├── skills/             # 官方Skills
│       ├── docs/               # 官方文档
│       └── scripts/            # 脚本
├── skills/                     # 电商技能包（Python）
│   ├── low_fans_hunter.py      # 低粉爆品挖掘
│   ├── high_fans_tracker.py   # 高粉爆品追踪
│   ├── prohibited_word_checker.py  # 违禁词检测
│   ├── roi_analyzer.py        # ROI分析
│   ├── white_background_generator.py  # 白底图生成
│   ├── ai_title_dehumanizer.py   # 标题去AI化
│   ├── competitor_monitor.py   # 竞品监控
│   ├── amazon_product_selector.py  # 亚马逊选品
│   └── amazon_listing_publisher.py # 亚马逊上架
├── tools/                      # 工具集
├── memory.py                   # 记忆系统
├── scheduler.py                # 定时调度器
├── main.py                    # Python主入口
├── requirements.txt            # Python依赖
├── package.json               # Node.js依赖
└── README.md                 # 本文档
```

## 功能特性

### 电商技能 (9个)

| 分类 | 技能 | 说明 | 状态 |
|------|------|------|------|
| **选品挖掘** | LowFansHunter | 低粉爆品挖掘（四维验证） | ✅ |
| | HighFansTracker | 高粉爆品追踪（类目轮换） | ✅ |
| **内容创作** | AITitleDehumanizer | 标题去AI化 | ✅ |
| **图片处理** | WhiteBackgroundGenerator | 白底图生成 | ✅ |
| **数据分析** | ROIAnalyzer | 广告ROI分析 | ✅ |
| | CompetitorMonitor | 竞品监控 | ✅ |
| **违规检测** | ProhibitedWordChecker | 客服违禁词检测 | ✅ |
| **亚马逊** | AmazonProductSelector | 亚马逊选品 | ✅ |
| | AmazonListingPublisher | 亚马逊自动上架 | ✅ |

### OpenClaw后端功能

| 功能 | 说明 |
|------|------|
| 定时任务 | Cron表达式调度 |
| 浏览器自动化 | Playwright控制 |
| 记忆系统 | 持久化上下文 |
| 消息推送 | 钉钉/飞书等 |
| Skill扩展 | 自定义技能 |

## 安装

### 1. 安装Python依赖
```bash
pip install -r requirements.txt
```

### 2. 安装前端依赖
```bash
cd frontend
npm install
```

### 3. 运行
```bash
# 运行Python技能
python main.py -s low_fans_hunter -p '{"keyword":"收纳"}'

# 运行前端
cd frontend
npm run dev
```

## 使用示例

### Python技能调用
```bash
# 低粉爆品挖掘
python main.py -s low_fans_hunter -p '{"platform":"xiaohongshu","keyword":"收纳"}'

# ROI分析
python main.py -s roi_analyzer -p '{"file_path":"data/ads.xlsx"}'

# 违禁词检测
python main.py -s prohibited_word_checker -p '{"file_path":"data/chat.xlsx"}'
```

### 前端页面
访问 `http://localhost:8080/#/ecommerce` 查看电商运营控制台

## 开发指南

### 创建新技能
在 `skills/` 目录创建新的Python文件，继承 `BaseSkill` 类：

```python
from skills import BaseSkill

class MySkill(BaseSkill):
    def execute(self, **kwargs):
        return {
            "success": True,
            "data": {},
            "message": "完成",
            "notify": False
        }
```

### 添加定时任务
```python
agent.add_schedule_task(
    task_id="daily_check",
    name="每日违禁词检测",
    schedule="0 9 * * *",
    skill_name="prohibited_word_checker"
)
```

## 技术栈

- **后端**: OpenClaw (Node.js) + Python Skills
- **前端**: Vue3 + Element Plus + TailwindCSS
- **数据库**: SQLite (记忆系统)
- **消息**: 钉钉Webhook

## License

MIT License

## GitHub

https://github.com/llixinhao3-source/-ecommerce-agent
