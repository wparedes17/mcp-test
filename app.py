import json
import logging
from starlette.applications import Starlette
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Route
from starlette.requests import Request
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from mcp.server.fastmcp import FastMCP

# Basic MCP server with two example tools
mcp = FastMCP("Example MCP")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

# HTTP endpoints: /mcp for requests, /health for health checks
async def mcp_handler(request: Request):
    payload = await request.json()
    # Delegate to FastMCP to process the MCP message & return a response
    result = await mcp.handle_http(payload)
    return JSONResponse(result)

async def health(_request: Request):
    return PlainTextResponse("ok", status_code=200)

routes = [
    Route("/mcp", endpoint=mcp_handler, methods=["POST"]),
    Route("/health", endpoint=health, methods=["GET"]),
]

middleware = [
    Middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]),
]

app = Starlette(routes=routes, middleware=middleware)