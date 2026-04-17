"""
亚马逊选品技能
Amazon Product Selector

BSR分析 + 利润计算，科学选品

选品维度：
- 销量：月销>300单
- 竞争度：评论数<100
- 利润：毛利率>30%
- 评分：平均分<4.3
- 趋势：排名变化上升中
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path
import pandas as pd

from . import BaseSkill
from tools.browser import BrowserTool
from tools.excel import ExcelTool


class AmazonProductSelector(BaseSkill):
    """亚马逊选品"""
    
    # 选品标准
    STANDARDS = {
        "min_monthly_sales": 300,     # 最低月销
        "max_reviews": 100,           # 最大评论数
        "min_profit_rate": 0.30,     # 最低利润率
        "max_rating": 4.3,            # 最高平均评分
        "max_weight": 500,            # 最大重量(g)
    }
    
    # BSR分析标准
    BSR_STANDARDS = {
        "top100": {"name": "红海", "color": "red", "suggestion": "谨慎进入"},
        "100_500": {"name": "竞争激烈", "color": "orange", "suggestion": "有机会"},
        "500_2000": {"name": "有机会", "color": "yellow", "suggestion": "推荐"},
        "2000_plus": {"name": "蓝海", "color": "green", "suggestion": "强烈推荐"},
    }
    
    def __init__(self, agent):
        super().__init__(agent)
        self.browser: BrowserTool = None
        self.products: List[Dict] = []
    
    def analyze_bsr(self, bsr: int) -> Dict[str, str]:
        """分析BSR"""
        if bsr <= 100:
            return self.BSR_STANDARDS["top100"]
        elif bsr <= 500:
            return self.BSR_STANDARDS["100_500"]
        elif bsr <= 2000:
            return self.BSR_STANDARDS["500_2000"]
        else:
            return self.BSR_STANDARDS["2000_plus"]
    
    def calculate_profit(self, price: float, cost: float, shipping: float, 
                        platform_fee_rate: float = 0.15, ad_rate: float = 0.15) -> Dict[str, float]:
        """
        计算利润
        
        Args:
            price: 售价
            cost: 采购成本
            shipping: 国际运费
            platform_fee_rate: 平台费率
            ad_rate: 广告费率
        
        Returns:
            利润分析
        """
        revenue = price
        total_cost = cost + shipping
        platform_fee = revenue * platform_fee_rate
        ad_fee = revenue * ad_rate
        
        total_expense = total_cost + platform_fee + ad_fee
        profit = revenue - total_expense
        profit_rate = profit / revenue if revenue > 0 else 0
        
        return {
            "revenue": revenue,
            "cost": cost,
            "shipping": shipping,
            "platform_fee": platform_fee,
            "ad_fee": ad_fee,
            "total_cost": total_expense,
            "profit": profit,
            "profit_rate": profit_rate
        }
    
    def score_product(self, product: Dict) -> Dict[str, Any]:
        """
        评分产品
        
        评分公式：
        总分 = 销量分×0.3 + 利润分×0.25 + 竞争度分×0.25 + 评分分×0.2
        
        Args:
            product: 产品数据
        
        Returns:
            评分结果
        """
        scores = {}
        
        # 销量分 (0-100)
        monthly_sales = product.get("monthly_sales", 0)
        if monthly_sales >= 500:
            scores["sales"] = 100
        elif monthly_sales >= 300:
            scores["sales"] = 80
        elif monthly_sales >= 100:
            scores["sales"] = 60
        else:
            scores["sales"] = 40
        
        # 利润分 (0-100)
        profit_rate = product.get("profit_rate", 0)
        if profit_rate >= 0.40:
            scores["profit"] = 100
        elif profit_rate >= 0.30:
            scores["profit"] = 80
        elif profit_rate >= 0.20:
            scores["profit"] = 60
        else:
            scores["profit"] = 40
        
        # 竞争度分 (0-100)
        # 评论越少分数越高
        reviews = product.get("reviews", 999)
        if reviews <= 50:
            scores["competition"] = 100
        elif reviews <= 100:
            scores["competition"] = 80
        elif reviews <= 200:
            scores["competition"] = 60
        else:
            scores["competition"] = 40
        
        # 评分分 (0-100)
        # 评分越低分数越高（痛点存在）
        rating = product.get("rating", 5.0)
        if rating <= 4.0:
            scores["rating"] = 100
        elif rating <= 4.3:
            scores["rating"] = 80
        elif rating <= 4.5:
            scores["rating"] = 60
        else:
            scores["rating"] = 40
        
        # 总分
        total = (scores["sales"] * 0.3 + 
                 scores["profit"] * 0.25 + 
                 scores["competition"] * 0.25 + 
                 scores["rating"] * 0.2)
        
        # 评级
        if total >= 90:
            rating_text = "⭐⭐⭐⭐⭐ 强烈推荐"
        elif total >= 80:
            rating_text = "⭐⭐⭐⭐ 推荐"
        elif total >= 70:
            rating_text = "⭐⭐⭐ 一般"
        elif total >= 60:
            rating_text = "⭐⭐ 谨慎"
        else:
            rating_text = "⭐ 不推荐"
        
        return {
            "scores": scores,
            "total": total,
            "rating": rating_text
        }
    
    def check_standards(self, product: Dict) -> Dict[str, bool]:
        """
        检查是否符合选品标准
        
        Returns:
            检查结果
        """
        checks = {
            "销量达标": product.get("monthly_sales", 0) >= self.STANDARDS["min_monthly_sales"],
            "竞争度合格": product.get("reviews", 999) <= self.STANDARDS["max_reviews"],
            "利润达标": product.get("profit_rate", 0) >= self.STANDARDS["min_profit_rate"],
            "评分有空间": product.get("rating", 5.0) <= self.STANDARDS["max_rating"],
            "重量合格": product.get("weight", 999) <= self.STANDARDS["max_weight"],
        }
        
        checks["全部达标"] = all(checks.values())
        
        return checks
    
    def select_product(self, product_data: Dict) -> Dict[str, Any]:
        """
        选品分析
        
        Args:
            product_data: 产品数据
        
        Returns:
            选品结果
        """
        # 计算利润
        profit_info = self.calculate_profit(
            price=product_data.get("price", 0),
            cost=product_data.get("cost", 0),
            shipping=product_data.get("shipping", 0)
        )
        product_data.update(profit_info)
        
        # BSR分析
        bsr = product_data.get("bsr", 99999)
        bsr_analysis = self.analyze_bsr(bsr)
        
        # 评分
        score_result = self.score_product(product_data)
        
        # 标准检查
        checks = self.check_standards(product_data)
        
        return {
            "product_name": product_data.get("name", ""),
            "bsr": bsr,
            "bsr_level": bsr_analysis["name"],
            "profit": profit_info["profit"],
            "profit_rate": profit_info["profit_rate"],
            "scores": score_result["scores"],
            "total_score": score_result["total"],
            "rating": score_result["rating"],
            "checks": checks
        }
    
    def select_batch(self, products: List[Dict]) -> List[Dict]:
        """批量选品"""
        results = []
        
        for product in products:
            result = self.select_product(product)
            results.append(result)
        
        # 按总分排序
        results.sort(key=lambda x: x["total_score"], reverse=True)
        
        self.products = results
        return results
    
    def generate_report(self) -> str:
        """生成选品报告"""
        if not self.products:
            return "暂无选品数据"
        
        lines = [
            "# 亚马逊选品报告",
            f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            f"**分析商品**: {len(self.products)} 个",
            ""
        ]
        
        # 统计
        recommend_count = sum(1 for p in self.products if p["total_score"] >= 80)
        lines.append(f"## 统计概览")
        lines.append(f"- 强烈推荐/推荐: {recommend_count} 个")
        lines.append(f"- 合格率: {recommend_count/len(self.products)*100:.1f}%")
        lines.append("")
        
        # TOP10
        lines.append("## TOP10 推荐")
        lines.append("")
        
        for i, product in enumerate(self.products[:10], 1):
            color_icon = "🟢" if "强烈推荐" in product["rating"] else "🟡"
            lines.append(f"{i}. {color_icon} {product['product_name']}")
            lines.append(f"   BSR: {product['bsr']} ({product['bsr_level']})")
            lines.append(f"   利润: ${product['profit']:.2f} ({product['profit_rate']*100:.1f}%)")
            lines.append(f"   评分: {product['rating']} (总分: {product['total_score']:.1f})")
            lines.append("")
        
        return "\n".join(lines)
    
    def save_results(self, output_file: str):
        """保存结果"""
        if not self.products:
            self.log("没有结果需要保存")
            return
        
        df = pd.DataFrame(self.products)
        
        # 排序
        df = df.sort_values("total_score", ascending=False)
        
        excel = ExcelTool(output_file)
        excel.write(df)
        
        self.log(f"结果已保存: {output_file}")
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        执行技能
        
        Args:
            file_path: 产品数据文件（Excel/JSON）
            output_file: 输出文件
        
        Returns:
            执行结果
        """
        import json
        
        file_path = kwargs.get("file_path", "")
        output_file = kwargs.get("output_file", "./output/amazon_selection.xlsx")
        
        self.log("开始亚马逊选品分析")
        
        try:
            # 加载数据
            if file_path.endswith(".json"):
                with open(file_path, 'r', encoding='utf-8') as f:
                    products = json.load(f)
            else:
                excel = ExcelTool(file_path)
                df = excel.read()
                products = df.to_dict('records')
            
            # 批量选品
            results = self.select_batch(products)
            
            # 保存结果
            self.save_results(output_file)
            
            # 生成报告
            report = self.generate_report()
            
            # 统计
            recommend_count = sum(1 for p in results if p["total_score"] >= 80)
            
            return {
                "success": True,
                "data": {
                    "total": len(results),
                    "recommended": recommend_count,
                    "pass_rate": f"{recommend_count/len(results)*100:.1f}%",
                    "output_file": output_file
                },
                "message": f"选品完成: {len(results)}个商品, {recommend_count}个推荐",
                "report": report,
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
