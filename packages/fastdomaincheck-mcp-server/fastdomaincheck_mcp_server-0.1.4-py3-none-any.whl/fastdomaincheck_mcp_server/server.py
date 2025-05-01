import asyncio
import logging

# Low-level MCP server components
from mcp.server import Server
import mcp.server.stdio as stdio
import mcp.types as types
from mcp.server.models import InitializationOptions

# Import domain checking functions
# Note the relative import within the package
from .checker import check_domains_availability

# Configure logger (can keep the existing config)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create a low-level Server instance
# The server name here is used during initialization
server = Server("fastdomaincheck-mcp-server")

# Register check_domains_availability as an MCP Tool
# The low-level server expects async handlers
@server.call_tool()
async def check_domains(domains: list[str]) -> dict[str, str]:
    """Check if multiple domains are registered via stdio server."""
    logger.info(f"Received check_domains request via stdio for {len(domains)} domains.")
    # Run the synchronous blocking function in a separate thread
    # to avoid blocking the asyncio event loop.
    try:
        result = await asyncio.to_thread(check_domains_availability, domains)
        return result
    except Exception as e:
        logger.error(f"Error during check_domains_availability execution: {e}", exc_info=True)
        # Return an error structure or raise an exception appropriate for MCP tools if needed
        # For now, returning a simple error dictionary, although MCP might expect specific error handling.
        # Consider how errors should propagate via the tool call result.
        return {"error": f"Failed to check domains: {e}"}

# Main async function to run the stdio server
async def run_stdio_server():
    """Sets up and runs the MCP server over stdio."""
    logger.info("Starting FastDomainCheck MCP Server in stdio mode...")
    async with stdio.stdio_server() as (read_stream, write_stream):
        # Define server capabilities (only tools in this case)
        capabilities = server.get_capabilities(
            experimental_capabilities={}, # Add any experimental capabilities if needed
            # notification_options=None # No notifications defined
        )
        # Prepare initialization options
        init_options = InitializationOptions(
            server_name="fastdomaincheck-mcp-server",
            server_version="0.1.4", # Match pyproject.toml
            capabilities=capabilities
        )
        # Run the server loop
        await server.run(
            read_stream,
            write_stream,
            initialization_options=init_options,
        )
    logger.info("FastDomainCheck MCP Server stdio mode finished.")

def main():
    """
    Synchronous entry point for the MCP server.
    This function is used as the console_scripts entry point.
    """
    try:
        asyncio.run(run_stdio_server())
    except KeyboardInterrupt:
        logger.info("Server stopped by user.")

if __name__ == "__main__":
    main()
