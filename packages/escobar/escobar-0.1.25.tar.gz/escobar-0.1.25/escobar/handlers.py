import json
import os
import re
from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join
import tornado
import aiohttp
from traitlets.config import LoggingConfigurable

# Default proxy port
DEFAULT_PROXY_PORT = 3000

class ProxyHandler(APIHandler):
    """
    Handler for /proxy endpoint.
    Proxies requests to http://localhost:<port>/<path>
    """
    @tornado.web.authenticated
    async def get(self, path_with_port):
        # Extract port and path from the URL
        # Expected format: <port>/<path>
        match = re.match(r'^(\d+)(?:/(.*))?$', path_with_port)
        
        if match:
            port = match.group(1)
            path = match.group(2) or ''
            
            # Ensure port is an integer
            try:
                port = int(port)
            except (ValueError, TypeError):
                self.set_status(400)
                self.finish({"error": f"Invalid port: {port}"})
                return
        else:
            # If no port is specified in the URL, use the default port
            # and treat the entire path_with_port as the path
            port = DEFAULT_PROXY_PORT
            path = path_with_port
        
        # Log the port and path for debugging
        self.log.info(f"Proxying request to port {port}, path: {path}")
        
        # Construct the target URL
        target_url = f"http://localhost:{port}/{path}"
        
        try:
            # Make the GET request to the target URL
            async with aiohttp.ClientSession() as session:
                async with session.get(target_url) as response:
                    # Get the response content
                    content = await response.text()
                    
                    # Set the same content type as the original response
                    self.set_header("Content-Type", response.headers.get("Content-Type", "text/plain"))
                    
                    # Return the content
                    self.finish(content)
        except Exception as e:
            self.set_status(500)
            self.finish({"error": str(e)})

def setup_handlers(web_app):
    host_pattern = ".*$"
    base_url = web_app.settings["base_url"]
    
    # Register the /proxy endpoint with a path parameter
    proxy_pattern = url_path_join(base_url, "proxy", "(.*)")
    handlers = [(proxy_pattern, ProxyHandler)]
    
    web_app.add_handlers(host_pattern, handlers)
