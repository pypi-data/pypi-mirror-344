from django.urls import path, include
from django.conf import settings
from django_mcp.config import mcp_config
import logging

# Define the application namespace if needed, though often not required for included URLs
# app_name = 'django_mcp'

# Get the server instance
server = mcp_config.get_server()

# Start with empty list
urlpatterns = []

# Add the SSE endpoint from FastMCP if available
if server:
    # Get the URL patterns from the server
    # Allow configuring a prefix from settings, defaulting to 'mcp/'
    mcp_base_url = mcp_config.get('MCP_BASE_URL', '/mcp/')
    prefix = mcp_base_url.strip('/')
    
    server_urls = server.get_urls(prefix=prefix)
    
    # Add server URLs to the urlpatterns
    urlpatterns += server_urls
else:
    logger = logging.getLogger(__name__)
    logger.warning("MCP Server instance not found, cannot register MCP SSE URL endpoint.") 