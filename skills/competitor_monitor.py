"""
竞品监控技能
Competitor Monitor

实时监控竞品价格、库存、评论、BSR排名变动

监控维度：
- 价格监控：变动>5%
- 库存监控：库存<20
- 评论监控：差评增加/评分下降
- BSR监控：排名变动>50名
- 促销监控：限时促销发现
"""

import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path
import pandas as pd

from . import BaseSkill
from tools.browser import BrowserTool
from tools.excel import ExcelTool


class CompetitorMonitor(BaseSkill):
    """竞品监控"""
    
    # 告警阈值
    THRESHOLDS = {
        "price_change": 0.05,    # 价格变动>5%
        "stock_low": 20,          # 库存<20
        "rating_drop": 0.2,       # 评分下降>0.2
        "bsr_change": 50,        # BSR排名变动>50
    }
    
    def __init__(self, agent):
        super().__init__(agent)
        self.browser: BrowserTool = None
        self.current_data: Dict[str, Dict] = {}
        self.alerts: List[Dict] = []
    
    async def connect_browser(self):
        """连接浏览器"""
        cdp_url = self.config.get("browser", {}).get("cdp_url", "http://127.0.0.1:9222")
        self.browser = BrowserTool(cdp_url)
        await self.browser.connect()
        self.log("已连接到浏览器")
    
    def load_previous_data(self, file_path: str) -> Dict[str, Dict]:
        """加载历史数据"""
        try:
            excel = ExcelTool(file_path)
            df = excel.read()
            
            data = {}
            for _, row in df.iterrows():
                product_id = row.get("商品ID", "")
                data[product_id] = {
                    "price": row.get("价格", 0),
                    "stock": row.get("库存", 0),
                    "rating": row.get("评分", 0),
                    "bsr": row.get("BSR", 0),
                    "comments": row.get("评论数", 0),
                    "update_time": row.get("更新时间", "")
                }
            
            return data
        except Exception as e:
            self.log(f"加载历史数据失败: {e}")
            return {}
    
    async def fetch_product_info(self, url: str) -> Dict[str, Any]:
        """
        获取商品信息
        
        Args:
            url: 商品URL
        
        Returns:
            商品信息
        """
        try:
            await self.browser.goto(url)
            await asyncio.sleep(3)
            
            # 实际需要解析页面
            # 这里简化处理
            
            return {
                "price": 0,
                "stock": 0,
                "rating": 0,
                "bsr": 0,
                "comments": 0
            }
        except Exception as e:
            self.log(f"获取商品信息失败: {e}")
            return {}
    
    def check_alerts(self, product_id: str, current: Dict, previous: Optional[Dict]) -> List[Dict]:
        """
        检查告警
        
        Args:
            product_id: 商品ID
            current: 当前数据
            previous: 历史数据
        
        Returns:
            告警列表
        """
        alerts = []
        
        if not previous:
            return alerts
        
        # 价格变动
        price_change = abs(current.get("price", 0) - previous.get("price", 0)) / max(previous.get("price", 1), 1)
        if price_change > self.THRESHOLDS["price_change"]:
            alerts.append({
                "type": "price_change",
                "product_id": product_id,
                "before": previous.get("price"),
                "after": current.get("price"),
                "change_rate": f"{price_change*100:.1f}%",
                "severity": "warning"
            })
        
        # 库存预警
        if current.get("stock", 999) < self.THRESHOLDS["stock_low"]:
            alerts.append({
                "type": "stock_low",
                "product_id": product_id,
                "stock": current.get("stock"),
                "severity": "critical" if current.get("stock", 999) < 5 else "warning"
            })
        
        # 评分下降
        rating_diff = previous.get("rating", 0) - current.get("rating", 0)
        if rating_diff > self.THRESHOLDS["rating_drop"]:
            alerts.append({
                "type": "rating_drop",
                "product_id": product_id,
                "before": previous.get("rating"),
                "after": current.get("rating"),
                "severity": "warning"
            })
        
        # BSR变动
        bsr_diff = abs(current.get("bsr", 0) - previous.get("bsr", 0))
        if bsr_diff > self.THRESHOLDS["bsr_change"]:
            alerts.append({
                "type": "bsr_change",
                "product_id": product_id,
                "before": previous.get("bsr"),
                "after": current.get("bsr"),
                "change": bsr_diff,
                "severity": "info"
            })
        
        return alerts
    
    def monitor_batch(self, urls: List[str], previous_file: str = None) -> List[Dict]:
        """
        批量监控
        
        Args:
            urls: 商品URL列表
            previous_file: 历史数据文件
        
        Returns:
            监控结果
        """
        # 加载历史数据
        previous_data = {}
        if previous_file:
            previous_data = self.load_previous_data(previous_file)
        
        results = []
        
        for url in urls:
            product_id = url.split("/")[-1]  # 简化
            current = self.fetch_product_info(url)  # 同步调用
            
            # 检查告警
            alerts = self.check_alerts(product_id, current, previous_data.get(product_id))
            
            results.append({
                "url": url,
                "product_id": product_id,
                "data": current,
                "alerts": alerts
            })
            
            # 更新当前数据
            self.current_data[product_id] = current
        
        self.alerts = [a for r in results for a in r["alerts"]]
        
        return results
    
    def save_current_data(self, output_file: str):
        """保存当前数据"""
        rows = []
        
        for product_id, data in self.current_data.items():
            rows.append({
                "商品ID": product_id,
                "价格": data.get("price", 0),
                "库存": data.get("stock", 0),
                "评分": data.get("rating", 0),
                "BSR": data.get("bsr", 0),
                "评论数": data.get("comments", 0),
                "更新时间": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
        
        df = pd.DataFrame(rows)
        excel = ExcelTool(output_file)
        excel.write(df)
        
        self.log(f"数据已保存: {output_file}")
    
    def generate_report(self) -> str:
        """生成监控报告"""
        if not self.alerts:
            return "✅ 本次监控未发现异常"
        
        lines = [
            "# 竞品监控报告",
            f"**监控时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            f"**告警总数**: {len(self.alerts)}",
            ""
        ]
        
        # 按类型分组
        by_type = {}
        for alert in self.alerts:
            alert_type = alert["type"]
            if alert_type not in by_type:
                by_type[alert_type] = []
            by_type[alert_type].append(alert)
        
        for alert_type, alerts in by_type.items():
            lines.append(f"## {alert_type.replace('_', ' ').title()}")
            
            for alert in alerts:
                severity_icon = "🔴" if alert["severity"] == "critical" else "⚠️"
                lines.append(f"{severity_icon} {alert['product_id']}")
                
                if alert_type == "price_change":
                    lines.append(f"   价格: {alert['before']} → {alert['after']} ({alert['change_rate']})")
                elif alert_type == "stock_low":
                    lines.append(f"   库存: {alert['stock']}")
                elif alert_type == "rating_drop":
                    lines.append(f"   评分: {alert['before']} → {alert['after']}")
                elif alert_type == "bsr_change":
                    lines.append(f"   BSR: {alert['before']} → {alert['after']} (变动{alert['change']})")
            
            lines.append("")
        
        return "\n".join(lines)
    
    async def close(self):
        """关闭浏览器"""
        if self.browser:
            await self.browser.close()
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """
        执行技能
        
        Args:
            urls: 商品URL列表（JSON字符串或列表）
            previous_file: 历史数据文件
            output_file: 输出文件
        
        Returns:
            执行结果
        """
        import json
        
        urls_str = kwargs.get("urls", "[]")
        previous_file = kwargs.get("previous_file", "")
        output_file = kwargs.get("output_file", "./output/competitor_monitor.xlsx")
        
        self.log("开始竞品监控")
        
        try:
            # 解析URLs
            if isinstance(urls_str, str):
                urls = json.loads(urls_str)
            else:
                urls = urls_str
            
            # 连接浏览器
            await self.connect_browser()
            
            # 批量监控
            results = self.monitor_batch(urls, previous_file if Path(previous_file).exists() else None)
            
            # 保存数据
            self.save_current_data(output_file)
            
            # 生成报告
            report = self.generate_report()
            
            # 统计
            critical_count = sum(1 for a in self.alerts if a["severity"] == "critical")
            warning_count = sum(1 for a in self.alerts if a["severity"] == "warning")
            
            return {
                "success": True,
                "data": {
                    "total": len(urls),
                    "alerts": len(self.alerts),
                    "critical": critical_count,
                    "warning": warning_count,
                    "output_file": output_file
                },
                "message": f"监控完成: {len(self.alerts)}个告警",
                "report": report,
                "notify": critical_count > 0  # 有严重告警时通知
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
