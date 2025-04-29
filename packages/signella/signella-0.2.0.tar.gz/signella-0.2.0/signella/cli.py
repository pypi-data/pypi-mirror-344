#!/usr/bin/env python3
import os
import sys
import argparse
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def print_colored(text, color=Fore.WHITE, bold=False):
    """Print text with color and optional bold formatting."""
    if bold:
        print(f"{color}{Style.BRIGHT}{text}")
    else:
        print(f"{color}{text}")

def print_header(text):
    """Print a section header."""
    print("\n" + "=" * 60)
    print_colored(f"  {text}  ", Fore.CYAN, bold=True)
    print("=" * 60)

def print_env_var(name, value, description):
    """Print an environment variable with its value and description."""
    print_colored(f"{Fore.GREEN}{name}: ", bold=True, color=Fore.GREEN)
    
    if value:
        print_colored(f"  Current Value: {value}", Fore.YELLOW)
    else:
        print_colored(f"  Current Value: {Fore.RED}Not Set", Fore.RED)
    
    print_colored(f"  Description: {description}", Fore.WHITE)
    print()

def show_help():
    """Display help information about Signella."""
    print_header("SIGNELLA - Redis-based Variable Sharing")
    
    print_colored("Signella is a Redis-based variable sharing singleton for Python.", Fore.WHITE)
    print_colored("It provides a simple dictionary-like interface with JSON serialization.", Fore.WHITE)
    print_colored("Signella automatically starts a Redis server if one isn't available.", Fore.WHITE)
    print("\n")
    
    print_header("USAGE")
    print_colored("From Python:", Fore.MAGENTA, bold=True)
    print("""
    from signella import signal

    # Set values
    signal['name'] = 'Jimmy'

    # Get values
    print(signal['name'])

    # Use compound keys
    signal['user', 123, 'profile'] = {'name': 'Jimmy', 'age': 30}
    print(signal['user', 123, 'profile'])
    """)
    
    print_header("ENVIRONMENT VARIABLES")
    
    # Display each environment variable with current value and description
    print_env_var(
        "RADIOVAR_PORT", 
        os.getenv("RADIOVAR_PORT"), 
        "Override the default Redis port (6379)"
    )
    
    print_env_var(
        "RADIOVAR_NS", 
        os.getenv("RADIOVAR_NS"), 
        "Set a namespace prefix for all keys (e.g., 'myapp::key')"
    )
    
    print_header("ADDITIONAL INFORMATION")
    print_colored("GitHub: https://github.com/yourusername/signella", Fore.BLUE)
    print_colored("PyPI: https://pypi.org/project/signella/", Fore.BLUE)
    from signella import __version__
    print_colored(f"Version: {__version__}", Fore.WHITE)

def main():
    parser = argparse.ArgumentParser(description="Signella command line interface")
    parser.add_argument("command", nargs="?", default="help", help="Command to run (currently only 'help' is supported)")
    
    args = parser.parse_args()
    
    if args.command == "help":
        show_help()
    else:
        print_colored(f"Unknown command: {args.command}", Fore.RED)
        print_colored("Currently only the 'help' command is supported.", Fore.YELLOW)
        sys.exit(1)

if __name__ == "__main__":
    main()