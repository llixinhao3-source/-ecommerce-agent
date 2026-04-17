#!/usr/bin/env python3
"""
电商全链路运营Agent
Ecommerce Full-Chain Operation Agent

支持功能：
- 低粉爆品挖掘
- 高粉爆品追踪
- 违禁词检测
- ROI分析
- 钉钉推送
"""

import argparse
import sys
import json
from datetime import datetime

class EcommerceAgent:
    """电商全链路运营Agent"""
    
    def __init__(self, config_path="config/settings.json"):
        self.config = self.load_config(config_path)
        self.skills = {}
        self.memory = {}
        
    def load_config(self, path):
        """加载配置"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"配置文件 {path} 不存在，使用默认配置")
            return self.default_config()
    
    def default_config(self):
        """默认配置"""
        return {
            "dingtalk": {
                "webhook": "",
                "at_mobiles": []
            },
            "browser": {
                "cdp_port": 9222
            },
            "paths": {
                "output": "./output",
                "memory": "./memory"
            }
        }
    
    def register_skill(self, name, skill):
        """注册技能"""
        self.skills[name] = skill
        print(f"✅ 已注册技能: {name}")
    
    def run_skill(self, name, **kwargs):
        """运行技能"""
        if name not in self.skills:
            print(f"❌ 技能 {name} 不存在")
            return None
        
        skill = self.skills[name]
        print(f"🚀 运行技能: {name}")
        return skill.execute(**kwargs)
    
    def save_memory(self, key, value):
        """保存记忆"""
        self.memory[key] = {
            "value": value,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_memory(self, key):
        """获取记忆"""
        return self.memory.get(key, {}).get("value")
    
    def send_dingtalk(self, message, webhook=None):
        """发送钉钉消息"""
        from tools.dingtalk import DingTalk
        
        webhook = webhook or self.config["dingtalk"]["webhook"]
        dt = DingTalk(webhook)
        return dt.send_text(message)
    
    def run(self, skill_name, **kwargs):
        """运行主逻辑"""
        result = self.run_skill(skill_name, **kwargs)
        
        if result and result.get("notify"):
            self.send_dingtalk(result["message"])
        
        return result


def main():
    parser = argparse.ArgumentParser(description="电商全链路运营Agent")
    parser.add_argument("--skill", "-s", required=True, help="技能名称")
    parser.add_argument("--params", "-p", default="{}", help="技能参数(JSON格式)")
    parser.add_argument("--config", "-c", default="config/settings.json", help="配置文件")
    parser.add_argument("--notify", "-n", action="store_true", help="完成后发送钉钉通知")
    
    args = parser.parse_args()
    
    # 解析参数
    try:
        params = json.loads(args.params)
    except json.JSONDecodeError:
        print("❌ 参数格式错误，请使用JSON格式")
        sys.exit(1)
    
    # 初始化Agent
    agent = EcommerceAgent(args.config)
    
    # 注册技能
    from skills.low_fans_hunter import LowFansHunter
    from skills.prohibited_word_checker import ProhibitedWordChecker
    from skills.roi_analyzer import ROIAnalyzer
    
    agent.register_skill("low_fans_hunter", LowFansHunter(agent))
    agent.register_skill("prohibited_word_checker", ProhibitedWordChecker(agent))
    agent.register_skill("roi_analyzer", ROIAnalyzer(agent))
    
    # 运行技能
    result = agent.run(args.skill, **params)
    
    if result:
        print(f"✅ 技能执行成功: {args.skill}")
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"❌ 技能执行失败: {args.skill}")
        sys.exit(1)


if __name__ == "__main__":
    main()
