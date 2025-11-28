import uvicorn
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route, Mount
from fastmcp import FastMCP

# 1. Define MCP Server
mcp = FastMCP("Example MCP")

@mcp.tool()
def add(a: int, b: int) -> int:
    return 2 * (a + b)

@mcp.tool()
def multiply(a: int, b: int) -> int:
    return 2 * (a * b)

# 2. Get the modern HTTP app (Fixes Deprecation Warning)
# This sub-app internally handles "/sse" and "/messages"
mcp_app = mcp.http_app()

# 3. Define Health Check
async def health(request):
    return PlainTextResponse("ok")

# 4. Mount Routes
# We mount the MCP app at "/mcp".
# This means the SSE endpoint becomes: http://localhost:8080/mcp/sse
routes = [
    Route("/health", endpoint=health),
    Mount("/mcp", app=mcp_app),
]

app = Starlette(routes=routes)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)