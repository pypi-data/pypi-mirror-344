"""
Moralis API MCP 服务基本测试
"""

import unittest
import asyncio
import os
from dotenv import load_dotenv
from mcp.client import MCPClient


# 加载环境变量
load_dotenv()


class TestMoralisApiMCP(unittest.TestCase):
    """测试Moralis API MCP服务的基本功能"""
    
    def setUp(self):
        """设置测试环境"""
        self.loop = asyncio.get_event_loop()
        self.client = MCPClient("http://localhost:8000")
        
        # 测试用的地址和交易哈希
        self.test_wallet = "0x1f9090aaE28b8a3dCeaDf281B0F12828e676c326"
        self.test_token = "0xdac17f958d2ee523a2206206994597c13d831ec7"  # USDT
        self.test_tx_hash = "0x2959cd3d09cca9b1e302e9feba8b3ba36b0dd75dff95bbfd3a146170d6f97aa2"
        
    async def async_test_wallet_balance(self):
        """测试获取钱包余额"""
        result = await self.client.call_tool(
            "get_wallet_balance",
            {"address": self.test_wallet, "chain": "eth"}
        )
        self.assertIsNotNone(result)
        
    async def async_test_token_price(self):
        """测试获取代币价格"""
        result = await self.client.call_tool(
            "get_token_price",
            {"address": self.test_token, "chain": "eth"}
        )
        self.assertIsNotNone(result)
        
    async def async_test_transaction(self):
        """测试获取交易详情"""
        result = await self.client.call_tool(
            "get_transaction_by_hash",
            {"transaction_hash": self.test_tx_hash, "chain": "eth"}
        )
        self.assertIsNotNone(result)
        
    def test_wallet_balance(self):
        """测试获取钱包余额的包装器"""
        self.loop.run_until_complete(self.async_test_wallet_balance())
        
    def test_token_price(self):
        """测试获取代币价格的包装器"""
        self.loop.run_until_complete(self.async_test_token_price())
        
    def test_transaction(self):
        """测试获取交易详情的包装器"""
        self.loop.run_until_complete(self.async_test_transaction())


if __name__ == "__main__":
    unittest.main() 