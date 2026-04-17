"""
Skills基类
Base Class for Skills
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime


class BaseSkill(ABC):
    """技能基类"""
    
    def __init__(self, agent):
        self.agent = agent
        self.name = self.__class__.__name__
        self.config = agent.config
        self.memory = agent.memory
    
    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        执行技能
        
        Returns:
            {
                "success": bool,
                "data": Any,
                "message": str,
                "notify": bool  # 是否需要发送通知
            }
        """
        pass
    
    def save_memory(self, key: str, value: Any):
        """保存记忆"""
        self.agent.save_memory(f"{self.name}_{key}", value)
    
    def get_memory(self, key: str) -> Optional[Any]:
        """获取记忆"""
        return self.agent.get_memory(f"{self.name}_{key}")
    
    def log(self, message: str):
        """日志输出"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{self.name}] {message}")
    
    def format_report(self, title: str, data: Dict[str, Any]) -> str:
        """格式化报告"""
        lines = [
            f"# {title}",
            f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "",
        ]
        
        for key, value in data.items():
            if isinstance(value, list):
                lines.append(f"## {key}")
                for item in value:
                    lines.append(f"- {item}")
                lines.append("")
            else:
                lines.append(f"- **{key}**: {value}")
        
        return "\n".join(lines)
