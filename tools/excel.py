"""
Excel处理工具
Excel Processing Tool
"""

import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Optional


class ExcelTool:
    """Excel读写工具"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
    
    def read(self, sheet_name: int = 0) -> pd.DataFrame:
        """
        读取Excel
        
        Args:
            sheet_name: 工作表名称或索引
        
        Returns:
            DataFrame
        """
        return pd.read_excel(self.file_path, sheet_name=sheet_name)
    
    def write(self, df: pd.DataFrame, sheet_name: str = "Sheet1", append: bool = False):
        """
        写入Excel
        
        Args:
            df: 数据DataFrame
            sheet_name: 工作表名称
            append: 是否追加模式
        """
        if append:
            # 追加模式：读取现有数据，合并，写入
            try:
                existing = pd.read_excel(self.file_path, sheet_name=sheet_name)
                df = pd.concat([existing, df], ignore_index=True)
            except FileNotFoundError:
                pass
        
        # 确保目录存在
        Path(self.file_path).parent.mkdir(parents=True, exist_ok=True)
        
        # 写入Excel
        with pd.ExcelWriter(self.file_path, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    def read_all_sheets(self) -> Dict[str, pd.DataFrame]:
        """读取所有工作表"""
        return pd.read_excel(self.file_path, sheet_name=None)
    
    def get_sheet_names(self) -> List[str]:
        """获取所有工作表名称"""
        xl_file = pd.ExcelFile(self.file_path)
        return xl_file.sheet_names


class ExcelBuilder:
    """Excel构建器"""
    
    def __init__(self):
        self.dataframes: Dict[str, pd.DataFrame] = {}
    
    def add_sheet(self, name: str, data: List[Dict[str, Any]]):
        """添加工作表"""
        self.dataframes[name] = pd.DataFrame(data)
    
    def add_dataframe(self, name: str, df: pd.DataFrame):
        """添加DataFrame"""
        self.dataframes[name] = df
    
    def save(self, file_path: str):
        """保存到文件"""
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            for sheet_name, df in self.dataframes.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)


def read_excel(file_path: str, sheet: int = 0) -> pd.DataFrame:
    """快速读取Excel"""
    return pd.read_excel(file_path, sheet_name=sheet)


def write_excel(file_path: str, data: List[Dict[str, Any]], sheet: str = "Sheet1"):
    """快速写入Excel"""
    df = pd.DataFrame(data)
    builder = ExcelBuilder()
    builder.add_sheet(sheet, data)
    builder.save(file_path)
