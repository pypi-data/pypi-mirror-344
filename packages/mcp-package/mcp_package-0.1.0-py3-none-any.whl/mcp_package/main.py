from fastapi import FastAPI
from fastapi_mcp import FastApiMCP

app = FastAPI(title="My MCP Server")

# your APIs
@app.get("/")
async def hello():
    return {"message": "Hello from MCP"}

# MCP mount
mcp = FastApiMCP(app)
mcp.mount() 