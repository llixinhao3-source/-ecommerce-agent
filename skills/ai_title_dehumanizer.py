"""
标题去AI化技能
AI Title Dehumanizer

将AI生成的标题转化为native speaker的自然表达

去AI化技巧：
- 避免 Best/Top/Premium
- 加入情感词
- 口语化表达
- 悬念感营造
"""

import re
from typing import Dict, Any, List, Tuple
from . import BaseSkill


class AITitleDehumanizer(BaseSkill):
    """标题去AI化"""
    
    # AI痕迹词
    AI_PATTERNS = {
        "best": ["best", "top", "premier", "ultimate"],
        "premium": ["premium", "luxury", "high-end", "professional"],
        "intro": ["introducing", "presenting", "announcing"],
        "exclaim": ["!!!", "！！", "!!!"],
        "keyword_stack": []  # 关键词堆砌
    }
    
    # 去AI化替换表
    REPLACEMENTS = {
        "best": {
            "pattern": r"\bThe Best\b|\bBest\b|\bTop\b",
            "replacement": {
                "casual": "that actually works",
                "enthusiastic": "I'm obsessed with",
                "curious": "you didn't know you needed"
            }
        },
        "premium": {
            "pattern": r"\bPremium\b|\bLuxury\b|\bHigh-End\b",
            "replacement": {
                "casual": "feels way more expensive than it is",
                "honest": "solid quality",
                "curious": "surprisingly good"
            }
        }
    }
    
    # 情感词
    EMOTION_WORDS = [
        "actually", "honestly", "for real", "no cap",
        "obsessed", "shook", "wild", "crazy",
        "lifesaver", "game changer", "rip", "hits different"
    ]
    
    # 悬念营造词
    SUSPENSE_WORDS = [
        "until", "but", "however", "actually",
        "storytime", "spill", "tea", "plot twist"
    ]
    
    def __init__(self, agent):
        super().__init__(agent)
    
    def detect_ai_patterns(self, title: str) -> List[Dict[str, Any]]:
        """
        检测AI痕迹
        
        Args:
            title: 标题
        
        Returns:
            检测到的AI痕迹列表
        """
        findings = []
        title_lower = title.lower()
        
        # 检查 Best/Top
        for word in self.AI_PATTERNS["best"]:
            if word in title_lower:
                findings.append({
                    "type": "best",
                    "word": word,
                    "position": title_lower.find(word)
                })
        
        # 检查 Premium
        for word in self.AI_PATTERNS["premium"]:
            if word in title_lower:
                findings.append({
                    "type": "premium",
                    "word": word,
                    "position": title_lower.find(word)
                })
        
        # 检查过多感叹号
        exclaim_count = title.count("!") + title.count("！")
        if exclaim_count > 1:
            findings.append({
                "type": "exclaim",
                "word": "!!!",
                "count": exclaim_count
            })
        
        return findings
    
    def dehumanize(self, title: str, style: str = "casual") -> str:
        """
        去AI化标题
        
        Args:
            title: 原始标题
            style: 风格 (casual/enthusiastic/curious/honest)
        
        Returns:
            去AI化后的标题
        """
        result = title
        
        # 替换 Best/Top
        result = re.sub(
            r"\bThe Best\b|\bBest(?!\s+selling)\b|\bTop(?!\s+10)\b",
            self.REPLACEMENTS["best"]["replacement"].get(style, "actually good"),
            result,
            flags=re.IGNORECASE
        )
        
        # 替换 Premium
        result = re.sub(
            r"\bPremium\b|\bLuxury\b|\bHigh-End\b",
            self.REPLACEMENTS["premium"]["replacement"].get(style, "solid"),
            result,
            flags=re.IGNORECASE
        )
        
        # 移除过多感叹号
        result = re.sub(r"!{2,}", "!", result)
        result = re.sub(r"！{2,}", "！", result)
        
        return result
    
    def add_emotion(self, title: str) -> str:
        """
        添加情感词
        
        Args:
            title: 标题
        
        Returns:
            添加情感词后的标题
        """
        import random
        
        emotion = random.choice(self.EMOTION_WORDS)
        
        # 随机插入位置
        if random.random() > 0.5:
            return f"{title}, {emotion}"
        else:
            return f"{emotion} - {title}"
    
    def add_suspense(self, title: str) -> str:
        """
        添加悬念
        
        Args:
            title: 标题
        
        Returns:
            添加悬念后的标题
        """
        import random
        
        if "but" in title.lower() or "until" in title.lower():
            return title
        
        suspense = random.choice(self.SUSPENSE_WORDS)
        
        if suspense == "until":
            return title.replace(" - ", " until I ")  # 简化处理
        elif suspense == "but":
            return title + " but wait..."
        elif suspense == "actually":
            return f"I thought {title.lower().split()[0]} was basic, {title.split()[0]} actually..."
        else:
            return title
    
    def process_batch(self, titles: List[str], style: str = "casual") -> List[Dict[str, Any]]:
        """
        批量处理标题
        
        Args:
            titles: 标题列表
            style: 风格
        
        Returns:
            处理结果
        """
        results = []
        
        for original in titles:
            # 检测AI痕迹
            patterns = self.detect_ai_patterns(original)
            
            # 去AI化
            dehumanized = self.dehumanize(original, style)
            
            # 添加情感（可选）
            if patterns:
                dehumanized = self.add_emotion(dehumanized)
            
            # 添加悬念（可选）
            if patterns and len(patterns) > 1:
                dehumanized = self.add_suspense(dehumanized)
            
            results.append({
                "original": original,
                "dehumanized": dehumanized,
                "patterns_found": len(patterns),
                "patterns": patterns
            })
        
        return results
    
    def generate_title(self, product: str, style: str = "casual") -> str:
        """
        根据产品生成自然标题
        
        Args:
            product: 产品名称
            style: 风格
        
        Returns:
            生成的标题
        """
        import random
        
        templates = {
            "casual": [
                f"Using {product} for a week - honest review",
                f"Why {product} is actually worth it",
                f"{product} review after 30 days of use",
            ],
            "curious": [
                f"Everyone talks about {product}, but...",
                f"Is {product} actually good?",
                f"The truth about {product}",
            ],
            "enthusiastic": [
                f"{product} is a game changer!",
                f"I can't stop using {product}",
                f"Obsessed with this {product}!",
            ]
        }
        
        return random.choice(templates.get(style, templates["casual"]))
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        执行技能
        
        Args:
            titles: 标题列表（JSON字符串或列表）
            product: 产品名称（用于生成标题）
            style: 风格 (casual/curious/enthusiastic/honest)
            batch: 是否批量处理
        
        Returns:
            执行结果
        """
        import json
        
        titles_str = kwargs.get("titles", "[]")
        product = kwargs.get("product", "")
        style = kwargs.get("style", "casual")
        batch = kwargs.get("batch", False)
        
        self.log(f"开始去AI化标题, style={style}")
        
        try:
            # 解析标题
            if isinstance(titles_str, str):
                titles = json.loads(titles_str)
            else:
                titles = titles_str
            
            if product:
                # 生成标题
                generated = self.generate_title(product, style)
                
                return {
                    "success": True,
                    "data": {
                        "generated": generated,
                        "style": style
                    },
                    "message": f"生成标题: {generated}",
                    "notify": False
                }
            elif titles:
                # 批量处理
                results = self.process_batch(titles, style)
                
                return {
                    "success": True,
                    "data": {
                        "total": len(results),
                        "processed": len([r for r in results if r["patterns_found"] > 0]),
                        "results": results
                    },
                    "message": f"处理完成: {len(results)} 个标题",
                    "notify": False
                }
            else:
                return {
                    "success": False,
                    "data": {},
                    "message": "请提供titles或product参数",
                    "notify": False
                }
                
        except Exception as e:
            self.log(f"执行失败: {e}")
            return {
                "success": False,
                "data": {},
                "message": f"执行失败: {e}",
                "notify": False
            }
