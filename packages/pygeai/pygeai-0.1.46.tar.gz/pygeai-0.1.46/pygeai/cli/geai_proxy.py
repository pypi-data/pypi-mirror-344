#!/usr/bin/env python
import json
import asyncio
import sys
import argparse
import uuid
import yaml
from pygeai import logger
from pygeai.proxy.managers import ServerManager
from pygeai.proxy.config import ProxySettingsManager


def load_config(path: str) -> list:
    """
    Load server configuration from YAML or JSON file.

    :param path: str - Path to configuration file
    :return: list - List of server configurations
    :raises: FileNotFoundError - If the configuration file doesn't exist
    :raises: ValueError - If the file format is invalid or missing mcpServers key
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f) if path.endswith(('.yaml', '.yml')) else json.load(f)
            if 'mcpServers' not in config:
                raise ValueError(f"Config file '{path}' must contain 'mcpServers' key")
            
            servers = []
            for name, server_cfg in config['mcpServers'].items():
                server_cfg['name'] = name
                servers.append(server_cfg)
            return servers
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Configuration file '{path}' not found") from exc


def configure_proxy_settings(settings: ProxySettingsManager, args: argparse.Namespace, only_missing: bool = False):
    """
    Configure proxy settings interactively or from command line arguments.

    :param settings: ProxySettingsManager - Settings manager instance
    :param args: argparse.Namespace - Command line arguments
    :param only_missing: bool - Whether to only configure missing settings
    :return: None
    """
    if not args.alias:
        alias = input("-> Insert alias for settings section (Leave empty for default): ") or ProxySettingsManager.DEFAULT_ALIAS
    else:
        alias = args.alias

    current_id = settings.get_proxy_id(alias)
    current_name = settings.get_proxy_name(alias)
    current_description = settings.get_proxy_description(alias)
    current_affinity = settings.get_proxy_affinity(alias)

    first_time = not all([current_id, current_name, current_description])

    if not any([current_id, current_name, current_description, current_affinity]):
        sys.stdout.write("# Configuring GEAI proxy settings...\n")
        
        if not current_id:
            current_id = uuid.uuid4()
            settings.set_proxy_id(current_id, alias)
            sys.stdout.write(f"Generated new proxy ID: {current_id}\n")
        
        if not only_missing or not current_id:
            server_id = input(f"-> Insert proxy ID (UUID) (Current: {current_id}, Leave empty to keep): ")
            if server_id:
                try:
                    settings.set_proxy_id(uuid.UUID(server_id), alias)
                except ValueError:
                    sys.stderr.write("Error: Invalid UUID format\n")
                    return

        if not only_missing or not current_name:
            server_name = input("-> Insert proxy name (Leave empty to keep current value): ")
            if server_name:
                settings.set_proxy_name(server_name, alias)

        if not only_missing or not current_description:
            server_description = input("-> Insert proxy description (Leave empty to keep current value): ")
            if server_description:
                settings.set_proxy_description(server_description, alias)

        
        if not only_missing or (not current_affinity and first_time):
            server_affinity = input("-> Insert proxy affinity (UUID) (Leave empty to keep current value): ")
            if server_affinity:
                try:
                    settings.set_proxy_affinity(uuid.UUID(server_affinity), alias)
                except ValueError:
                    sys.stderr.write("Error: Invalid UUID format\n")
                    return
    else:
        # Command line mode
        if args.proxy_id:
            try:
                settings.set_proxy_id(uuid.UUID(args.proxy_id), alias)
            except ValueError:
                sys.stderr.write("Error: Invalid UUID format for proxy ID\n")
                return
        elif not only_missing or not settings.get_proxy_id(alias):
            # Generate new UUID if no ID is provided
            current_id = settings.get_proxy_id(alias)
            if not current_id:
                current_id = uuid.uuid4()
                settings.set_proxy_id(current_id, alias)
                sys.stdout.write(f"Generated new proxy ID: {current_id}\n")

        if args.proxy_name:
            settings.set_proxy_name(args.proxy_name, alias)
        elif not only_missing or not settings.get_proxy_name(alias):
            pass  # Name is not requested if not in args and only_missing is True

        if args.proxy_desc:
            settings.set_proxy_description(args.proxy_desc, alias)
        elif not only_missing or not settings.get_proxy_description(alias):
            pass  # Description is not requested if not in args and only_missing is True

        if args.proxy_affinity:
            try:
                settings.set_proxy_affinity(uuid.UUID(args.proxy_affinity), alias)
            except ValueError:
                sys.stderr.write("Error: Invalid UUID format for proxy affinity\n")
                return
        elif not only_missing or not settings.get_proxy_affinity(alias):
            pass  # Affinity is not requested if not in args and only_missing is True

    sys.stdout.write(f"Proxy settings for alias '{alias}' saved successfully!\n")


async def main():
    """
    Main entry point for the GEAI proxy CLI.

    :return: int - Exit code (0 for success, 1 for error)
    """
    logger.info("Starting GEAI proxy CLI")
    parser = argparse.ArgumentParser(description="Proxy CLI between GEAI and MCP servers")
    parser.add_argument("config", type=str, nargs="?", help="Path to the configuration file (JSON/YAML)")
    parser.add_argument("--list-tools", action="store_true", help="List all available tools")
    parser.add_argument("--invoke", type=str, help="Invoke a specific tool in JSON format")
    parser.add_argument("--configure", action="store_true", help="Configure proxy settings")
    parser.add_argument("--proxy-id", type=str, help="Set proxy server ID (UUID)")
    parser.add_argument("--proxy-name", type=str, help="Set proxy server name")
    parser.add_argument("--proxy-desc", type=str, help="Set proxy server description")
    parser.add_argument("--proxy-affinity", type=str, help="Set proxy server affinity (UUID)")
    parser.add_argument("--alias", type=str, help="Set alias for settings section")
    args = parser.parse_args()

    settings = ProxySettingsManager()
    if not args.alias:
        args.alias = "default"

    sys.stdout.write(f"Using alias: {args.alias}\n")
    # Force configuration if any required field is missing
    while True:
        if args.configure or not all([
            settings.get_proxy_id(args.alias),
            settings.get_proxy_name(args.alias),
            settings.get_proxy_description(args.alias),
            settings.get_api_key(args.alias),
            settings.get_base_url(args.alias)
        ]):
            sys.stdout.write("\nProxy configuration required. Please complete all required fields.\n")
            geai_api_key = settings.get_api_key(args.alias)
            geai_base_url = settings.get_base_url()
            sys.stdout.write(f"api_key: {geai_api_key}\n")
            sys.stdout.write(f"base_url: {geai_base_url}\n")
            configure_proxy_settings(settings, args, only_missing=not args.configure)
            args.configure = False  # Reset configure flag
        else:
            break

    if not args.config:
        sys.stderr.write("Error: Configuration file path is required\n")
        return 1

    servers_cfg = load_config(args.config)
    server_manager = ServerManager(servers_cfg, settings)
    await server_manager.start()

    return 0


def cli_entry() -> int:
    """
    CLI entry point.

    :return: int - Exit code (0 for success, 1 for error)
    """
    try:
        return asyncio.run(main())
    except KeyboardInterrupt:
        sys.stdout.write("\nExiting...\n")
        return 0
    except (RuntimeError, ConnectionError, ValueError) as e:
        sys.stderr.write(f"Error: {e}\n")
        return 1


if __name__ == "__main__":
    if len(sys.argv) == 1:
        import os
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(os.path.dirname(script_dir), "proxy", "sample-mcp-config.json")
        sys.stdout.write(f"Config file path: {config_path}\n")
        
        sys.argv.extend([config_path])
    sys.exit(cli_entry())
