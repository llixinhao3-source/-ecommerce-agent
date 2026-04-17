"""
高粉爆品追踪技能
High-Fans Hot Product Tracker

追踪已验证的爆品模式

类目轮换表：
周一: 家居日用 > 收纳整理
周二: 厨房用品 > 烹饪工具
周三: 数码配件 > 充电设备
周四: 美妆护肤 > 护肤工具
周五: 母婴用品 > 喂养用品
周六: 运动户外 > 健身装备
周日: 家纺布艺 > 床上用品

筛选标准：点赞>10，15天内
"""

import asyncio
from typing import Dict, Any, List
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd

from . import BaseSkill
from tools.browser import BrowserTool


class HighFansTracker(BaseSkill):
    """高粉爆品追踪"""
    
    # 类目轮换表
    CATEGORY_ROTATION = {
        0: {"大类": "家居日用", "小类": "收纳整理", "关键词": "收纳"},
        1: {"大类": "厨房用品", "小类": "烹饪工具", "关键词": "锅铲"},
        2: {"大类": "数码配件", "小类": "充电设备", "关键词": "充电宝"},
        3: {"大类": "美妆护肤", "小类": "护肤工具", "关键词": "化妆镜"},
        4: {"大类": "母婴用品", "小类": "喂养用品", "关键词": "水杯"},
        5: {"大类": "运动户外", "小类": "健身装备", "关键词": "瑜伽垫"},
        6: {"大类": "家纺布艺", "小类": "床上用品", "关键词": "四件套"},
    }
    
    # 筛选阈值
    THRESHOLDS = {
        "min_likes": 10,      # 最小点赞数
        "max_days": 15,        # 最大天数
    }
    
    def __init__(self, agent):
        super().__init__(agent)
        self.browser: BrowserTool = None
        self.results: List[Dict] = []
    
    def get_today_category(self) -> Dict[str, str]:
        """获取今天的类目"""
        weekday = datetime.now().weekday()
        return self.CATEGORY_ROTATION[weekday]
    
    async def connect_browser(self):
        """连接浏览器"""
        cdp_url = self.config.get("browser", {}).get("cdp_url", "http://127.0.0.1:9222")
        self.browser = BrowserTool(cdp_url)
        await self.browser.connect()
        self.log("已连接到浏览器")
    
    async def search_platform(self, platform: str, keyword: str, limit: int = 20):
        """搜索平台"""
        self.log(f"开始搜索: {platform} - {keyword}")
        
        if platform == "xiaohongshu":
            return await self.search_xiaohongshu(keyword, limit)
        return []
    
    async def search_xiaohongshu(self, keyword: str, limit: int):
        """搜索小红书"""
        url = f"https://www.xiaohongshu.com/search_result?keyword={keyword}"
        
        try:
            await self.browser.goto(url)
            await asyncio.sleep(3)
            
            # 获取帖子列表
            posts = []
            # 实际需要解析页面
            self.log(f"获取到 {len(posts)} 条帖子")
            
            return posts
        except Exception as e:
            self.log(f"搜索失败: {e}")
            return []
    
    async def verify_fans(self, account_url: str) -> Dict[str, Any]:
        """验证账号粉丝数"""
        try:
            await self.browser.goto(account_url)
            await asyncio.sleep(2)
            
            # 解析页面获取粉丝数
            return {"fans": 0, "name": ""}
        except Exception as e:
            self.log(f"验证失败: {e}")
            return {"fans": 0, "name": ""}
    
    def filter_posts(self, posts: List[Dict]) -> List[Dict]:
        """筛选帖子"""
        filtered = []
        
        for post in posts:
            likes = post.get("likes", 0)
            days_ago = post.get("days_ago", 999)
            
            if (likes >= self.THRESHOLDS["min_likes"] and
                days_ago <= self.THRESHOLDS["max_days"]):
                filtered.append(post)
        
        # 按点赞数排序
        filtered.sort(key=lambda x: x.get("likes", 0), reverse=True)
        
        self.log(f"筛选完成: {len(filtered)}/{len(posts)} 条符合条件")
        return filtered
    
    def analyze_content(self, post: Dict) -> Dict[str, Any]:
        """分析内容规律"""
        title = post.get("title", "")
        
        analysis = {
            "title_type": self.analyze_title_type(title),
            "has_number": any(c.isdigit() for c in title),
            "has_emoji": any(ord(c) > 127 for c in title),
            "length": len(title),
        }
        
        return analysis
    
    def analyze_title_type(self, title: str) -> str:
        """分析标题类型"""
        if "测评" in title or "对比" in title:
            return "测评型"
        elif "推荐" in title:
            return "推荐型"
        elif any(c.isdigit() for c in title):
            return "数字型"
        elif "干货" in title or "教程" in title:
            return "教程型"
        else:
            return "其他"
    
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
            keyword: 搜索关键词（可选，不填则根据轮换表）
            output: 输出文件路径
            limit: 获取数量
        
        Returns:
            执行结果
        """
        platform = kwargs.get("platform", "xiaohongshu")
        keyword = kwargs.get("keyword", "")
        output = kwargs.get("output", "./output/high_fans_tracker.xlsx")
        limit = kwargs.get("limit", 20)
        
        # 如果没有指定关键词，使用今天的类目
        if not keyword:
            category = self.get_today_category()
            keyword = category["关键词"]
            self.log(f"使用今日类目: {category['大类']} - {category['小类']}")
        
        self.log(f"开始执行高粉爆品追踪: {platform} - {keyword}")
        
        try:
            # 连接浏览器
            await self.connect_browser()
            
            # 搜索帖子
            posts = await self.search_platform(platform, keyword, limit)
            
            # 筛选
            filtered = self.filter_posts(posts)
            
            # 分析内容
            for post in filtered:
                post["content_analysis"] = self.analyze_content(post)
            
            self.results = filtered
            self.save_results(output)
            
            # 保存记忆
            self.save_memory("last_track", {
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
                    "output": output,
                    "keyword": keyword
                },
                "message": f"找到 {len(filtered)} 条高粉爆品",
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
        finally:
            await self.close()
