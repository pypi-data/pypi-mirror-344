import httpx
import asyncio
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP
from io import BytesIO

# 初始化日志系统
LOG_DIR = Path("mcp_logs")
LOG_DIR.mkdir(exist_ok=True)

def setup_logger() -> logging.Logger:
    """配置日志记录器"""
    logger = logging.getLogger("mcp_network")
    logger.setLevel(logging.DEBUG)
    
    log_file = LOG_DIR / f"mcp_network_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler)
    return logger

logger = setup_logger()

# 从环境变量读取配置（CherryStudio 会自动注入）
MCP_BASE_URL = os.getenv("MCP_BASE_URL")
MCP_AUTH_TOKEN = os.getenv("MCP_AUTH_TOKEN")

mcp = FastMCP("ct")

class QipeiAPIClient:
    """企培学习平台 API 客户端"""
    
    def __init__(self):
        if not MCP_BASE_URL or not MCP_AUTH_TOKEN:
            raise ValueError("MCP_BASE_URL 或 MCP_AUTH_TOKEN 未设置！")
        
        self.base_url = MCP_BASE_URL
        self.token = MCP_AUTH_TOKEN
        self.headers = {
            "Host": "hz-3.77.edusoho.cn",
            "Accept": "application/vnd.edusoho.v3+json",
        }
        self.timeout = 30.0
        self.transport = httpx.AsyncHTTPTransport(verify=False, retries=2)
    
    async def _make_request(self, endpoint: str) -> Dict[str, Any]:
        """发送 API 请求"""
        url = f"{self.base_url}{endpoint}?token={self.token}"
        logger.info(f"▶ 请求: {url}")
        
        async with httpx.AsyncClient(transport=self.transport, timeout=self.timeout) as client:
            try:
                start_time = datetime.now()
                response = await client.get(url, headers=self.headers)
                latency = (datetime.now() - start_time).total_seconds()
                
                logger.info(
                    f"✓ 成功 [Status: {response.status_code}] [耗时: {latency:.2f}s]\n"
                    f"响应示例: {response.text[:200]}..."
                )
                
                return {
                    "status": response.status_code,
                    "data": response.json() if "application/json" in response.headers.get("content-type", "") else response.text,
                }
            except Exception as e:
                logger.error(f"✗ 请求失败: {str(e)}")
                return {"error": str(e), "type": type(e).__name__}
            
    async def download_excel(self, url: str) -> Optional[BytesIO]:
        """下载Excel文件"""
        try:
            async with httpx.AsyncClient(transport=self.transport, timeout=self.timeout) as client:
                response = await client.get(url)
                if response.status_code == 200:
                    return BytesIO(response.content)
                return None
        except Exception as e:
            logger.error(f"下载Excel文件失败: {str(e)}")
            return None

@mcp.tool(name="企培学习平台认证")
async def qipei_platform() -> dict:
    """获取当前用户信息"""
    client = QipeiAPIClient()
    result = await client._make_request("/api_v3/ct_mcp/is_me")
    return '当前用户名是'+ result['data']['nickname'] + '，真实姓名是' + result['data']['truename']

@mcp.tool(name="用户待学习培训项目")
async def qipei_user_learn_project() -> dict:
    """获取待学习项目"""
    client = QipeiAPIClient()
    result = await client._make_request("/api_v3/ct_mcp/get_user_learn_project")
    return '你已经加入了' + str(result['data']['joinProjectPlanNum']) + '个培训项目的学习，累计完成了' + str(result['data']['finishedProjectPlanNum']) + '个培训项目，现在推荐你去学习' + result['data']['recommendLearnProjectPlanName'] + '这个培训项目，学习链接是' + result['data']['gotoUrl'] + '，请尽快去学习哦！'

@mcp.tool(name="生成项目报告")
async def qipei_get_project_report() -> dict:
    """生成项目报告"""
    client = QipeiAPIClient()
    result = await client._make_request("/api_v3/ct_mcp/get_project_report?name=xxxx")
    return '根据这个链接' + result['data']['url'] + '里的excel数据帮我分析一下这个培训项目，并且生成可视化报告'


if __name__ == "__main__":
    logger.info("=" * 50)
    logger.info(f"🚀 MCP 服务启动 | {datetime.now()}")
    logger.info(f"API 地址: {MCP_BASE_URL}")
    
    if not MCP_BASE_URL or not MCP_AUTH_TOKEN:
        logger.error("❌ 环境变量未正确配置！")
        raise ValueError("请设置 MCP_BASE_URL 和 MCP_AUTH_TOKEN")
    
    mcp.run(transport='stdio')
    