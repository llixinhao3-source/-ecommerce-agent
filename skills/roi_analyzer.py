"""
ROI分析技能
ROI Analyzer

计算广告投放回报，指导投流决策

指标：
- CTR: 点击率
- CVR: 转化率
- CPA: 单订单成本
- ROI: 投资回报率
- ROAS: 广告支出回报
"""

import pandas as pd
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime

from . import BaseSkill
from tools.excel import ExcelTool


class ROIAnalyzer(BaseSkill):
    """ROI分析"""
    
    # 评级标准
    RATING_STANDARD = {
        "excellent": 300,   # ROI > 300%
        "good": 200,        # ROI 200-300%
        "normal": 100,      # ROI 100-200%
        "bad": 0            # ROI < 100%
    }
    
    def __init__(self, agent):
        super().__init__(agent)
        self.data: Optional[pd.DataFrame] = None
        self.results: List[Dict] = []
    
    def load_data(self, file_path: str, sheet: int = 0) -> pd.DataFrame:
        """加载数据"""
        excel = ExcelTool(file_path)
        self.data = excel.read(sheet)
        self.log(f"加载数据: {len(self.data)} 行")
        return self.data
    
    def calculate_metrics(self, row: pd.Series) -> Dict[str, float]:
        """
        计算单个广告计划的指标
        
        Args:
            row: 广告数据行
        
        Returns:
            计算后的指标
        """
        impressions = row.get("曝光", 0)
        clicks = row.get("点击", 0)
        orders = row.get("订单", 0)
        spend = row.get("花费", 0)
        revenue = row.get("销售额", 0)
        cost = row.get("成本", 0)
        
        # CTR
        ctr = (clicks / impressions * 100) if impressions > 0 else 0
        
        # CVR
        cvr = (orders / clicks * 100) if clicks > 0 else 0
        
        # CPA
        cpa = spend / orders if orders > 0 else 0
        
        # ROI
        profit = revenue - cost - spend
        roi = (profit / spend * 100) if spend > 0 else 0
        
        # ROAS
        roas = revenue / spend if spend > 0 else 0
        
        return {
            "ctr": ctr,
            "cvr": cvr,
            "cpa": cpa,
            "roi": roi,
            "roas": roas,
            "profit": profit
        }
    
    def rate_roi(self, roi: float) -> str:
        """ROI评级"""
        if roi > self.RATING_STANDARD["excellent"]:
            return "⭐⭐⭐⭐⭐ 优秀"
        elif roi > self.RATING_STANDARD["good"]:
            return "⭐⭐⭐⭐ 良好"
        elif roi > self.RATING_STANDARD["normal"]:
            return "⭐⭐⭐ 一般"
        else:
            return "⭐⭐ 亏损"
    
    def analyze(self, data: pd.DataFrame = None) -> List[Dict]:
        """
        分析所有广告数据
        
        Args:
            data: 可选的数据DataFrame
        
        Returns:
            分析结果列表
        """
        if data is not None:
            self.data = data
        
        if self.data is None:
            self.log("没有数据")
            return []
        
        results = []
        
        for idx, row in self.data.iterrows():
            metrics = self.calculate_metrics(row)
            rating = self.rate_roi(metrics["roi"])
            
            result = {
                "计划名称": row.get("计划名称", f"计划{idx+1}"),
                "花费": row.get("花费", 0),
                "销售额": row.get("销售额", 0),
                "订单": row.get("订单", 0),
                "CTR": f"{metrics['ctr']:.2f}%",
                "CVR": f"{metrics['cvr']:.2f}%",
                "CPA": f"¥{metrics['cpa']:.2f}",
                "ROI": f"{metrics['roi']:.2f}%",
                "ROAS": f"{metrics['roas']:.2f}",
                "评级": rating,
                "利润": metrics["profit"]
            }
            results.append(result)
        
        # 按ROI排序
        results.sort(key=lambda x: float(x["ROI"].replace("%", "").replace("⭐", "")), reverse=True)
        
        self.results = results
        return results
    
    def generate_report(self) -> str:
        """生成分析报告"""
        if not self.results:
            return "暂无分析数据"
        
        total_spend = sum(r["花费"] for r in self.results)
        total_revenue = sum(r["销售额"] for r in self.results)
        total_profit = sum(r["利润"] for r in self.results)
        avg_roi = (total_profit / total_spend * 100) if total_spend > 0 else 0
        
        lines = [
            "# ROI分析报告",
            f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "",
            "## 总体概览",
            f"- 广告计划数: {len(self.results)}",
            f"- 总花费: ¥{total_spend:,.2f}",
            f"- 总销售额: ¥{total_revenue:,.2f}",
            f"- 总利润: ¥{total_profit:,.2f}",
            f"- 平均ROI: {avg_roi:.2f}%",
            "",
            "## 计划详情",
            ""
        ]
        
        for r in self.results:
            lines.append(f"### {r['计划名称']}")
            lines.append(f"- 花费: ¥{r['花费']:,.2f}")
            lines.append(f"- 销售额: ¥{r['销售额']:,.2f}")
            lines.append(f"- CTR: {r['CTR']} | CVR: {r['CVR']} | CPA: {r['CPA']}")
            lines.append(f"- ROI: {r['ROI']} | 评级: {r['评级']}")
            lines.append("")
        
        return "\n".join(lines)
    
    def save_results(self, output_path: str):
        """保存结果到Excel"""
        if not self.results:
            self.log("没有结果需要保存")
            return
        
        df = pd.DataFrame(self.results)
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        df.to_excel(output_path, index=False)
        
        self.log(f"结果已保存: {output_path}")
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        执行ROI分析
        
        Args:
            file_path: 数据文件路径
            output: 输出文件路径
            generate_report: 是否生成报告
        
        Returns:
            执行结果
        """
        file_path = kwargs.get("file_path", "")
        output = kwargs.get("output", "./output/roi_report.xlsx")
        generate_report = kwargs.get("generate_report", False)
        
        self.log(f"开始ROI分析: {file_path}")
        
        try:
            # 加载数据
            self.load_data(file_path)
            
            # 分析
            results = self.analyze()
            
            # 保存
            self.save_results(output)
            
            # 生成报告
            report = self.generate_report() if generate_report else ""
            
            # 统计
            total = sum(r["花费"] for r in results)
            profit = sum(r["利润"] for r in results)
            avg_roi = (profit / total * 100) if total > 0 else 0
            
            # 找出最优和最差
            best = results[0] if results else {}
            worst = results[-1] if results else {}
            
            return {
                "success": True,
                "data": {
                    "count": len(results),
                    "total_spend": total,
                    "total_profit": profit,
                    "avg_roi": avg_roi,
                    "best_plan": best.get("计划名称", ""),
                    "worst_plan": worst.get("计划名称", ""),
                    "output": output
                },
                "message": f"分析完成: {len(results)}个计划, 平均ROI {avg_roi:.2f}%",
                "report": report,
                "notify": avg_roi < 100  # ROI低于100%时通知
            }
            
        except Exception as e:
            self.log(f"分析失败: {e}")
            return {
                "success": False,
                "data": {},
                "message": f"分析失败: {e}",
                "notify": False
            }
