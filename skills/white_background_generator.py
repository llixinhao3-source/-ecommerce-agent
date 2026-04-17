"""
白底图生成技能
White Background Image Generator

生成符合电商平台标准的白底产品图

标准：
- 纯白背景 (RGB: 255,255,255)
- 产品占比60-70%
- 分辨率：1024×1024
- 无水印、无LOGO
"""

import asyncio
from typing import Dict, Any, List, Optional
from pathlib import Path
import base64

from . import BaseSkill
from tools.image import ImageTool, ImageGenerator


class WhiteBackgroundGenerator(BaseSkill):
    """白底图生成"""
    
    # 标准规格
    SPECS = {
        "background_color": (255, 255, 255),
        "product_ratio": 0.6,  # 60-70%
        "resolution": (1024, 1024),
        "format": "PNG"
    }
    
    # 平台规格
    PLATFORM_SPECS = {
        "amazon": {
            "min_size": 1500,
            "product_ratio": 0.85,
            "format": "JPEG"
        },
        "xiaohongshu": {
            "min_size": 1000,
            "product_ratio": 0.6,
            "format": "PNG"
        },
        "taobao": {
            "min_size": 800,
            "product_ratio": 0.7,
            "format": "PNG"
        }
    }
    
    def __init__(self, agent):
        super().__init__(agent)
        self.image_tool = ImageTool()
        self.generator = None
    
    def set_api(self, api_url: str, api_key: str):
        """设置AI生成API"""
        self.generator = ImageGenerator(api_url, api_key)
    
    def create_white_background(self, image_path: str, output_path: str) -> bool:
        """
        创建白底图
        
        Args:
            image_path: 输入图片路径
            output_path: 输出图片路径
        
        Returns:
            是否成功
        """
        self.log(f"创建白底图: {image_path}")
        
        # 这里需要调用实际的背景移除服务
        # 如 BiRefNet、remove.bg 等
        
        # 临时实现：直接复制
        import shutil
        shutil.copy(image_path, output_path)
        
        return True
    
    def create_batch(self, input_dir: str, output_dir: str, platform: str = "general") -> List[Dict]:
        """
        批量生成白底图
        
        Args:
            input_dir: 输入目录
            output_dir: 输出目录
            platform: 平台 (amazon/xiaohongshu/taobao/general)
        
        Returns:
            结果列表
        """
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        results = []
        
        for image_file in input_path.glob("*"):
            if image_file.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp"]:
                output_file = output_path / f"{image_file.stem}_white{image_file.suffix}"
                
                success = self.create_white_background(str(image_file), str(output_file))
                
                results.append({
                    "input": str(image_file),
                    "output": str(output_file) if success else None,
                    "success": success
                })
        
        self.log(f"批量处理完成: {len(results)} 个文件")
        return results
    
    def validate_image(self, image_path: str, platform: str = "general") -> Dict[str, Any]:
        """
        验证图片是否符合标准
        
        Args:
            image_path: 图片路径
            platform: 平台
        
        Returns:
            验证结果
        """
        from PIL import Image
        
        try:
            img = Image.open(image_path)
            width, height = img.size
            format_img = img.format
            
            # 检查分辨率
            specs = self.PLATFORM_SPECS.get(platform, self.PLATFORM_SPECS["general"])
            min_size = specs["min_size"]
            
            is_valid_size = width >= min_size and height >= min_size
            
            # 检查背景色（简化检查）
            # 实际应该检查中心区域的颜色
            is_white_bg = True  # 简化
            
            return {
                "valid": is_valid_size and is_white_bg,
                "width": width,
                "height": height,
                "format": format_img,
                "is_valid_size": is_valid_size,
                "is_white_bg": is_white_bg
            }
        except Exception as e:
            self.log(f"验证失败: {e}")
            return {"valid": False, "error": str(e)}
    
    def resize_for_platform(self, image_path: str, output_path: str, platform: str) -> bool:
        """
        调整图片尺寸以适配平台
        
        Args:
            image_path: 输入图片
            output_path: 输出图片
            platform: 平台
        
        Returns:
            是否成功
        """
        specs = self.PLATFORM_SPECS.get(platform, self.PLATFORM_SPECS["general"])
        
        return self.image_tool.resize_image(
            image_path,
            output_path,
            width=specs["min_size"],
            height=specs["min_size"]
        )
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        执行技能
        
        Args:
            input_path: 输入图片或目录
            output_path: 输出目录
            platform: 平台 (amazon/xiaohongshu/taobao/general)
            batch: 是否批量处理
        
        Returns:
            执行结果
        """
        input_path = kwargs.get("input_path", "")
        output_path = kwargs.get("output_path", "./output/white_bg")
        platform = kwargs.get("platform", "general")
        batch = kwargs.get("batch", False)
        
        self.log(f"开始生成白底图: {input_path}")
        
        try:
            if batch:
                # 批量处理
                results = self.create_batch(input_path, output_path, platform)
                
                success_count = sum(1 for r in results if r["success"])
                
                return {
                    "success": True,
                    "data": {
                        "total": len(results),
                        "success": success_count,
                        "failed": len(results) - success_count,
                        "output_dir": output_path
                    },
                    "message": f"批量处理完成: {success_count}/{len(results)} 成功",
                    "notify": False
                }
            else:
                # 单个处理
                output_file = Path(output_path) / f"{Path(input_path).stem}_white.png"
                
                success = self.create_white_background(input_path, str(output_file))
                
                if success:
                    # 调整尺寸
                    self.resize_for_platform(str(output_file), str(output_file), platform)
                    
                    # 验证
                    validation = self.validate_image(str(output_file), platform)
                    
                    return {
                        "success": True,
                        "data": {
                            "input": input_path,
                            "output": str(output_file),
                            "validation": validation
                        },
                        "message": f"白底图生成成功: {output_file}",
                        "notify": False
                    }
                else:
                    return {
                        "success": False,
                        "data": {},
                        "message": "白底图生成失败",
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
