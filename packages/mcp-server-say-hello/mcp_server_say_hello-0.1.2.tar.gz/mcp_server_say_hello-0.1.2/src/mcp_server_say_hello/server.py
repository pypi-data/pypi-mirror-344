import logging
from enum import Enum
from pydantic import BaseModel
from mcp.server import Server
from mcp.types import TextContent, Tool
from mcp.server.stdio import stdio_server

# 定义输入参数
class SayHelloInput(BaseModel):
    name: str

# 定义工具列表
class SayHelloTools(str, Enum):
    GREET = "say_hello"

logger = logging.getLogger(__name__)

async def serve() -> None:
    server = Server("mcp-server-say-hello")

    # 注册工具
    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name=SayHelloTools.GREET,
                description="向用户问好的工具",
                inputSchema=SayHelloInput.schema(),
            )
        ]

    # 处理工具调用
    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        if name == SayHelloTools.GREET:
            input_data = SayHelloInput(**arguments)
            return [TextContent(type="text", text=f"Hello {input_data.name}!")]

        return [
            TextContent(
                type="error",
                text=json.dumps({"error": "Invalid tool name", "code": 400}),
            )
        ]

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        print("MCP server started.")
        await server.run(read_stream, write_stream, options, raise_exceptions=True)
