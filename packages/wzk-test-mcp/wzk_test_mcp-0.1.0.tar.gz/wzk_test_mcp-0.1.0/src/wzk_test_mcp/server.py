from mcp.server import FastMCP

mcp = FastMCP("wzk_test")


@mcp.tool()
def test_tool(a, b):
    return a + b
