"""
记忆系统
Memory System

支持：
- 核心记忆（持久化）
- 日级记忆（按天存储）
- 关键词检索
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional


class Memory:
    """记忆系统"""
    
    def __init__(self, memory_dir: str = "./memory"):
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        
        # 记忆文件
        self.core_file = self.memory_dir / "core.json"
        self.daily_file = self.memory_dir / f"daily_{datetime.now().strftime('%Y%m%d')}.json"
        
        # 加载记忆
        self.core = self.load_json(self.core_file, {})
        self.daily = self.load_json(self.daily_file, {})
    
    def load_json(self, file_path: Path, default=None) -> Dict:
        """加载JSON文件"""
        try:
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"加载记忆失败: {e}")
        return default or {}
    
    def save_json(self, file_path: Path, data: Dict):
        """保存JSON文件"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存记忆失败: {e}")
    
    def save(self):
        """保存所有记忆"""
        self.save_json(self.core_file, self.core)
        self.save_json(self.daily_file, self.daily)
    
    # ========== 核心记忆 ==========
    
    def set_core(self, key: str, value: Any):
        """设置核心记忆"""
        self.core[key] = {
            "value": value,
            "updated_at": datetime.now().isoformat()
        }
        self.save()
    
    def get_core(self, key: str, default: Any = None) -> Any:
        """获取核心记忆"""
        data = self.core.get(key, {})
        return data.get("value", default)
    
    def delete_core(self, key: str):
        """删除核心记忆"""
        if key in self.core:
            del self.core[key]
            self.save()
    
    # ========== 日级记忆 ==========
    
    def add_daily(self, key: str, value: Any):
        """添加日级记忆"""
        if key not in self.daily:
            self.daily[key] = []
        
        self.daily[key].append({
            "value": value,
            "timestamp": datetime.now().isoformat()
        })
        self.save()
    
    def get_daily(self, key: str, limit: int = 10) -> List:
        """获取日级记忆"""
        records = self.daily.get(key, [])
        return records[-limit:]
    
    # ========== 通用操作 ==========
    
    def set(self, key: str, value: Any, memory_type: str = "core"):
        """通用设置"""
        if memory_type == "core":
            self.set_core(key, value)
        else:
            self.add_daily(key, value)
    
    def get(self, key: str, memory_type: str = "core", default: Any = None) -> Any:
        """通用获取"""
        if memory_type == "core":
            return self.get_core(key, default)
        else:
            records = self.get_daily(key)
            return [r["value"] for r in records] if records else default
    
    def search(self, keyword: str) -> List[Dict[str, Any]]:
        """搜索记忆"""
        results = []
        
        # 搜索核心记忆
        for key, data in self.core.items():
            value_str = str(data.get("value", ""))
            if keyword.lower() in value_str.lower() or keyword.lower() in key.lower():
                results.append({
                    "type": "core",
                    "key": key,
                    "value": data.get("value"),
                    "updated_at": data.get("updated_at")
                })
        
        # 搜索日级记忆
        for key, records in self.daily.items():
            if keyword.lower() in key.lower():
                for record in records:
                    results.append({
                        "type": "daily",
                        "key": key,
                        "value": record.get("value"),
                        "timestamp": record.get("timestamp")
                    })
        
        return results
    
    def get_recent(self, limit: int = 20) -> List[Dict[str, Any]]:
        """获取最近的记忆"""
        results = []
        
        # 核心记忆
        for key, data in self.core.items():
            results.append({
                "type": "core",
                "key": key,
                "value": data.get("value"),
                "updated_at": data.get("updated_at")
            })
        
        # 日级记忆
        for key, records in self.daily.items():
            for record in records[-3:]:  # 每个key最多3条
                results.append({
                    "type": "daily",
                    "key": key,
                    "value": record.get("value"),
                    "timestamp": record.get("timestamp")
                })
        
        # 按时间排序
        results.sort(key=lambda x: x.get("updated_at") or x.get("timestamp", ""), reverse=True)
        
        return results[:limit]
    
    def clear_old_daily(self, days: int = 7):
        """清理旧的日级记忆"""
        # 只保留最近N天的记忆
        # 这里简化处理，实际应该检查文件日期
        self.daily = {}
        self.save()


class UserMemory(Memory):
    """用户记忆 - 继承Memory并扩展用户相关功能"""
    
    def __init__(self, memory_dir: str = "./memory"):
        super().__init__(memory_dir)
        
        # 初始化用户配置
        if not self.get_core("user_preferences"):
            self.set_core("user_preferences", {
                "dingtalk_webhook": "",
                "platforms": [],
                "notify_enabled": True
            })
    
    def update_preference(self, key: str, value: Any):
        """更新用户偏好"""
        prefs = self.get_core("user_preferences", {})
        prefs[key] = value
        self.set_core("user_preferences", prefs)
    
    def get_preference(self, key: str, default: Any = None) -> Any:
        """获取用户偏好"""
        prefs = self.get_core("user_preferences", {})
        return prefs.get(key, default)
    
    def add_task_record(self, task_name: str, result: Dict[str, Any]):
        """添加任务执行记录"""
        self.add_daily("task_records", {
            "task": task_name,
            "result": result,
            "timestamp": datetime.now().isoformat()
        })
    
    def get_task_history(self, task_name: str = None, limit: int = 10) -> List[Dict]:
        """获取任务历史"""
        records = self.get_daily("task_records", limit * 2)
        
        if task_name:
            records = [r for r in records if r.get("value", {}).get("task") == task_name]
        
        return [{"task": r["value"]["task"], "result": r["value"]["result"], "timestamp": r["timestamp"]} for r in records[-limit:]]


# 便捷函数
def create_memory(memory_dir: str = "./memory") -> Memory:
    """创建记忆实例"""
    return Memory(memory_dir)

def create_user_memory(memory_dir: str = "./memory") -> UserMemory:
    """创建用户记忆实例"""
    return UserMemory(memory_dir)
