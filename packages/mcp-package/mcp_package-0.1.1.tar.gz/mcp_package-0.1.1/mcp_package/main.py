from fastapi import FastAPI
from fastapi_mcp import FastApiMCP
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="My MCP Server")
print(os.getenv("openapi_key"))

# your APIs
@app.get("/")
async def hello():
    print("14",os.getenv("openapi_key"))
    return {"message": "Hello from MCP" + os.getenv("openapi_key")}

@app.get("/test")
async def test():
    return {"message": "Hello from MCP2" + os.getenv("openapi_key")}

# MCP mount
mcp = FastApiMCP(app)
mcp.mount() 