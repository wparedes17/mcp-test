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

# 2. Get the HTTP app
mcp_app = mcp.http_app()

# 3. Define Health Check
async def health(request):
    return PlainTextResponse("ok")

# 4. Define Routes
# We Mount "/" at the very end. This acts as a catch-all.
# /health  -> goes to health()
# /sse     -> goes to mcp_app
# /messages -> goes to mcp_app
routes = [
    Route("/health", endpoint=health),
    Mount("/", app=mcp_app),
]

app = Starlette(routes=routes)

# 5. DEBUG: Print routes on startup so we see exactly what paths exist
@app.on_event("startup")
async def startup_event():
    print("--> SERVER STARTING. REGISTERED ROUTES:", flush=True)
    # Print main routes
    for route in routes:
        if isinstance(route, Route):
            print(f"  - Path: {route.path}", flush=True)
        elif isinstance(route, Mount):
            print(f"  - Mount: {route.path} -> (Sub-app)", flush=True)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)