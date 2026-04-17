"""
图片处理工具
Image Processing Tool
"""

import base64
import requests
from pathlib import Path
from typing import Optional, List
from PIL import Image, ImageDraw, ImageFont


class ImageTool:
    """图片处理工具"""
    
    def __init__(self):
        self.session = requests.Session()
    
    def remove_background(self, image_path: str, output_path: str, api_key: str = None) -> bool:
        """
        移除背景
        
        Args:
            image_path: 输入图片路径
            output_path: 输出图片路径
            api_key: API密钥（使用在线服务）
        
        Returns:
            是否成功
        """
        # 这里需要集成实际的背景移除服务
        # 如 BiRefNet, remove.bg, Clipdrop 等
        
        try:
            # 示例：使用 PIL 进行简单处理
            img = Image.open(image_path)
            
            # 保存（实际需要调用AI模型）
            img.save(output_path)
            return True
        except Exception as e:
            print(f"背景移除失败: {e}")
            return False
    
    def add_text_watermark(self, image_path: str, output_path: str, text: str, 
                          position: str = "bottom-right", opacity: int = 128) -> bool:
        """
        添加文字水印
        
        Args:
            image_path: 输入图片路径
            output_path: 输出图片路径
            text: 水印文字
            position: 位置 (top-left/top-right/bottom-left/bottom-right/center)
            opacity: 透明度 (0-255)
        
        Returns:
            是否成功
        """
        try:
            img = Image.open(image_path)
            
            # 创建水印层
            watermark = Image.new('RGBA', img.size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(watermark)
            
            # 设置字体（使用默认字体）
            try:
                font = ImageFont.truetype("arial.ttf", 20)
            except:
                font = ImageFont.load_default()
            
            # 计算位置
            text_width, text_height = draw.textsize(text, font=font)
            
            positions = {
                "top-left": (10, 10),
                "top-right": (img.width - text_width - 10, 10),
                "bottom-left": (10, img.height - text_height - 10),
                "bottom-right": (img.width - text_width - 10, img.height - text_height - 10),
                "center": ((img.width - text_width) // 2, (img.height - text_height) // 2),
            }
            
            pos = positions.get(position, positions["bottom-right"])
            
            # 绘制文字
            draw.text(pos, text, fill=(255, 255, 255, opacity), font=font)
            
            # 合并
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            result = Image.alpha_composite(img, watermark)
            result.save(output_path)
            
            return True
        except Exception as e:
            print(f"添加水印失败: {e}")
            return False
    
    def resize_image(self, image_path: str, output_path: str, 
                    width: int = None, height: int = None, 
                    keep_ratio: bool = True) -> bool:
        """
        调整图片大小
        
        Args:
            image_path: 输入图片路径
            output_path: 输出图片路径
            width: 目标宽度
            height: 目标高度
            keep_ratio: 是否保持比例
        
        Returns:
            是否成功
        """
        try:
            img = Image.open(image_path)
            original_width, original_height = img.size
            
            if keep_ratio:
                if width and height:
                    # 按比例缩放
                    ratio = min(width / original_width, height / original_height)
                    new_width = int(original_width * ratio)
                    new_height = int(original_height * ratio)
                elif width:
                    ratio = width / original_width
                    new_width = width
                    new_height = int(original_height * ratio)
                elif height:
                    ratio = height / original_height
                    new_width = int(original_width * ratio)
                    new_height = height
                else:
                    new_width, new_height = original_width, original_height
            else:
                new_width = width or original_width
                new_height = height or original_height
            
            resized = img.resize((new_width, new_height), Image.LANCZOS)
            resized.save(output_path)
            
            return True
        except Exception as e:
            print(f"调整大小失败: {e}")
            return False
    
    def create_thumbnail(self, image_path: str, output_path: str, size: tuple = (200, 200)) -> bool:
        """
        创建缩略图
        
        Args:
            image_path: 输入图片路径
            output_path: 输出图片路径
            size: 缩略图大小
        
        Returns:
            是否成功
        """
        try:
            img = Image.open(image_path)
            img.thumbnail(size, Image.LANCZOS)
            img.save(output_path)
            return True
        except Exception as e:
            print(f"创建缩略图失败: {e}")
            return False
    
    def image_to_base64(self, image_path: str) -> str:
        """图片转base64"""
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    
    def base64_to_image(self, base64_str: str, output_path: str) -> bool:
        """base64转图片"""
        try:
            img_data = base64.b64decode(base64_str)
            with open(output_path, "wb") as f:
                f.write(img_data)
            return True
        except Exception as e:
            print(f"base64转图片失败: {e}")
            return False


class ImageGenerator:
    """AI图片生成器"""
    
    def __init__(self, api_url: str = None, api_key: str = None):
        self.api_url = api_url
        self.api_key = api_key
        self.session = requests.Session()
    
    def generate_image(self, prompt: str, output_path: str = None, 
                       model: str = "gpt-image-1") -> Optional[str]:
        """
        生成图片
        
        Args:
            prompt: 图片描述
            output_path: 输出路径
            model: 模型名称
        
        Returns:
            生成的图片路径或base64
        """
        # 这里需要集成实际的图片生成服务
        # 如 DALL-E, Midjourney, Stable Diffusion, Gemini 等
        
        print(f"图片生成功能需要配置API: {self.api_url}")
        return None
    
    def generate_product_image(self, product_name: str, style: str = "white_background") -> str:
        """
        生成产品图
        
        Args:
            product_name: 产品名称
            style: 风格 (white_background/scene/lifestyle)
        
        Returns:
            生成的图片路径
        """
        prompts = {
            "white_background": f"Professional product photo of {product_name}, clean white background, studio lighting, high quality, e-commerce",
            "scene": f"{product_name} placed in a modern living room setting, natural lighting, warm tones, photorealistic",
            "lifestyle": f"Lifestyle shot of {product_name} in use, warm lighting, cozy atmosphere, authentic, not staged",
        }
        
        prompt = prompts.get(style, prompts["white_background"])
        return self.generate_image(prompt)


def resize_keep_ratio(img: Image.Image, target_size: tuple) -> Image.Image:
    """保持比例缩放图片"""
    original_width, original_height = img.size
    target_width, target_height = target_size
    
    ratio = min(target_width / original_width, target_height / original_height)
    new_width = int(original_width * ratio)
    new_height = int(original_height * ratio)
    
    return img.resize((new_width, new_height), Image.LANCZOS)
