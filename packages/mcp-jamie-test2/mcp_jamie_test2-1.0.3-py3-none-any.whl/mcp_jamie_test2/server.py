from typing import Any
import asyncio
import httpx
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio
import logging
logging.basicConfig(level=logging.INFO)

# Create an MCP server
server = Server("mcp-jamie-test2")


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    列出可用的工具。
    每个工具使用 JSON Schema 验证来指定其参数。
    """
    return [
        types.Tool(
            name="add",
            description="Add two numbers together123",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "The first number"},
                    "b": {"type": "number", "description": "The second number"}
                },
                "required": ["a"]
            }
        ),
        types.Tool(
            name="text_processing",
            description="- 支持转化英文单词的大小写 \n - 支持统计英文单词的数量",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "str", "description": "等待转化的英文单词"},
                    "operation": {"type": "str", "description": "转换类型，可选upper/lower/count"}
                },
                "required": ["text"]
            }
        )

    ]

async def add(a: int, b: int = 0) -> dict:
    logging.info(f"------Adding {a} and {b}")
    """Add two numbers together."""

    return {"result": a + b }

async def text_processing(text: str, operation: str) -> str:
    """- 支持转化英文单词的大小写 - 支持统计英文单词的数量
    operation可选: upper/lower/count
    """
    if operation == "upper":
        return text.upper()
    elif operation == "lower":
        return text.lower()
    elif operation == "count":
        return str(len(text))
    else:
        raise ValueError("Invalid operation")

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    处理工具执行请求。
    """
    if not arguments:
        raise ValueError("缺少参数")
    if name == "add":
        result = await add(**arguments)
        return [types.TextContent(type="text", text=f"{result}")]
    if name == "text_processing":
        result = await text_processing(**arguments)
        return [types.TextContent(type="text", text=f"{result}")]
    else:
        raise NotImplementedError(f"工具 {name} 不支持")



async def main():
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="mcp-server-demo",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())