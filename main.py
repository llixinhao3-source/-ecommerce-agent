#!/usr/bin/env python3
"""
电商全链路运营Agent
Ecommerce Full-Chain Operation Agent

支持功能：
- 低粉爆品挖掘
- 高粉爆品追踪
- 违禁词检测
- ROI分析
- 定时任务调度
- 记忆系统
"""

import argparse
import sys
import json
from datetime import datetime

class EcommerceAgent:
    """电商全链路运营Agent"""
    
    def __init__(self, config_path: str = "config/settings.json"):
        self.config = self.load_config(config_path)
        self.skills = {}
        self.scheduler = None
        self.memory = None
        self.init_memory()
        
    def load_config(self, path: str) -> dict:
        """加载配置"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"配置文件 {path} 不存在，使用默认配置")
            return self.default_config()
    
    def default_config(self) -> dict:
        """默认配置"""
        return {
            "dingtalk": {
                "webhook": "",
                "at_mobiles": []
            },
            "browser": {
                "cdp_url": "http://127.0.0.1:9222"
            },
            "paths": {
                "output": "./output",
                "memory": "./memory"
            }
        }
    
    def init_memory(self):
        """初始化记忆系统"""
        from memory import create_user_memory
        memory_dir = self.config.get("paths", {}).get("memory", "./memory")
        self.memory = create_user_memory(memory_dir)
    
    def init_scheduler(self):
        """初始化调度器"""
        from scheduler import Scheduler
        state_file = f"{self.config.get('paths', {}).get('memory', './memory')}/scheduler_state.json"
        self.scheduler = Scheduler(state_file)
    
    def register_skill(self, name: str, skill) -> None:
        """注册技能"""
        self.skills[name] = skill
        print(f"✅ 已注册技能: {name}")
    
    def run_skill(self, name: str, **kwargs) -> dict:
        """运行技能"""
        if name not in self.skills:
            print(f"❌ 技能 {name} 不存在")
            return {"success": False, "message": f"技能 {name} 不存在"}
        
        skill = self.skills[name]
        print(f"🚀 运行技能: {name}")
        
        try:
            result = skill.execute(**kwargs)
            
            # 记录到记忆
            if self.memory:
                self.memory.add_task_record(name, result)
            
            return result
        except Exception as e:
            print(f"❌ 技能执行失败: {e}")
            return {"success": False, "message": str(e)}
    
    def send_dingtalk(self, message: str, webhook: str = None) -> dict:
        """发送钉钉消息"""
        from tools.dingtalk import DingTalk
        
        webhook = webhook or self.config["dingtalk"]["webhook"]
        if not webhook:
            return {"success": False, "message": "未配置钉钉webhook"}
        
        dt = DingTalk(webhook)
        return dt.send_text(message)
    
    def send_markdown(self, title: str, content: str, webhook: str = None) -> dict:
        """发送Markdown消息"""
        from tools.dingtalk import DingTalk
        
        webhook = webhook or self.config["dingtalk"]["webhook"]
        if not webhook:
            return {"success": False, "message": "未配置钉钉webhook"}
        
        dt = DingTalk(webhook)
        return dt.send_markdown(title, content)
    
    def search_memory(self, keyword: str) -> list:
        """搜索记忆"""
        if not self.memory:
            return []
        return self.memory.search(keyword)
    
    def run(self, skill_name: str, **kwargs) -> dict:
        """运行主逻辑"""
        result = self.run_skill(skill_name, **kwargs)
        
        # 自动发送钉钉通知
        if result and result.get("notify"):
            message = result.get("message", "") + "\n\n" + json.dumps(result.get("data", {}), ensure_ascii=False, indent=2)
            self.send_dingtalk(message)
        
        return result
    
    def add_schedule_task(self, task_id: str, name: str, schedule: str, skill_name: str, **kwargs) -> None:
        """添加定时任务"""
        if not self.scheduler:
            self.init_scheduler()
        
        def task_wrapper():
            self.run_skill(skill_name, **kwargs)
        
        self.scheduler.add_task(task_id, name, schedule, task_wrapper)
        print(f"✅ 已添加定时任务: {name} ({schedule})")
    
    def start_scheduler(self) -> None:
        """启动调度器"""
        if not self.scheduler:
            self.init_scheduler()
        self.scheduler.start()
    
    def stop_scheduler(self) -> None:
        """停止调度器"""
        if self.scheduler:
            self.scheduler.stop()


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
    from skills.high_fans_tracker import HighFansTracker
    from skills.prohibited_word_checker import ProhibitedWordChecker
    from skills.roi_analyzer import ROIAnalyzer
    
    agent.register_skill("low_fans_hunter", LowFansHunter(agent))
    agent.register_skill("high_fans_tracker", HighFansTracker(agent))
    agent.register_skill("prohibited_word_checker", ProhibitedWordChecker(agent))
    agent.register_skill("roi_analyzer", ROIAnalyzer(agent))
    
    # 运行技能
    result = agent.run(args.skill, **params)
    
    if result and result.get("success"):
        print(f"✅ 技能执行成功: {args.skill}")
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"❌ 技能执行失败: {args.skill}")
        print(json.dumps(result, ensure_ascii=False, indent=2) if result else "")
        sys.exit(1)


if __name__ == "__main__":
    main()
