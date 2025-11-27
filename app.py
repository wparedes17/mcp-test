from fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route, Mount
import uvicorn

# Create the MCP server
mcp = FastMCP("Example MCP")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return 2 * (a + b)

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return 2 * (a * b)

# Health check endpoint
async def health(request):
    return PlainTextResponse("ok", status_code=200)

# Get FastMCP's ASGI app and mount it
mcp_app = mcp.get_asgi_app()

# Create main app with custom routes
app = Starlette(routes=[
    Route("/health", endpoint=health, methods=["GET"]),
    Mount("/", app=mcp_app),  # Mount MCP app at root
])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)