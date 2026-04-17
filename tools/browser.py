"""
浏览器操作工具
Browser Automation Tool
"""

import asyncio
from typing import Optional, Dict, Any, List
from playwright.async_api import async_playwright, Page, Browser


class BrowserTool:
    """浏览器自动化工具"""
    
    def __init__(self, cdp_url: str = "http://127.0.0.1:9222"):
        self.cdp_url = cdp_url
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.playwright = None
    
    async def connect(self):
        """连接到浏览器"""
        self.playwright = async_playwright()
        await self.playwright.start()
        self.browser = await self.playwright.chromium.connect_over_cdp(self.cdp_url)
        self.page = await self.browser.new_page()
        return self
    
    async def goto(self, url: str, wait_until: str = "networkidle"):
        """打开页面"""
        await self.page.goto(url, wait_until=wait_until)
        await asyncio.sleep(2)
    
    async def click(self, selector: str, timeout: int = 30000):
        """点击元素"""
        await self.page.click(selector, timeout=timeout)
        await asyncio.sleep(1)
    
    async def fill(self, selector: str, value: str):
        """填写表单"""
        await self.page.fill(selector, value)
    
    async def query_selector_all(self, selector: str) -> List:
        """查询所有匹配元素"""
        return await self.page.query_selector_all(selector)
    
    async def inner_text(self, selector: str = "body") -> str:
        """获取元素文本"""
        return await self.page.inner_text(selector)
    
    async def screenshot(self, path: str):
        """截图"""
        await self.page.screenshot(path=path)
    
    async def close(self):
        """关闭浏览器"""
        if self.page:
            await self.page.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()


class BrowserContext:
    """浏览器上下文管理器"""
    
    def __init__(self, cdp_url: str = "http://127.0.0.1:9222"):
        self.tool = BrowserTool(cdp_url)
    
    async def __aenter__(self):
        await self.tool.connect()
        return self.tool
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.tool.close()


async def quick_screenshot(url: str, path: str, cdp_url: str = "http://127.0.0.1:9222"):
    """快速截图"""
    async with BrowserContext(cdp_url) as browser:
        await browser.goto(url)
        await browser.screenshot(path)


def sync_quick_screenshot(url: str, path: str, cdp_url: str = "http://127.0.0.1:9222"):
    """同步版本的快速截图"""
    asyncio.run(quick_screenshot(url, path, cdp_url))
