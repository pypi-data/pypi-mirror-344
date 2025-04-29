from mcp.server.fastmcp import FastMCP

mcp = FastMCP("DummyTestMCP")


@mcp.tool()
def hello_world() -> str:
    """Returns hello world greeting"""
    return "Hello World!"


def main() -> None:
    """Run the MCP server"""
    print("Starting MCP server")
    mcp.run()


if __name__ == "__main__":
    main()
