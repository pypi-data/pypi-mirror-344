from mcp.server.fastmcp import FastMCP
# Import domain checking functions
from checker import check_domains_availability

# Create FastMCP instance, define service name
mcp = FastMCP("FastDomainCheck")


# Register check_domains_availability as an MCP Tool using a decorator
@mcp.tool()
def check_domains(domains: list[str]) -> dict[str, str]:
    """Check if multiple domains are registered."""
    return check_domains_availability(domains)

# Function to be called by the entry point script
def run_server():
    """Runs the MCP server using uvicorn."""
    try:
        import uvicorn
        print("Starting FastDomainCheck MCP Server with uvicorn...")
        # Use mcp.sse_app() which returns the ASGI application
        uvicorn.run(mcp.sse_app(), host="127.0.0.1", port=8000, log_level="info")
    except ImportError:
        print("Error: uvicorn is not installed. Please install it with 'uv add uvicorn[standard]' or 'pip install uvicorn[standard]'")
    except Exception as e:
        print(f"Failed to start server: {e}")

# The old main function (optional, can be removed or kept for other purposes)
# def main():
#     print("Initializing FastDomainCheck MCP Server components (if any)...")
#     pass

if __name__ == "__main__":
    # This block now calls the server running function for direct execution
    run_server()
    # print("To run the server using the installed package, use the defined script name (e.g., 'fastdomaincheck-server')")
    # print("To run via MCP runner, use: mcp run server.py")
