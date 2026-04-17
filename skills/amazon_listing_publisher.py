"""
亚马逊自动上架技能
Amazon Listing Publisher

批量创建亚马逊Listing

上架字段：
- 主图：白底
- 标题：核心词前置
- 五点描述：特性+痛点
- 关键词：长尾词
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path
import pandas as pd

from . import BaseSkill
from tools.excel import ExcelTool


class AmazonListingPublisher(BaseSkill):
    """亚马逊自动上架"""
    
    # 标题公式
    TITLE_TEMPLATE = "{brand} {核心关键词} {产品特性} {规格} {数量}"
    
    # 五点描述公式
    BULLET_TEMPLATE = [
        "【{特性}】{描述} - {痛点解决}",
        "【{特性}】{材质/工艺}",
        "【{特性}】{使用场景}",
        "【{特性}】{品质保证}",
        "【{售后}】{保障内容}"
    ]
    
    def __init__(self, agent):
        super().__init__(agent)
        self.listings: List[Dict] = []
    
    def generate_title(self, product: Dict, style: str = "standard") -> str:
        """
        生成标题
        
        Args:
            product: 产品数据
            style: 风格 (standard/premium/keyword_focused)
        
        Returns:
            标题
        """
        brand = product.get("brand", "")
        keyword = product.get("核心关键词", product.get("name", ""))
        feature = product.get("产品特性", "")
        spec = product.get("规格", "")
        quantity = product.get("数量", "")
        
        if style == "premium":
            # 强调品质
            return f"{brand} {keyword} - {feature} ({spec})"
        elif style == "keyword_focused":
            # 关键词优先
            return f"{keyword} {brand} {feature} {spec} {quantity}"
        else:
            # 标准格式
            return f"{brand} {keyword} {feature} {spec} {quantity}"
    
    def generate_bullets(self, product: Dict) -> List[str]:
        """
        生成五点描述
        
        Args:
            product: 产品数据
        
        Returns:
            五点描述列表
        """
        bullets = []
        
        for template in self.BULLET_TEMPLATE:
            bullet = template.format(
                特性=product.get("特性", "Premium Quality"),
                描述=product.get("描述", "High quality material"),
                痛点解决=product.get("痛点解决", "Perfect for daily use"),
                材质=product.get("材质", "Durable material"),
                工艺=product.get("工艺", "Fine craftsmanship"),
                使用场景=product.get("使用场景", "Suitable for home, office, outdoor"),
                品质保证=product.get("品质保证", "Quality Guarantee"),
                售后=product.get("售后", "Warranty"),
                保障内容=product.get("保障内容", "30-day money back")
            )
            bullets.append(bullet)
        
        return bullets
    
    def dehumanize_title(self, title: str) -> str:
        """
        去AI化标题
        
        Args:
            title: 原始标题
        
        Returns:
            去AI化后的标题
        """
        # 移除过于营销化的词汇
        replacements = {
            "Best": "Quality",
            "Top": "Excellent",
            "Premium": "Standard",
            "Luxury": "Classic",
        }
        
        result = title
        for old, new in replacements.items():
            result = result.replace(old, new)
        
        return result
    
    def generate_search_terms(self, product: Dict) -> str:
        """
        生成搜索关键词
        
        Args:
            product: 产品数据
        
        Returns:
            关键词字符串
        """
        keywords = product.get("关键词", [])
        if isinstance(keywords, str):
            keywords = keywords.split(",")
        
        # 添加同义词和长尾词
        base_keywords = product.get("核心关键词", "").split()
        all_keywords = list(keywords) + base_keywords
        
        # 限制250字节
        result = " ".join(all_keywords)
        if len(result) > 250:
            result = result[:247] + "..."
        
        return result
    
    def create_listing(self, product: Dict, style: str = "standard") -> Dict[str, Any]:
        """
        创建单个Listing
        
        Args:
            product: 产品数据
            style: 标题风格
        
        Returns:
            Listing数据
        """
        # 生成标题
        title = self.generate_title(product, style)
        title = self.dehumanize_title(title)
        
        # 生成五点描述
        bullets = self.generate_bullets(product)
        
        # 生成搜索关键词
        search_terms = self.generate_search_terms(product)
        
        # 产品描述
        description = product.get("产品描述", product.get("description", ""))
        
        return {
            "SKU": product.get("SKU", product.get("sku", "")),
            "ASIN": product.get("ASIN", product.get("asin", "")),
            "Title": title,
            "Bullet1": bullets[0] if len(bullets) > 0 else "",
            "Bullet2": bullets[1] if len(bullets) > 1 else "",
            "Bullet3": bullets[2] if len(bullets) > 2 else "",
            "Bullet4": bullets[3] if len(bullets) > 3 else "",
            "Bullet5": bullets[4] if len(bullets) > 4 else "",
            "Description": description,
            "SearchTerms": search_terms,
            "Price": product.get("价格", product.get("price", 0)),
            "Quantity": product.get("库存", product.get("quantity", 100)),
            "Status": "pending"
        }
    
    def create_batch(self, products: List[Dict], style: str = "standard") -> List[Dict]:
        """
        批量创建Listing
        
        Args:
            products: 产品列表
            style: 标题风格
        
        Returns:
            Listing列表
        """
        listings = []
        
        for product in products:
            listing = self.create_listing(product, style)
            listings.append(listing)
        
        self.listings = listings
        return listings
    
    def validate_listing(self, listing: Dict) -> Dict[str, Any]:
        """
        验证Listing
        
        Args:
            listing: Listing数据
        
        Returns:
            验证结果
        """
        errors = []
        
        # 检查标题长度
        title = listing.get("Title", "")
        if len(title) > 200:
            errors.append("标题超过200字符")
        elif len(title) < 50:
            errors.append("标题少于50字符")
        
        # 检查必填字段
        required_fields = ["SKU", "Title", "Price"]
        for field in required_fields:
            if not listing.get(field):
                errors.append(f"缺少必填字段: {field}")
        
        # 检查价格
        price = listing.get("Price", 0)
        if price <= 0:
            errors.append("价格必须大于0")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
    
    def export_for_upload(self, output_file: str, format: str = "excel") -> str:
        """
        导出上传文件
        
        Args:
            output_file: 输出文件
            format: 格式 (excel/csv/tsv)
        
        Returns:
            输出文件路径
        """
        if not self.listings:
            self.log("没有Listing需要导出")
            return None
        
        # 验证所有Listing
        for listing in self.listings:
            validation = self.validate_listing(listing)
            listing["Status"] = "✅ 有效" if validation["valid"] else f"❌ {', '.join(validation['errors'])}"
            listing["_validation"] = validation
        
        df = pd.DataFrame(self.listings)
        
        if format == "csv":
            df.to_csv(output_file, index=False, encoding="utf-8-sig")
        elif format == "tsv":
            df.to_csv(output_file, index=False, encoding="utf-8-sig", sep="\t")
        else:
            excel = ExcelTool(output_file)
            excel.write(df)
        
        self.log(f"导出完成: {output_file}")
        return output_file
    
    def generate_report(self) -> str:
        """生成上架报告"""
        if not self.listings:
            return "暂无Listing数据"
        
        valid_count = sum(1 for l in self.listings if "✅" in l.get("Status", ""))
        
        lines = [
            "# 亚马逊上架报告",
            f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            f"**商品总数**: {len(self.listings)}",
            f"**有效Listing**: {valid_count}",
            f"**待修复**: {len(self.listings) - valid_count}",
            ""
        ]
        
        # 列出问题
        issues = [l for l in self.listings if "❌" in l.get("Status", "")]
        if issues:
            lines.append("## 待修复问题")
            for listing in issues[:10]:
                lines.append(f"- **{listing.get('SKU')}**: {listing.get('Status').replace('❌ ', '')}")
            lines.append("")
        
        return "\n".join(lines)
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        执行技能
        
        Args:
            file_path: 产品数据文件
            output_file: 输出文件
            style: 标题风格 (standard/premium/keyword_focused)
            format: 导出格式 (excel/csv/tsv)
        
        Returns:
            执行结果
        """
        import json
        
        file_path = kwargs.get("file_path", "")
        output_file = kwargs.get("output_file", "./output/amazon_listings.xlsx")
        style = kwargs.get("style", "standard")
        format_type = kwargs.get("format", "excel")
        
        self.log(f"开始创建Listing, style={style}")
        
        try:
            # 加载数据
            if file_path.endswith(".json"):
                with open(file_path, 'r', encoding='utf-8') as f:
                    products = json.load(f)
            else:
                excel = ExcelTool(file_path)
                df = excel.read()
                products = df.to_dict('records')
            
            # 批量创建
            listings = self.create_batch(products, style)
            
            # 导出
            output = self.export_for_upload(output_file, format_type)
            
            # 生成报告
            report = self.generate_report()
            
            # 统计
            valid_count = sum(1 for l in listings if "✅" in l.get("Status", ""))
            
            return {
                "success": True,
                "data": {
                    "total": len(listings),
                    "valid": valid_count,
                    "invalid": len(listings) - valid_count,
                    "output_file": output
                },
                "message": f"创建完成: {len(listings)}个Listing, {valid_count}个有效",
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
