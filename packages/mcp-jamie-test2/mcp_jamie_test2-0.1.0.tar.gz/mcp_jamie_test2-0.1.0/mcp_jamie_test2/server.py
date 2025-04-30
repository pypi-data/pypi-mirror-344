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
server = Server("mcp-server-demo")


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
        )
    ]

async def add(a: int, b: int = 0) -> dict:
    logging.info(f"------Adding {a} and {b}")
    """Add two numbers together."""

    return {"result": a + b }


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