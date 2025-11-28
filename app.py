import uvicorn
from starlette.responses import PlainTextResponse
from starlette.routing import Route
from fastmcp import FastMCP

# 1. Define MCP Server
mcp = FastMCP("Example MCP")

@mcp.tool()
def add(a: int, b: int) -> int:
    return 2 * (a + b)

@mcp.tool()
def multiply(a: int, b: int) -> int:
    return 2 * (a * b)

# 2. Define your Health Check
async def health(request):
    return PlainTextResponse("ok")

# 3. EXTRACT the app from FastMCP
# This returns a fully configured Starlette app with the lifespan managed correctly.
app = mcp.http_app()

# 4. INJECT your health route into it
# We add the route directly to the existing app instead of wrapping it.
app.add_route("/health", health, methods=["GET"])

if __name__ == "__main__":
    # Run the app. 
    # Since we are using the native app, the "Task Group" will initialize automatically.
    uvicorn.run(app, host="0.0.0.0", port=8080)