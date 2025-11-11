#!/usr/bin/env python3
"""
Ribit 2.0 - Comprehensive Dependency Checker
=============================================

Checks all required Python modules and provides installation commands
with --break-system-packages flag for missing dependencies.

Usage:
    python3 check_ribit_dependencies.py
    or
    ./check_ribit_dependencies.py
"""

import sys
import importlib
import subprocess

# ANSI color codes
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
MAGENTA = '\033[95m'
BOLD = '\033[1m'
RESET = '\033[0m'

# Complete dependency list with pip package names and import names
DEPENDENCIES = {
    # Matrix Protocol
    'matrix-nio[e2e]': {
        'import_name': 'nio',
        'description': 'Matrix protocol client with E2EE encryption',
        'required': True,
        'test_import': None  # Don't test specific attributes, just import
    },
    
    # DeltaChat
    'deltachat': {
        'import_name': 'deltachat',
        'description': 'DeltaChat messaging library',
        'required': True,
        'test_import': None
    },
    
    # HTTP and Web
    'aiohttp': {
        'import_name': 'aiohttp',
        'description': 'Async HTTP client/server framework',
        'required': True,
        'test_import': None
    },
    'requests': {
        'import_name': 'requests',
        'description': 'HTTP library for Python',
        'required': True,
        'test_import': None
    },
    'beautifulsoup4': {
        'import_name': 'bs4',
        'description': 'Web scraping and HTML parsing',
        'required': True,
        'test_import': None
    },
    'lxml': {
        'import_name': 'lxml',
        'description': 'XML and HTML parser',
        'required': True,
        'test_import': None
    },
    
    # Wikipedia
    'wikipedia-api': {
        'import_name': 'wikipediaapi',
        'description': 'Wikipedia API wrapper',
        'required': True,
        'test_import': None
    },
    
    # Image Processing
    'Pillow': {
        'import_name': 'PIL',
        'description': 'Python Imaging Library',
        'required': True,
        'test_import': None
    },
    
    # File Operations
    'python-magic': {
        'import_name': 'magic',
        'description': 'File type identification',
        'required': True,
        'test_import': None
    },
    'aiofiles': {
        'import_name': 'aiofiles',
        'description': 'Async file I/O operations',
        'required': True,
        'test_import': None
    },
    
    # Database
    'supabase': {
        'import_name': 'supabase',
        'description': 'Supabase client for bridge state management',
        'required': True,
        'test_import': None
    },
    
    # GUI Automation (Optional)
    'pyautogui': {
        'import_name': 'pyautogui',
        'description': 'GUI automation and control',
        'required': False,
        'test_import': None
    },
    'pynput': {
        'import_name': 'pynput',
        'description': 'Keyboard and mouse input control',
        'required': False,
        'test_import': None
    },
    
    # ROS (Optional)
    'rospy': {
        'import_name': 'rospy',
        'description': 'ROS 1 Python client library',
        'required': False,
        'test_import': None
    },
    'rclpy': {
        'import_name': 'rclpy',
        'description': 'ROS 2 Python client library',
        'required': False,
        'test_import': None
    },
}


def check_module(pip_name, info):
    """
    Check if a module is installed and importable.
    
    Args:
        pip_name: Name of the pip package
        info: Dictionary with module information
        
    Returns:
        tuple: (is_installed, error_message)
    """
    import_name = info['import_name']
    test_import = info.get('test_import')
    
    try:
        # Import the module
        module = importlib.import_module(import_name)
        
        # If there's a specific test import, check it
        if test_import:
            parts = test_import.split('.')
            obj = module
            for part in parts[1:]:  # Skip the first part (module name)
                obj = getattr(obj, part)
        
        return True, None
    except ImportError as e:
        return False, str(e)
    except AttributeError as e:
        return False, f"Module imported but missing attribute: {e}"


def print_banner():
    """Print ASCII art banner"""
    banner = f"""
{CYAN}╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║  ██████╗ ██╗██████╗ ██╗████████╗    ██████╗     ██████╗          ║
║  ██╔══██╗██║██╔══██╗██║╚══██╔══╝    ╚════██╗   ██╔═████╗         ║
║  ██████╔╝██║██████╔╝██║   ██║        █████╔╝   ██║██╔██║         ║
║  ██╔══██╗██║██╔══██╗██║   ██║       ██╔═══╝    ████╔╝██║         ║
║  ██║  ██║██║██████╔╝██║   ██║       ███████╗██╗╚██████╔╝         ║
║  ╚═╝  ╚═╝╚═╝╚═════╝ ╚═╝   ╚═╝       ╚══════╝╚═╝ ╚═════╝          ║
║                                                                   ║
║            {MAGENTA}Dependency Checker & Installer{CYAN}                       ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝{RESET}
"""
    print(banner)


def main():
    """Main function to check dependencies and provide installation commands"""
    print_banner()
    
    print(f"{BOLD}{CYAN}Checking Ribit 2.0 Dependencies...{RESET}\n")
    
    # Separate dependencies by type
    required_installed = []
    required_missing = []
    optional_installed = []
    optional_missing = []
    
    # Check each dependency
    for pip_name, info in DEPENDENCIES.items():
        is_required = info['required']
        is_installed, error = check_module(pip_name, info)
        
        # Format the status line
        status_icon = f"{GREEN}✓{RESET}" if is_installed else (f"{RED}✗{RESET}" if is_required else f"{YELLOW}⚠{RESET}")
        req_label = "" if is_required else f" {YELLOW}(optional){RESET}"
        
        print(f"{status_icon} {pip_name:25s} {CYAN}{info['description']}{req_label}{RESET}")
        
        # Categorize the result
        if is_installed:
            if is_required:
                required_installed.append(pip_name)
            else:
                optional_installed.append(pip_name)
        else:
            if is_required:
                required_missing.append(pip_name)
            else:
                optional_missing.append(pip_name)
            
            # Show error details if verbose
            if error and is_required:
                print(f"   {RED}└─ Error: {error[:65]}{RESET}")
    
    # Summary
    print(f"\n{BOLD}{CYAN}{'='*70}{RESET}")
    print(f"{BOLD}{CYAN}Summary{RESET}\n")
    
    total_required = len(required_installed) + len(required_missing)
    total_optional = len(optional_installed) + len(optional_missing)
    
    print(f"Required dependencies:  {GREEN}{len(required_installed)}{RESET}/{total_required} installed")
    print(f"Optional dependencies:  {YELLOW}{len(optional_installed)}{RESET}/{total_optional} installed")
    
    # Installation commands
    if required_missing or optional_missing:
        print(f"\n{BOLD}{YELLOW}{'='*70}{RESET}")
        print(f"{BOLD}{YELLOW}Installation Commands{RESET}\n")
        
        if required_missing:
            print(f"{BOLD}{RED}⚠ REQUIRED Dependencies (MUST install):{RESET}\n")
            
            # Single command for all required
            all_required = ' '.join(f"'{pkg}'" if '[' in pkg else pkg for pkg in required_missing)
            print(f"{CYAN}# Install all required dependencies:{RESET}")
            print(f"{BOLD}pip3 install {all_required} --break-system-packages{RESET}\n")
            
            # Individual commands
            print(f"{CYAN}# Or install individually:{RESET}")
            for pkg in required_missing:
                pkg_formatted = f"'{pkg}'" if '[' in pkg else pkg
                print(f"pip3 install {pkg_formatted} --break-system-packages")
            print()
        
        if optional_missing:
            print(f"{BOLD}{YELLOW}📦 OPTIONAL Dependencies (for full features):{RESET}\n")
            
            # Group by category
            gui_pkgs = [p for p in optional_missing if p in ['pyautogui', 'pynput']]
            ros_pkgs = [p for p in optional_missing if p in ['rospy', 'rclpy']]
            
            if gui_pkgs:
                print(f"{CYAN}# GUI Automation (for desktop control):{RESET}")
                print(f"pip3 install {' '.join(gui_pkgs)} --break-system-packages\n")
            
            if ros_pkgs:
                print(f"{CYAN}# ROS Integration (for robotics):{RESET}")
                print(f"pip3 install {' '.join(ros_pkgs)} --break-system-packages\n")
        
        # Alternative: install from requirements.txt
        print(f"{BOLD}{MAGENTA}💡 Quick Install (All Dependencies):{RESET}\n")
        print(f"{CYAN}# Install everything from requirements.txt:{RESET}")
        print(f"{BOLD}pip3 install -r requirements.txt --break-system-packages{RESET}\n")
        
        # Explanation
        print(f"{BOLD}{CYAN}{'='*70}{RESET}")
        print(f"{BOLD}About --break-system-packages:{RESET}")
        print(f"This flag allows pip to install packages in externally managed")
        print(f"Python environments (like system Python on Ubuntu 23.04+).")
        print(f"It's safe to use for development and testing.\n")
    
    # Final status
    print(f"{BOLD}{CYAN}{'='*70}{RESET}")
    
    if not required_missing and not optional_missing:
        print(f"\n{GREEN}{BOLD}✅ ALL DEPENDENCIES INSTALLED{RESET}")
        print(f"{GREEN}Ribit 2.0 is ready to run!{RESET}\n")
        return 0
    elif not required_missing:
        print(f"\n{YELLOW}{BOLD}✅ ALL REQUIRED DEPENDENCIES INSTALLED{RESET}")
        print(f"{YELLOW}Some optional features are unavailable.{RESET}")
        print(f"{YELLOW}Install optional dependencies above for full functionality.{RESET}\n")
        return 0
    else:
        print(f"\n{RED}{BOLD}❌ MISSING REQUIRED DEPENDENCIES{RESET}")
        print(f"{RED}Please install the required packages using the commands above.{RESET}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
