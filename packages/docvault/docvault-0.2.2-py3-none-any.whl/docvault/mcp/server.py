import logging
from typing import Optional

import mcp.server.stdio

# Import types for responses
import mcp.types as types

# Import the FastMCP server
from mcp.server.fastmcp import FastMCP

import docvault.core.storage as storage
from docvault import config
from docvault.core.embeddings import search
from docvault.core.library_manager import lookup_library_docs
from docvault.core.scraper import get_scraper
from docvault.db import operations

types.ToolResult = types.CallToolResult  # alias for backward compatibility with tests

logger = logging.getLogger("docvault.mcp")


def create_server() -> FastMCP:
    """Create and configure the MCP server using FastMCP"""
    # Create FastMCP server
    server = FastMCP("DocVault")

    # Add document scraping tool
    @server.tool()
    async def scrape_document(url: str, depth: int = 1) -> types.CallToolResult:
        """Scrape a document from a URL and store it in the document vault"""
        try:
            scraper = get_scraper()
            result = await scraper.scrape_url(url, depth=depth)

            return types.CallToolResult(
                content=[
                    types.TextContent(
                        type="text",
                        text=f"Successfully scraped document: {result['title']} (ID: {result['id']})",
                    )
                ],
                metadata={
                    "document_id": result["id"],
                    "title": result["title"],
                    "url": url,
                    "success": True,
                },
            )
        except Exception as e:
            logger.exception(f"Error scraping document: {e}")
            return types.CallToolResult(
                content=[
                    types.TextContent(
                        type="text", text=f"Error scraping document: {str(e)}"
                    )
                ],
                metadata={"success": False, "error": str(e)},
            )

    # Add document search tool
    @server.tool()
    async def search_documents(query: str, limit: int = 5) -> types.CallToolResult:
        """Search documents in the vault using semantic search"""
        try:
            results = await search(query, limit=limit)

            content_items = []
            for r in results:
                result_text = f"Document: {r['title']} (ID: {r['document_id']})\n"
                result_text += f"Score: {r['score']:.2f}\n"
                result_text += f"Content: {r['content'][:200]}{'...' if len(r['content']) > 200 else ''}\n\n"

                content_items.append(types.TextContent(type="text", text=result_text))

            # If no results, add a message
            if not content_items:
                content_items.append(
                    types.TextContent(
                        type="text", text=f"No results found for '{query}'."
                    )
                )

            return types.CallToolResult(
                content=content_items,
                metadata={
                    "success": True,
                    "result_count": len(results),
                    "query": query,
                },
            )
        except Exception as e:
            logger.exception(f"Error searching documents: {e}")
            return types.CallToolResult(
                content=[
                    types.TextContent(
                        type="text", text=f"Error searching documents: {str(e)}"
                    )
                ],
                metadata={"success": False, "error": str(e)},
            )

    # Add document read tool
    @server.tool()
    async def read_document(
        document_id: int, format: str = "markdown"
    ) -> types.CallToolResult:
        """Read a document from the vault"""
        try:
            document = operations.get_document(document_id)

            if not document:
                return types.CallToolResult(
                    content=[
                        types.TextContent(
                            type="text", text=f"Document not found: {document_id}"
                        )
                    ],
                    metadata={
                        "success": False,
                        "error": f"Document not found: {document_id}",
                    },
                )

            if format.lower() == "html":
                content = storage.read_html(document["html_path"])
            else:
                content = storage.read_markdown(document["markdown_path"])

            return types.CallToolResult(
                content=[types.TextContent(type="text", text=content)],
                metadata={
                    "success": True,
                    "document_id": document_id,
                    "title": document["title"],
                    "url": document["url"],
                    "format": format,
                },
            )
        except Exception as e:
            logger.exception(f"Error reading document: {e}")
            return types.CallToolResult(
                content=[
                    types.TextContent(
                        type="text", text=f"Error reading document: {str(e)}"
                    )
                ],
                metadata={"success": False, "error": str(e)},
            )

    # Add library docs lookup tool
    @server.tool(name="lookup_library_docs")
    async def lookup_library_docs_tool(
        library_name: str, version: str = "latest"
    ) -> types.CallToolResult:
        """Lookup and fetch documentation for a specific library and version if not already available"""
        try:
            documents = await lookup_library_docs(library_name, version)

            if not documents:
                return types.CallToolResult(
                    content=[
                        types.TextContent(
                            type="text",
                            text=f"Could not find documentation for {library_name} {version}",
                        )
                    ],
                    metadata={
                        "success": False,
                        "message": f"Could not find documentation for {library_name} {version}",
                    },
                )

            content_text = (
                f"Documentation for {library_name} {version} is available:\n\n"
            )
            for doc in documents:
                content_text += f"- {doc['title']} (ID: {doc['id']})\n"

            return types.CallToolResult(
                content=[types.TextContent(type="text", text=content_text)],
                metadata={
                    "success": True,
                    "message": f"Documentation for {library_name} {version} is available",
                    "document_count": len(documents),
                    "documents": [
                        {"id": doc["id"], "title": doc["title"], "url": doc["url"]}
                        for doc in documents
                    ],
                },
            )
        except Exception as e:
            logger.exception(f"Error looking up library docs: {e}")
            return types.CallToolResult(
                content=[
                    types.TextContent(
                        type="text",
                        text=f"Error looking up library documentation: {str(e)}",
                    )
                ],
                metadata={"success": False, "error": str(e)},
            )

    # Add document listing tool
    @server.tool()
    async def list_documents(filter: str = "", limit: int = 20) -> types.CallToolResult:
        """List all documents in the vault"""
        try:
            documents = operations.list_documents(limit=limit, filter_text=filter)

            if not documents:
                return types.CallToolResult(
                    content=[
                        types.TextContent(
                            type="text", text="No documents found in the vault."
                        )
                    ],
                    metadata={"success": True, "document_count": 0},
                )

            content_text = f"Found {len(documents)} documents in the vault:\n\n"
            for doc in documents:
                content_text += f"- ID {doc['id']}: {doc['title']} ({doc['url']})\n"

            return types.CallToolResult(
                content=[types.TextContent(type="text", text=content_text)],
                metadata={
                    "success": True,
                    "document_count": len(documents),
                    "documents": [
                        {
                            "id": doc["id"],
                            "title": doc["title"],
                            "url": doc["url"],
                            "scraped_at": doc["scraped_at"],
                        }
                        for doc in documents
                    ],
                },
            )
        except Exception as e:
            logger.exception(f"Error listing documents: {e}")
            return types.CallToolResult(
                content=[
                    types.TextContent(
                        type="text", text=f"Error listing documents: {str(e)}"
                    )
                ],
                metadata={"success": False, "error": str(e)},
            )

    return server


async def _run_stdio_server(server: FastMCP):
    """Run the server with stdio transport"""
    async with mcp.server.stdio.stdio_server():
        await server.run()


def run_server(
    host: Optional[str] = None, port: Optional[int] = None, transport: str = "stdio"
) -> None:
    """Run the MCP server"""
    try:
        # Configure logging
        logging.basicConfig(
            level=logging.getLevelName(config.LOG_LEVEL),
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[logging.StreamHandler(), logging.FileHandler(config.LOG_FILE)],
        )

        logger.info(f"Starting DocVault MCP server with {transport} transport")

        # Create server
        server = create_server()

        # Use the appropriate transport
        if transport == "stdio":
            server.run()
        else:
            # Use HOST/PORT for SSE/web mode (Uvicorn)
            host = host or config.HOST
            port = port or config.PORT
            logger.info(f"Server will be available at http://{host}:{port}")
            server.run("sse")
    except Exception as e:
        logger.exception(f"Error running server: {e}")
