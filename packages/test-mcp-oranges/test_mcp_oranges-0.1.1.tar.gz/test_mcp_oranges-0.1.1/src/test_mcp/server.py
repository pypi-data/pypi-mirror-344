from mcp.server.fastmcp import FastMCP

mcp = FastMCP("DummyTestMCP")


@mcp.tool()
def hello_world() -> str:
    """Returns hello world greeting"""
    return "Hello World!"


if __name__ == "__main__":
    mcp.run()
