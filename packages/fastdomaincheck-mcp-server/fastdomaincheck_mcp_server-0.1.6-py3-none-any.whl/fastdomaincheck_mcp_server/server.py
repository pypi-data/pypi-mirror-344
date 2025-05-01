import asyncio
import logging
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

# Low-level MCP server components
from mcp.server import Server
import mcp.server.stdio as stdio
import mcp.types as types
from mcp.server.models import InitializationOptions
from mcp.server.lowlevel import NotificationOptions

# Import domain checking functions
# Note the relative import within the package
from .checker import check_domains_availability

# Configure logger (can keep the existing config)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@asynccontextmanager
async def server_lifespan(server: Server) -> AsyncIterator[dict]:
    """Manage server startup and shutdown lifecycle."""
    logger.info("Starting FastDomainCheck MCP Server...")
    try:
        # Initialize any resources here if needed
        yield {}
    finally:
        # Cleanup on shutdown
        logger.info("Shutting down FastDomainCheck MCP Server...")

# Create a server instance with lifespan management
server = Server("fastdomaincheck-mcp-server", lifespan=server_lifespan)

# Register check_domains_availability as an MCP Tool
# The low-level server expects async handlers
@server.call_tool()
async def check_domains(domains: list[str]) -> dict[str, str]:
    """Check if multiple domains are registered via stdio server."""
    logger.info(f"Received check_domains request for {len(domains)} domains.")
    try:
        # Run the synchronous blocking function in a separate thread
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
    async with stdio.stdio_server() as (read_stream, write_stream):
        # Define server capabilities
        capabilities = server.get_capabilities(
            experimental_capabilities={},
            notification_options=NotificationOptions()
        )
        # Prepare initialization options
        init_options = InitializationOptions(
            server_name="fastdomaincheck-mcp-server",
            server_version="0.1.6",  # Match pyproject.toml
            capabilities=capabilities
        )
        try:
            # Run the server loop with proper error handling
            await server.run(
                read_stream,
                write_stream,
                initialization_options=init_options,
            )
        except Exception as e:
            logger.error(f"Server error: {e}", exc_info=True)
            raise

def main():
    """
    Synchronous entry point for the MCP server.
    This function is used as the console_scripts entry point.
    """
    try:
        asyncio.run(run_stdio_server())
    except KeyboardInterrupt:
        logger.info("Server stopped by user.")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()
