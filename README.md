# Ecommerce Agent - 电商全链路运营Agent

> 基于大模型的电商运营自动化工具，支持选品挖掘、内容创作、数据分析、平台上架等完整链路

## 功能特性

### 已实现的技能 (9个)

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

### 系统特性

| 特性 | 说明 | 状态 |
|------|------|------|
| 记忆系统 | 核心记忆+日级记忆+搜索 | ✅ |
| 定时调度 | Cron表达式+间隔任务 | ✅ |
| 钉钉通知 | 自动推送执行结果 | ✅ |
| 浏览器自动化 | Playwright封装 | ✅ |
| Excel处理 | Pandas封装 | ✅ |

## 安装

```bash
# 克隆项目
git clone https://github.com/llixinhao3-source/ecommerce-agent.git
cd ecommerce-agent

# 安装依赖
pip install -r requirements.txt

# 安装Playwright浏览器
playwright install chromium
```

## 快速开始

### 1. 配置

编辑 `config/settings.json`：

```json
{
  "dingtalk": {
    "webhook": "你的钉钉webhook地址"
  },
  "browser": {
    "cdp_url": "http://127.0.0.1:9222"
  }
}
```

### 2. 运行技能

```bash
# 违禁词检测
python main.py -s prohibited_word_checker -p '{"file_path": "data/chat.xlsx"}'

# ROI分析
python main.py -s roi_analyzer -p '{"file_path": "data/ads.xlsx"}'

# 低粉爆品挖掘
python main.py -s low_fans_hunter -p '{"platform": "xiaohongshu", "keyword": "收纳"}'

# 高粉爆品追踪
python main.py -s high_fans_tracker -p '{"platform": "xiaohongshu"}'

# 标题去AI化
python main.py -s ai_title_dehumanizer -p '{"product": "咖啡杯"}'

# 白底图生成
python main.py -s white_background_generator -p '{"input_path": "images/", "batch": true}'

# 竞品监控
python main.py -s competitor_monitor -p '{"urls": ["url1", "url2"]}'

# 亚马逊选品
python main.py -s amazon_product_selector -p '{"file_path": "data/amazon.xlsx"}'

# 亚马逊上架
python main.py -s amazon_listing_publisher -p '{"file_path": "data/products.xlsx"}'
```

## 项目结构

```
ecommerce-agent/
├── main.py                 # 主入口
├── memory.py               # 记忆系统
├── scheduler.py            # 定时调度器
├── requirements.txt       # 依赖
├── README.md              # 文档
├── config/
│   └── settings.json      # 配置文件
├── skills/                # 技能模块
│   ├── __init__.py
│   ├── low_fans_hunter.py        # 低粉爆品挖掘
│   ├── high_fans_tracker.py       # 高粉爆品追踪
│   ├── prohibited_word_checker.py # 违禁词检测
│   ├── roi_analyzer.py            # ROI分析
│   ├── white_background_generator.py # 白底图生成
│   ├── ai_title_dehumanizer.py   # 标题去AI化
│   ├── competitor_monitor.py     # 竞品监控
│   ├── amazon_product_selector.py  # 亚马逊选品
│   └── amazon_listing_publisher.py # 亚马逊上架
├── tools/                  # 工具集
│   ├── dingtalk.py         # 钉钉推送
│   ├── browser.py          # 浏览器操作
│   ├── excel.py            # Excel处理
│   └── image.py            # 图片处理
├── memory/                  # 记忆存储
└── output/                 # 输出目录
```

## 技能详解

### 1. 低粉爆品挖掘 (LowFansHunter)

**四维验证模型**：
- 粉丝<1000
- 点赞>10
- 评论<50
- 1-2个月内

```python
result = agent.run("low_fans_hunter", 
    platform="xiaohongshu",
    keyword="收纳",
    output="./output/hot.xlsx"
)
```

### 2. 高粉爆品追踪 (HighFansTracker)

**类目轮换表**：
| 周几 | 大类目 | 小类目 |
|------|--------|--------|
| 周一 | 家居日用 | 收纳整理 |
| 周二 | 厨房用品 | 烹饪工具 |
| 周三 | 数码配件 | 充电设备 |
| 周四 | 美妆护肤 | 护肤工具 |
| 周五 | 母婴用品 | 喂养用品 |
| 周六 | 运动户外 | 健身装备 |
| 周日 | 家纺布艺 | 床上用品 |

### 3. 违禁词检测 (ProhibitedWordChecker)

**违禁词分类**：
- 🔴 严重违规：辱骂、攻击、敏感词
- ⚠️ 一般违规：不耐烦、催促、消极

### 4. ROI分析 (ROIAnalyzer)

**评分公式**：
```
总分 = 销量分×0.3 + 利润分×0.25 + 竞争度×0.25 + 评分分×0.2
```

### 5. 标题去AI化 (AITitleDehumanizer)

**去AI化技巧**：
- 避免：Best/Top/Premium
- 加入：actually/for real/no cap
- 口语化：I'm obsessed with...

### 6. 白底图生成 (WhiteBackgroundGenerator)

**标准**：
- 纯白背景 (RGB: 255,255,255)
- 产品占比60-70%
- 分辨率：1024×1024

### 7. 竞品监控 (CompetitorMonitor)

**告警规则**：
- 价格变动>5%
- 库存<20
- 评分下降>0.2
- BSR排名变动>50

### 8. 亚马逊选品 (AmazonProductSelector)

**选品标准**：
- 月销>300单
- 评论<100条
- 利润>30%
- 评分<4.3

### 9. 亚马逊上架 (AmazonListingPublisher)

**上架流程**：
1. 生成标题（去AI化）
2. 生成五点描述
3. 生成搜索关键词
4. 导出Excel上传

## 开发指南

### 创建新技能

```python
from skills import BaseSkill

class MySkill(BaseSkill):
    def __init__(self, agent):
        super().__init__(agent)
    
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
    skill_name="prohibited_word_checker",
    file_path="data/chat.xlsx"
)
agent.start_scheduler()
```

## 定时任务Cron表达式

| 表达式 | 说明 |
|--------|------|
| `0 9 * * *` | 每天9点 |
| `0 */2 * * *` | 每2小时 |
| `0 9,18 * * *` | 每天9点和18点 |

## License

MIT License
