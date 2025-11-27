import uvicorn
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route, Mount
from fastmcp import FastMCP

# 1. Define your MCP Server
mcp = FastMCP("Example MCP")

@mcp.tool()
def add(a: int, b: int) -> int:
    return 2 * (a + b)

@mcp.tool()
def multiply(a: int, b: int) -> int:
    return 2 * (a * b)

# 2. Define your custom health check
async def health(request):
    return PlainTextResponse("ok")

# 3. Create the Starlette App
# We "mount" the MCP server at "/sse" (or any path you prefer).
# .sse_app() creates an ASGI app specifically for the MCP protocol.
mcp_app = mcp.sse_app()

routes = [
    Route("/health", endpoint=health),
    Mount("/sse", app=mcp_app), # MCP is now available at http://.../sse
]

app = Starlette(routes=routes)

if __name__ == "__main__":
    # Run the parent Starlette app
    uvicorn.run(app, host="0.0.0.0", port=8000)