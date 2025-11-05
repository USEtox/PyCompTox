"""
API Key Management Utility for PyCompTox

This script helps you set up and manage your CompTox Dashboard API key.
"""

import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from pycomptox import save_api_key, load_api_key, delete_api_key, get_config_info


def main():
    """Main function for API key management."""
    
    print("=" * 60)
    print("PyCompTox API Key Management")
    print("=" * 60)
    print()
    
    # Show current configuration
    config_info = get_config_info()
    print("Current Configuration:")
    print(f"  Config Directory: {config_info['config_dir']}")
    print(f"  API Key File:     {config_info['api_key_file']}")
    print(f"  Saved API Key:    {'✓ Yes' if config_info['has_saved_key'] else '✗ No'}")
    print(f"  Env Variable:     {'✓ Set' if config_info['has_env_key'] else '✗ Not set'}")
    print(f"  API Key Available: {'✓ Yes' if config_info['api_key_available'] else '✗ No'}")
    print()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "set":
            # Set API key
            if len(sys.argv) < 3:
                print("Usage: python setup_api_key.py set YOUR_API_KEY")
                return
            
            api_key = sys.argv[2]
            try:
                save_api_key(api_key)
                print(f"✓ API key saved successfully to:")
                print(f"  {config_info['api_key_file']}")
                print()
                print("You can now use PyCompTox without providing the API key:")
                print("  from pycomptox import Chemical")
                print("  client = Chemical()  # API key loaded automatically")
            except Exception as e:
                print(f"✗ Error saving API key: {e}")
        
        elif command == "delete":
            # Delete API key
            if delete_api_key():
                print("✓ API key deleted successfully")
            else:
                print("✗ No saved API key found")
        
        elif command == "show":
            # Show API key (masked)
            api_key = load_api_key()
            if api_key:
                # Mask most of the key
                if len(api_key) > 8:
                    masked = api_key[:4] + "*" * (len(api_key) - 8) + api_key[-4:]
                else:
                    masked = "*" * len(api_key)
                print(f"API Key (masked): {masked}")
                
                if config_info['has_env_key']:
                    print("Source: Environment variable (COMPTOX_API_KEY)")
                else:
                    print(f"Source: Configuration file")
            else:
                print("✗ No API key found")
        
        elif command == "test":
            # Test API key
            print("Testing API connection...")
            try:
                from pycomptox import Chemical
                client = Chemical()
                
                # Try a simple search
                results = client.search_by_exact_value("DTXSID7020182")
                if results:
                    print(f"✓ API key is valid!")
                    print(f"  Test search successful: Found {results[0]['preferredName']}")
                else:
                    print("⚠ API key works but no results returned")
            except ValueError as e:
                print(f"✗ No API key configured: {e}")
            except PermissionError as e:
                print(f"✗ API key is invalid: {e}")
            except Exception as e:
                print(f"✗ Error testing API: {e}")
        
        else:
            print(f"Unknown command: {command}")
            show_usage()
    
    else:
        show_usage()


def show_usage():
    """Show usage information."""
    print("Usage:")
    print("  python setup_api_key.py set YOUR_API_KEY  - Save your API key")
    print("  python setup_api_key.py show              - Show current API key (masked)")
    print("  python setup_api_key.py delete            - Delete saved API key")
    print("  python setup_api_key.py test              - Test API key connection")
    print()
    print("Examples:")
    print('  python setup_api_key.py set "abc123xyz789"')
    print("  python setup_api_key.py test")


if __name__ == "__main__":
    main()
