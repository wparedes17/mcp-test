import random
import uvicorn
from starlette.responses import PlainTextResponse
from fastmcp import FastMCP

# 1. Initialize
mcp = FastMCP("Name Decorator")

# 2. Define the Lists
PRETTY_ADJECTIVES = ['handsome', 'perfect', 'herculeo']
UGLY_ADJECTIVES = ['shit', 'scrooge', 'calderonic']

# 3. Tool: Pretty Name
@mcp.tool()
def pretty_name(name: str) -> str:
    """
    Takes a name and adds a compliment to it.
    Use this when the user wants a nice or positive version of a name.
    """
    # Pick a random word from the pretty list
    adjective = random.choice(PRETTY_ADJECTIVES)
    return f"{name} {adjective}"

# 4. Tool: Ugly Name
@mcp.tool()
def ugly_name(name: str) -> str:
    """
    Takes a name and adds an insult or ugly word to it.
    Use this when the user wants a bad, nasty, or ugly version of a name.
    """
    # Pick a random word from the ugly list
    adjective = random.choice(UGLY_ADJECTIVES)
    return f"{name} {adjective}"

# 5. Define Health Check
async def health(request):
    return PlainTextResponse("ok")

# 6. Extract App and Inject Health
# We use the standard http_app from FastMCP to ensure tools are registered correctly
app = mcp.http_app()
app.add_route("/health", health, methods=["GET"])

if __name__ == "__main__":
    # Run on port 8080
    uvicorn.run(app, host="0.0.0.0", port=8080)