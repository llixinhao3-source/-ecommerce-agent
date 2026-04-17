"""
低粉爆品挖掘技能
Low-Fans Hot Product Hunter

从社交平台挖掘粉丝少但销量高的潜力爆品

四维验证模型：
- 内容维度：点赞>10
- 时间维度：1-2个月内
- 供给维度：评论<50
- 账号维度：粉丝<1000
"""

import asyncio
from typing import Dict, Any, List
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd

from . import BaseSkill
from tools.browser import BrowserTool


class LowFansHunter(BaseSkill):
    """低粉爆品挖掘"""
    
    # 违禁词列表
    PROHIBITED_WORDS = []
    
    # 筛选阈值
    THRESHOLDS = {
        "max_fans": 1000,      # 最大粉丝数
        "min_likes": 10,        # 最小点赞数
        "max_comments": 50,    # 最大评论数
        "max_days": 60          # 最大天数
    }
    
    def __init__(self, agent):
        super().__init__(agent)
        self.browser: BrowserTool = None
        self.results: List[Dict] = []
    
    async def connect_browser(self):
        """连接浏览器"""
        cdp_url = self.config.get("browser", {}).get("cdp_url", "http://127.0.0.1:9222")
        self.browser = BrowserTool(cdp_url)
        await self.browser.connect()
        self.log("已连接到浏览器")
    
    async def search_platform(self, platform: str, keyword: str, limit: int = 20):
        """
        搜索平台获取帖子列表
        
        Args:
            platform: 平台名称 (xiaohongshu/douyin/weibo)
            keyword: 搜索关键词
            limit: 获取数量
        """
        self.log(f"开始搜索: {platform} - {keyword}")
        
        if platform == "xiaohongshu":
            await self.search_xiaohongshu(keyword, limit)
        elif platform == "douyin":
            await self.search_douyin(keyword, limit)
        else:
            self.log(f"不支持的平台: {platform}")
    
    async def search_xiaohongshu(self, keyword: str, limit: int):
        """搜索小红书"""
        url = f"https://www.xiaohongshu.com/search_result?keyword={keyword}"
        
        try:
            await self.browser.goto(url)
            await asyncio.sleep(3)
            
            # 获取帖子列表
            posts = []
            
            # 模拟获取数据（实际需要解析页面）
            self.log(f"获取到 {len(posts)} 条帖子")
            
            return posts
        except Exception as e:
            self.log(f"搜索失败: {e}")
            return []
    
    async def search_douyin(self, keyword: str, limit: int):
        """搜索抖音"""
        # 类似实现
        pass
    
    async def verify_account(self, account_url: str) -> Dict[str, Any]:
        """
        验证账号粉丝数
        
        Args:
            account_url: 账号主页链接
        
        Returns:
            {"fans": int, "name": str}
        """
        try:
            await self.browser.goto(account_url)
            await asyncio.sleep(2)
            
            # 解析页面获取粉丝数
            # text = await self.browser.inner_text("body")
            # fans = self.extract_fans(text)
            
            return {"fans": 0, "name": ""}
        except Exception as e:
            self.log(f"验证账号失败: {e}")
            return {"fans": 9999, "name": ""}
    
    def filter_posts(self, posts: List[Dict]) -> List[Dict]:
        """
        筛选帖子
        
        四维验证：
        - 点赞 > 10
        - 时间 < 60天
        - 评论 < 50
        - 粉丝 < 1000
        """
        filtered = []
        
        for post in posts:
            likes = post.get("likes", 0)
            comments = post.get("comments", 0)
            fans = post.get("fans", 9999)
            days_ago = post.get("days_ago", 999)
            
            if (likes >= self.THRESHOLDS["min_likes"] and
                comments <= self.THRESHOLDS["max_comments"] and
                fans <= self.THRESHOLDS["max_fans"] and
                days_ago <= self.THRESHOLDS["max_days"]):
                filtered.append(post)
        
        self.log(f"筛选完成: {len(filtered)}/{len(posts)} 条符合条件")
        return filtered
    
    def check_prohibited_words(self, content: str) -> Dict[str, Any]:
        """
        检查违禁词
        
        Returns:
            {"has_violation": bool, "words": list}
        """
        violations = []
        content_lower = content.lower()
        
        for word in self.PROHIBITED_WORDS:
            if word.lower() in content_lower:
                violations.append(word)
        
        return {
            "has_violation": len(violations) > 0,
            "words": violations
        }
    
    def save_results(self, output_path: str):
        """保存结果"""
        if not self.results:
            self.log("没有结果需要保存")
            return
        
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        df = pd.DataFrame(self.results)
        df.to_excel(output_path, index=False)
        
        self.log(f"结果已保存: {output_path}")
    
    async def close(self):
        """关闭浏览器"""
        if self.browser:
            await self.browser.close()
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """
        执行技能
        
        Args:
            platform: 平台 (xiaohongshu/douyin)
            keyword: 搜索关键词
            output: 输出文件路径
            limit: 获取数量
        
        Returns:
            执行结果
        """
        platform = kwargs.get("platform", "xiaohongshu")
        keyword = kwargs.get("keyword", "")
        output = kwargs.get("output", "./output/low_fans_hunter.xlsx")
        limit = kwargs.get("limit", 20)
        
        self.log(f"开始执行低粉爆品挖掘: {platform} - {keyword}")
        
        try:
            # 连接浏览器
            await self.connect_browser()
            
            # 搜索帖子
            posts = await self.search_platform(platform, keyword, limit)
            
            # 逐个验证账号
            for post in posts:
                account_info = await self.verify_account(post.get("account_url", ""))
                post["fans"] = account_info.get("fans", 9999)
            
            # 筛选
            filtered = self.filter_posts(posts)
            
            # 保存结果
            self.results = filtered
            self.save_results(output)
            
            # 保存记忆
            self.save_memory("last_hunt", {
                "platform": platform,
                "keyword": keyword,
                "count": len(filtered),
                "timestamp": datetime.now().isoformat()
            })
            
            return {
                "success": True,
                "data": {
                    "total": len(posts),
                    "filtered": len(filtered),
                    "output": output
                },
                "message": f"找到 {len(filtered)} 条低粉爆品",
                "notify": True
            }
            
        except Exception as e:
            self.log(f"执行失败: {e}")
            return {
                "success": False,
                "data": {},
                "message": f"执行失败: {e}",
                "notify": False
            }
        finally:
            await self.close()


# 便捷函数
async def quick_hunt(platform: str, keyword: str, output: str = "./output/low_fans_hunter.xlsx"):
    """快速执行低粉爆品挖掘"""
    from main import EcommerceAgent
    
    agent = EcommerceAgent()
    hunter = LowFansHunter(agent)
    return await hunter.execute(platform=platform, keyword=keyword, output=output)
