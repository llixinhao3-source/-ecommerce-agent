# Ecommerce Agent - 电商全链路运营Agent

> 基于大模型的电商运营自动化工具，支持选品挖掘、违禁词检测、ROI分析等功能

## 功能特性

### 已实现的功能

| 技能 | 说明 | 状态 |
|------|------|------|
| 低粉爆品挖掘 | 从小红书/抖音挖掘粉丝少但销量高的潜力爆品 | ✅ |
| 违禁词检测 | 检测客服聊天中的违禁词 | ✅ |
| ROI分析 | 计算广告投放回报，指导投流决策 | ✅ |

### 计划开发

| 技能 | 说明 | 状态 |
|------|------|------|
| 高粉爆品追踪 | 追踪已验证的爆品模式 | 🔜 |
| 竞品监控 | 实时监控竞品价格、库存变动 | 🔜 |
| 白底图生成 | AI生成白底图 | 🔜 |
| 场景图制作 | 影视化场景图生成 | 🔜 |
| 标题去AI化 | 将AI生成的标题转成native表达 | 🔜 |

## 安装

```bash
# 克隆项目
git clone https://github.com/llixinhao3-source/dianshang_promote.git
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
python main.py -s prohibited_word_checker -p '{"file_path": "data/chat.xlsx", "output": "output/report.xlsx"}'

# ROI分析
python main.py -s roi_analyzer -p '{"file_path": "data/ads.xlsx", "output": "output/roi.xlsx"}'

# 低粉爆品挖掘
python main.py -s low_fans_hunter -p '{"platform": "xiaohongshu", "keyword": "收纳", "output": "output/hot.xlsx"}'
```

## 项目结构

```
ecommerce-agent/
├── main.py                 # 主入口
├── requirements.txt         # 依赖
├── config/
│   └── settings.json       # 配置文件
├── skills/
│   ├── __init__.py         # Skill基类
│   ├── low_fans_hunter.py  # 低粉爆品挖掘
│   ├── prohibited_word_checker.py  # 违禁词检测
│   └── roi_analyzer.py     # ROI分析
├── tools/
│   ├── dingtalk.py        # 钉钉推送
│   ├── browser.py          # 浏览器操作
│   └── excel.py           # Excel处理
├── memory/                  # 记忆存储
├── output/                 # 输出目录
└── docs/                   # 文档
```

## 使用示例

### Python调用

```python
from main import EcommerceAgent
from skills.prohibited_word_checker import ProhibitedWordChecker

# 初始化
agent = EcommerceAgent()

# 注册技能
checker = ProhibitedWordChecker(agent)
agent.register_skill("checker", checker)

# 运行
result = agent.run("checker", 
    file_path="data/chat.xlsx",
    output="output/report.xlsx"
)

print(result)
```

### 违禁词检测

```python
# 检查Excel文件
checker = ProhibitedWordChecker(agent)
violations = checker.check_excel("data/chat.xlsx", "聊天内容")

# 生成报告
report = checker.generate_report()
print(report)
```

### ROI分析

```python
# 加载数据并分析
analyzer = ROIAnalyzer(agent)
analyzer.load_data("data/ads.xlsx")
results = analyzer.analyze()

# 生成报告
report = analyzer.generate_report()
print(report)
```

## 配置说明

### 钉钉配置

```json
{
  "dingtalk": {
    "webhook": "https://oapi.dingtalk.com/robot/send?access_token=xxx",
    "at_mobiles": ["138xxxx"]
  }
}
```

### 浏览器配置

```json
{
  "browser": {
    "cdp_url": "http://127.0.0.1:9222",
    "headless": false
  }
}
```

### 技能配置

```json
{
  "skills": {
    "low_fans_hunter": {
      "max_fans": 1000,
      "min_likes": 10,
      "max_days": 60
    }
  }
}
```

## 开发指南

### 创建新技能

```python
from skills import BaseSkill

class MySkill(BaseSkill):
    def __init__(self, agent):
        super().__init__(agent)
    
    def execute(self, **kwargs):
        # 你的逻辑
        return {
            "success": True,
            "data": {},
            "message": "完成",
            "notify": False
        }
```

### 添加新工具

在 `tools/` 目录下创建新工具文件：

```python
# tools/my_tool.py
class MyTool:
    def __init__(self):
        pass
    
    def do_something(self):
        pass
```

## License

MIT License

## 贡献

欢迎提交Issue和PR！
