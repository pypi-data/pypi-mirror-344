from mcp.server import FastMCP

mcp = FastMCP("wzk_test")


@mcp.tool()
def add_a_and_b(a, b):
    return a + b
