"""
钉钉推送工具
DingTalk Notification Tool
"""

import requests
from typing import Optional, Dict, Any


class DingTalk:
    """钉钉消息推送"""
    
    def __init__(self, webhook: str):
        self.webhook = webhook
        self.session = requests.Session()
    
    def send_text(self, content: str, at_mobiles: Optional[list] = None) -> Dict[str, Any]:
        """
        发送文本消息
        
        Args:
            content: 消息内容
            at_mobiles: 需要@的手机号列表
        
        Returns:
            API响应结果
        """
        payload = {
            "msgtype": "text",
            "text": {
                "content": content
            }
        }
        
        if at_mobiles:
            payload["at"] = {
                "atMobiles": at_mobiles
            }
        
        response = self.session.post(self.webhook, json=payload)
        return response.json()
    
    def send_markdown(self, title: str, content: str) -> Dict[str, Any]:
        """
        发送Markdown消息
        
        Args:
            title: 标题
            content: Markdown格式内容
        
        Returns:
            API响应结果
        """
        payload = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": content
            }
        }
        
        response = self.session.post(self.webhook, json=payload)
        return response.json()
    
    def send_link(self, title: str, text: str, message_url: str, pic_url: str = "") -> Dict[str, Any]:
        """
        发送链接消息
        
        Args:
            title: 标题
            text: 文本描述
            message_url: 点击后跳转链接
            pic_url: 图片URL
        
        Returns:
            API响应结果
        """
        payload = {
            "msgtype": "link",
            "link": {
                "title": title,
                "text": text,
                "messageUrl": message_url,
                "picUrl": pic_url
            }
        }
        
        response = self.session.post(self.webhook, json=payload)
        return response.json()
    
    def send_action_card(self, title: str, text: str, single_title: str, single_url: str) -> Dict[str, Any]:
        """
        发送ActionCard消息
        
        Args:
            title: 标题
            text: 消息内容
            single_title: 按钮标题
            single_url: 按钮跳转链接
        
        Returns:
            API响应结果
        """
        payload = {
            "msgtype": "actionCard",
            "actionCard": {
                "title": title,
                "text": text,
                "singleTitle": single_title,
                "singleURL": single_url
            }
        }
        
        response = self.session.post(self.webhook, json=payload)
        return response.json()


def create_dingtalk(webhook: str) -> DingTalk:
    """工厂函数：创建钉钉实例"""
    return DingTalk(webhook)
