"""
违禁词检测技能
Prohibited Word Checker

检测客服聊天中的违禁词

严重违规：辱骂、人身攻击、敏感词
一般违规：不耐烦、催促、消极
"""

import re
from typing import Dict, Any, List, Tuple
from pathlib import Path
import pandas as pd
from datetime import datetime

from . import BaseSkill
from tools.excel import ExcelTool


class ProhibitedWordChecker(BaseSkill):
    """违禁词检测"""
    
    # 严重违规词
    SERIOUS_WORDS = [
        # 辱骂攻击
        "傻逼", "sb", "傻b", "傻叉", "傻猪", "狗东西", "不要脸", "臭不要脸",
        "滚", "滚蛋", "gun", "他妈的", "他妈", "妈死了",
        # 威胁
        "报警", "投诉", "举报", "找平台",
        # 推诿
        "我不管", "随便你", "不关我的事", "去找平台", "随便评价",
        "没有售后服务", "不卖", "穷酸", "穷鬼", "没钱别问",
        # 敏感词
        "微信", "京东", "小红书", "抖音", "快手",
        # 其他
        "骗人", "诈骗", "骗子"
    ]
    
    # 一般违规词
    GENERAL_WORDS = [
        "无语", "服了", "我真服了", "这都不行", "还想怎样",
        "呵呵", "你看不懂吗", "懂？", "ok？", "那没办法了",
        "给钱", "付款啊", "快点", "赶紧"
    ]
    
    def __init__(self, agent):
        super().__init__(agent)
        self.violations: List[Dict] = []
    
    def check_text(self, text: str) -> Dict[str, Any]:
        """
        检查文本违禁词
        
        Args:
            text: 待检查文本
        
        Returns:
            {
                "has_violation": bool,
                "level": "serious/general/none",
                "words": [(word, level)],
                "count": int
            }
        """
        text_lower = text.lower()
        found = []
        
        # 检查严重违规
        for word in self.SERIOUS_WORDS:
            if word.lower() in text_lower:
                found.append((word, "serious"))
        
        # 检查一般违规
        for word in self.GENERAL_WORDS:
            if word.lower() in text_lower:
                found.append((word, "general"))
        
        # 确定级别
        levels = [item[1] for item in found]
        if "serious" in levels:
            level = "serious"
        elif "general" in levels:
            level = "general"
        else:
            level = "none"
        
        return {
            "has_violation": len(found) > 0,
            "level": level,
            "words": found,
            "count": len(found)
        }
    
    def check_chat(self, chat_data: List[Dict]) -> List[Dict]:
        """
        检查聊天记录
        
        Args:
            chat_data: [{"seller": str, "customer": str, "messages": [str]}]
        
        Returns:
            违规记录列表
        """
        violations = []
        
        for chat in chat_data:
            seller = chat.get("seller", "")
            customer = chat.get("customer", "")
            messages = chat.get("messages", [])
            
            for i, msg in enumerate(messages):
                result = self.check_text(msg)
                
                if result["has_violation"]:
                    violations.append({
                        "seller": seller,
                        "customer": customer,
                        "message": msg,
                        "level": result["level"],
                        "words": ",".join([w[0] for w in result["words"]]),
                        "message_index": i,
                        "timestamp": datetime.now().isoformat()
                    })
        
        self.violations = violations
        return violations
    
    def check_excel(self, file_path: str, text_column: str = "聊天内容") -> List[Dict]:
        """
        检查Excel文件中的聊天记录
        
        Args:
            file_path: Excel文件路径
            text_column: 文本列名
        
        Returns:
            违规记录列表
        """
        excel = ExcelTool(file_path)
        df = excel.read()
        
        if text_column not in df.columns:
            # 尝试查找包含"聊天"、"内容"的列
            for col in df.columns:
                if "聊天" in col or "内容" in col or "content" in col.lower():
                    text_column = col
                    break
        
        violations = []
        
        for idx, row in df.iterrows():
            text = str(row.get(text_column, ""))
            result = self.check_text(text)
            
            if result["has_violation"]:
                violations.append({
                    "row_index": idx,
                    "text": text,
                    "level": result["level"],
                    "words": ",".join([w[0] for w in result["words"]])
                })
        
        self.violations = violations
        return violations
    
    def generate_report(self) -> str:
        """生成违禁词检测报告"""
        if not self.violations:
            return "✅ 本次检测未发现违禁词"
        
        # 统计
        serious_count = sum(1 for v in self.violations if v["level"] == "serious")
        general_count = sum(1 for v in self.violations if v["level"] == "general")
        
        lines = [
            "# 客服聊天违禁词检测报告",
            f"**检测时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            f"**违规总数**: {len(self.violations)}",
            "",
            f"🔴 严重违规: {serious_count} 条",
            f"⚠️ 一般违规: {general_count} 条",
            "",
            "## 违规详情",
            ""
        ]
        
        for i, v in enumerate(self.violations, 1):
            level_icon = "🔴" if v["level"] == "serious" else "⚠️"
            lines.append(f"{level_icon} {i}. [{v.get('seller', '未知')}] - {v.get('customer', '未知')}")
            lines.append(f"   内容: {v.get('text', '')[:50]}...")
            lines.append(f"   违禁词: {v.get('words', '')}")
            lines.append("")
        
        return "\n".join(lines)
    
    def save_report(self, output_path: str):
        """保存报告到Excel"""
        if not self.violations:
            self.log("没有违规记录需要保存")
            return
        
        df = pd.DataFrame(self.violations)
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        df.to_excel(output_path, index=False)
        
        self.log(f"报告已保存: {output_path}")
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        执行违禁词检测
        
        Args:
            file_path: Excel文件路径
            text_column: 文本列名
            output: 输出报告路径
            generate_report: 是否生成报告
        
        Returns:
            执行结果
        """
        file_path = kwargs.get("file_path", "")
        text_column = kwargs.get("text_column", "聊天内容")
        output = kwargs.get("output", "./output/violation_report.xlsx")
        generate_report = kwargs.get("generate_report", False)
        
        self.log(f"开始检测违禁词: {file_path}")
        
        try:
            # 检查Excel
            violations = self.check_excel(file_path, text_column)
            
            # 保存报告
            if violations:
                self.save_report(output)
            
            # 生成报告内容
            report = self.generate_report() if generate_report else ""
            
            # 统计
            serious = sum(1 for v in violations if v["level"] == "serious")
            general = sum(1 for v in violations if v["level"] == "general")
            
            return {
                "success": True,
                "data": {
                    "total": len(violations),
                    "serious": serious,
                    "general": general,
                    "output": output
                },
                "message": f"检测完成: 共{len(violations)}条违规(严重{serious}条, 一般{general}条)",
                "report": report,
                "notify": serious > 0  # 严重违规时通知
            }
            
        except Exception as e:
            self.log(f"检测失败: {e}")
            return {
                "success": False,
                "data": {},
                "message": f"检测失败: {e}",
                "notify": False
            }
