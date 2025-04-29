from contextlib import AsyncExitStack
from typing import Any, List, Dict, Tuple
import asyncio
import json
import sys
from pygeai import logger
import mcp.types as types
from pygeai.proxy.servers import Server, MCPTool
from pygeai.proxy.config import ProxySettingsManager
from pygeai.proxy.clients import ProxyClient, ToolProxyData, ToolProxyJobResult


class ServerManager:
    """
    Manages multiple MCP servers.

    :param servers_cfg: List[Dict[str, Any]] - List of server configurations
    :param settings: ProxySettingsManager - Proxy settings manager
    """

    def __init__(self, servers_cfg: List[Dict[str, Any]], settings: ProxySettingsManager):
        """
        Initialize the server manager.

        :param servers_cfg: List[Dict[str, Any]] - List of server configurations
        :param settings: ProxySettingsManager - Proxy settings manager
        """
        self.servers_cfg = servers_cfg
        self.settings = settings
        self.servers: Dict[str, Server] = {}
        self.tools: Dict[str, MCPTool] = {}
        self.exit_stack: AsyncExitStack = AsyncExitStack()

    async def _initialize_servers(self) -> None:
        """
        Initialize all servers.

        :return: None
        :raises: Exception - If server initialization fails
        """
        for server_cfg in self.servers_cfg:
            server = Server(server_cfg['name'], server_cfg, self.settings)
            try:
                await self.exit_stack.enter_async_context(server.exit_stack)
                await server.initialize()
                self.servers[server.name] = server
            except Exception as e:
                logger.error("Failed to initialize server %s: %s", server.name, e)
                raise

        for server in self.servers.values():
            tools = await server.list_tools()
            for tool in tools:
                self.tools[tool.get_full_name()] = tool

    async def _initialize_client(self) -> ProxyClient:
        """
        Initialize the client.

        :return: ProxyClient - Initialized client instance
        """
        client = ProxyClient(self.settings.get_api_key(), self.settings.get_base_url(), self.settings.get_proxy_id())
        response = client.register(proxy_data=ToolProxyData(
            id=self.settings.get_proxy_id(),
            name=self.settings.get_proxy_name(),
            description=self.settings.get_proxy_description(),
            affinity=self.settings.get_proxy_affinity(),
            tools=list(self.tools.values())
        ))
        return client
    
    async def execute_tool(
        self,
        server_name: str,
        tool_name: str,
        arguments: dict[str, Any],
        retries: int = 2,
        delay: float = 1.0,
    ) -> Any:
        """
        Execute a tool with retry mechanism.

        :param server_name: str - Name of the server to execute the tool on
        :param tool_name: str - Name of the tool to execute
        :param arguments: dict[str, Any] - Tool arguments
        :param retries: int - Number of retry attempts
        :param delay: float - Delay between retries in seconds
        :return: Any - Tool execution result
        :raises: RuntimeError - If server is not found or not initialized
        :raises: Exception - If tool execution fails after all retries
        """
        if server_name not in self.servers:
            raise RuntimeError(f"Server {server_name} not found")
        
        if tool_name not in self.tools:
            raise RuntimeError(f"Tool {tool_name} not found")
            
        server = self.servers[server_name]
        
        result = await server.execute_tool(self.tools[tool_name].name, arguments, retries, delay)
        return result

    def extract_function_call_info(self, raw_json: str) -> Tuple[str, str]:
        """
        Extract function call info from raw JSON.

        :param raw_json: str - Raw JSON string
        :return: Tuple[str, str] - Tuple containing function name and arguments
        """
        try:
            data = json.loads(raw_json)
            return data['function']['name'], data['function']['arguments']
        except (json.JSONDecodeError, KeyError) as e:
            sys.stderr.write(f"Error extracting function call info: {e}\n")
            return None, None
        
    async def start(self) -> None:
        """
        Main proxy session handler.

        :return: None
        """
        try:
            await self._initialize_servers()
            client = await self._initialize_client()
            sys.stdout.write("Proxy initialized successfully\n")
            while True:
                jobs = client.dequeue()
                for job in jobs:
                    sys.stdout.write(f"----------------------------------Job: {job.id}----------------------------------\n")
                    tool_name, arguments = self.extract_function_call_info(job.input)
                    if tool_name:
                        sys.stdout.write(f"Executing tool {job.server}/{tool_name} with arguments {arguments}\n")
                        result = await self.execute_tool(job.server, tool_name, json.loads(arguments)) 
                        if isinstance(result.content, list):
                            for item in result.content:
                                if isinstance(item, types.TextContent):
                                    job.output = item.text
                                    sys.stdout.write(f"result: {job.output} success: {not result.isError}\n")
                                    client.send_result(ToolProxyJobResult(success=result.isError, job=job))
                                else:
                                    sys.stderr.write(f"Unknown content type {type(item)}\n")
                        else:
                            sys.stdout.write(f"{result}\n")
                await asyncio.sleep(1)
        finally:
            await self.exit_stack.aclose()