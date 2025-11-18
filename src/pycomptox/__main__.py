"""
Command-line interface for PyCompTox.

This module provides CLI access to PyCompTox functionality,
primarily for API key management.
"""

import sys
import argparse
from typing import Optional

from .config import (
    save_api_key,
    load_api_key,
    delete_api_key,
    get_config_info,
)


def main(argv: Optional[list] = None) -> int:
    """
    Main entry point for the PyCompTox CLI.
    
    Args:
        argv: Command-line arguments (defaults to sys.argv)
        
    Returns:
        Exit code (0 for success, 1 for error)
    """
    parser = argparse.ArgumentParser(
        prog="pycomptox-setup",
        description="PyCompTox - EPA CompTox Dashboard API Client",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  pycomptox-setup set YOUR_API_KEY    Save your API key
  pycomptox-setup show                Show configuration
  pycomptox-setup delete              Delete saved API key
  pycomptox-setup test                Test API connection

For more information, visit: https://github.com/USEtox/PyCompTox
        """
    )
    
    parser.add_argument(
        "command",
        choices=["set", "show", "delete", "test"],
        help="Command to execute"
    )
    
    parser.add_argument(
        "api_key",
        nargs="?",
        help="API key (required for 'set' command)"
    )
    
    args = parser.parse_args(argv)
    
    try:
        if args.command == "set":
            if not args.api_key:
                print("Error: API key is required for 'set' command")
                print("Usage: pycomptox-setup set YOUR_API_KEY")
                return 1
            
            save_api_key(args.api_key)
            config_info = get_config_info()
            print(f"✓ API key saved successfully")
            print(f"  Location: {config_info['api_key_file']}")
            return 0
        
        elif args.command == "show":
            config_info = get_config_info()
            print("PyCompTox Configuration")
            print("=" * 70)
            print(f"Config directory: {config_info['config_dir']}")
            print(f"API key file: {config_info['api_key_file']}")
            print(f"API key saved: {'Yes' if config_info['has_saved_key'] else 'No'}")
            print(f"API key in environment: {'Yes' if config_info['has_env_key'] else 'No'}")
            print(f"API key available: {'Yes' if config_info['api_key_available'] else 'No'}")
            
            if config_info['has_saved_key']:
                api_key = load_api_key()
                if api_key and len(api_key) > 12:
                    masked_key = api_key[:8] + "*" * (len(api_key) - 12) + api_key[-4:]
                    print(f"API key: {masked_key}")
            
            return 0
        
        elif args.command == "delete":
            config_info = get_config_info()
            if not config_info['has_saved_key']:
                print("No API key is currently saved.")
                return 0
            
            delete_api_key()
            print("✓ API key deleted successfully")
            return 0
        
        elif args.command == "test":
            config_info = get_config_info()
            if not config_info['api_key_available']:
                print("Error: No API key found.")
                print("Please save an API key first:")
                print("  pycomptox-setup set YOUR_API_KEY")
                return 1
            
            print("Testing API connection...")
            
            try:
                from .chemical.search import Chemical
                
                client = Chemical()
                results = client.search_by_exact_value("Bisphenol A")
                
                if results:
                    print("✓ API key is valid")
                    print(f"✓ Test search successful: Found {results[0]['preferredName']}")
                    return 0
                else:
                    print("⚠ API key works but no results found")
                    return 0
            
            except PermissionError:
                print("✗ API key is invalid or expired")
                return 1
            except Exception as e:
                print(f"✗ Connection test failed: {e}")
                return 1
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        return 130
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
