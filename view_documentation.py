#!/usr/bin/env python3
"""
Ribit 2.0 & Megabite Documentation Viewer
==========================================

Interactive documentation viewer for all Ribit 2.0 and Megabite guides.

Usage:
    python3 view_documentation.py
    or
    ./view_documentation.py

Features:
- View architecture documentation (slides)
- Read offline installation guides
- Read download links and ROS installation guides
- Beautiful ASCII art interface
- Interactive menu selection
"""

import webbrowser
import os
import sys
from pathlib import Path

# ANSI color codes for terminal output
GREEN = '\033[92m'
ORANGE = '\033[93m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_banner():
    """Print ASCII art banner for Ribit 2.0 & Megabite"""
    banner = f"""
{GREEN}╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║  ██████╗ ██╗██████╗ ██╗████████╗    ██████╗     ██████╗          ║
║  ██╔══██╗██║██╔══██╗██║╚══██╔══╝    ╚════██╗   ██╔═████╗         ║
║  ██████╔╝██║██████╔╝██║   ██║        █████╔╝   ██║██╔██║         ║
║  ██╔══██╗██║██╔══██╗██║   ██║       ██╔═══╝    ████╔╝██║         ║
║  ██║  ██║██║██████╔╝██║   ██║       ███████╗██╗╚██████╔╝         ║
║  ╚═╝  ╚═╝╚═╝╚═════╝ ╚═╝   ╚═╝       ╚══════╝╚═╝ ╚═════╝          ║
║                                                                   ║
║              {ORANGE}&{GREEN}                                                    ║
║                                                                   ║
║  ███╗   ███╗███████╗ ██████╗  █████╗ ██████╗ ██╗████████╗███████╗║
║  ████╗ ████║██╔════╝██╔════╝ ██╔══██╗██╔══██╗██║╚══██╔══╝██╔════╝║
║  ██╔████╔██║█████╗  ██║  ███╗███████║██████╔╝██║   ██║   █████╗  ║
║  ██║╚██╔╝██║██╔══╝  ██║   ██║██╔══██║██╔══██╗██║   ██║   ██╔══╝  ║
║  ██║ ╚═╝ ██║███████╗╚██████╔╝██║  ██║██████╔╝██║   ██║   ███████╗║
║  ╚═╝     ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚═╝   ╚═╝   ╚══════╝║
║                                                                   ║
║            {CYAN}Documentation Viewer{GREEN}                                     ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝{RESET}
"""
    print(banner)

def print_menu():
    """Print the interactive menu"""
    menu = f"""
{BOLD}{CYAN}Available Documentation:{RESET}

{YELLOW}Architecture & Development:{RESET}
  {GREEN}1.{RESET} Ribit 2.0 & Megabite Architecture (Slides)
     {CYAN}→{RESET} Complete system architecture, module structure, development journey

{YELLOW}Offline Installation:{RESET}
  {GREEN}2.{RESET} Offline Installation Guide
     {CYAN}→{RESET} Complete guide for installing without internet

  {GREEN}3.{RESET} Download Dependencies Script
     {CYAN}→{RESET} How to download all 63 packages (43 MB)

  {GREEN}4.{RESET} Install Offline Script
     {CYAN}→{RESET} How to install from local packages folder

{YELLOW}Package Information:{RESET}
  {GREEN}5.{RESET} Download Links (All Packages)
     {CYAN}→{RESET} Direct PyPI links for all 63 Python packages

  {GREEN}6.{RESET} Manual Download Guide
     {CYAN}→{RESET} Step-by-step instructions for manual download

  {GREEN}7.{RESET} ROS Installation Guide
     {CYAN}→{RESET} ROS 1 (Noetic) and ROS 2 (Humble) installation

{YELLOW}Other:{RESET}
  {GREEN}8.{RESET} View All Files
     {CYAN}→{RESET} Show all available documentation files

  {GREEN}0.{RESET} Exit

{BOLD}Enter your choice (0-8):{RESET} """
    return menu

def get_script_dir():
    """Get the directory where this script is located"""
    return Path(__file__).parent.absolute()

def open_in_browser(file_path):
    """Open a file in the default web browser"""
    try:
        file_url = file_path.as_uri()
        print(f"\n{CYAN}[INFO]{RESET} Opening in your default browser...")
        print(f"{CYAN}[INFO]{RESET} File: {file_path.name}")
        webbrowser.open(file_url)
        print(f"{GREEN}[SUCCESS]{RESET} Opened successfully!")
        return True
    except Exception as e:
        print(f"{RED}[ERROR]{RESET} Failed to open file: {e}")
        return False

def open_in_pager(file_path):
    """Open a text file in a pager (less/more) or print to terminal"""
    try:
        # Try to use less first, then more, then just cat
        if os.system(f'which less > /dev/null 2>&1') == 0:
            os.system(f'less "{file_path}"')
        elif os.system(f'which more > /dev/null 2>&1') == 0:
            os.system(f'more "{file_path}"')
        else:
            # Just print the file
            print(f"\n{CYAN}{'='*70}{RESET}")
            print(file_path.read_text())
            print(f"{CYAN}{'='*70}{RESET}\n")
        return True
    except Exception as e:
        print(f"{RED}[ERROR]{RESET} Failed to open file: {e}")
        return False

def view_architecture_slides():
    """View the architecture documentation slides"""
    script_dir = get_script_dir()
    presentation_dir = script_dir / "ribit_megabite_architecture_docs"
    
    if not presentation_dir.exists():
        print(f"\n{RED}[ERROR]{RESET} Architecture slides not found at:")
        print(f"        {presentation_dir}")
        print(f"\n{YELLOW}[INFO]{RESET} This is the slide-based architecture documentation.")
        print(f"        It may not be included in your clone.")
        return False
    
    title_slide = presentation_dir / "title.html"
    if not title_slide.exists():
        print(f"\n{RED}[ERROR]{RESET} Title slide not found.")
        return False
    
    return open_in_browser(title_slide)

def view_markdown_file(filename, description):
    """View a markdown file"""
    script_dir = get_script_dir()
    file_path = script_dir / filename
    
    if not file_path.exists():
        print(f"\n{RED}[ERROR]{RESET} File not found: {filename}")
        return False
    
    print(f"\n{CYAN}[INFO]{RESET} {description}")
    print(f"{CYAN}[INFO]{RESET} File: {filename}")
    print(f"{CYAN}[INFO]{RESET} Size: {file_path.stat().st_size / 1024:.1f} KB")
    
    # Ask user how to view
    print(f"\n{YELLOW}How would you like to view this file?{RESET}")
    print(f"  {GREEN}1.{RESET} In browser (formatted)")
    print(f"  {GREEN}2.{RESET} In terminal (text)")
    print(f"  {GREEN}3.{RESET} Cancel")
    
    choice = input(f"\n{BOLD}Choose (1-3):{RESET} ").strip()
    
    if choice == '1':
        return open_in_browser(file_path)
    elif choice == '2':
        return open_in_pager(file_path)
    else:
        print(f"{YELLOW}[CANCELLED]{RESET}")
        return False

def view_script_file(filename, description):
    """View a script file"""
    script_dir = get_script_dir()
    file_path = script_dir / filename
    
    if not file_path.exists():
        print(f"\n{RED}[ERROR]{RESET} File not found: {filename}")
        return False
    
    print(f"\n{CYAN}[INFO]{RESET} {description}")
    print(f"{CYAN}[INFO]{RESET} File: {filename}")
    print(f"{CYAN}[INFO]{RESET} This is an executable script.")
    
    # Show how to use it
    print(f"\n{YELLOW}Usage:{RESET}")
    print(f"  {CYAN}./{filename}{RESET}")
    print(f"  or")
    print(f"  {CYAN}bash {filename}{RESET}")
    
    # Ask if user wants to view the source
    choice = input(f"\n{BOLD}View source code? (y/n):{RESET} ").strip().lower()
    
    if choice == 'y':
        return open_in_pager(file_path)
    else:
        print(f"{YELLOW}[CANCELLED]{RESET}")
        return False

def list_all_files():
    """List all available documentation files"""
    script_dir = get_script_dir()
    
    print(f"\n{CYAN}{'='*70}{RESET}")
    print(f"{BOLD}All Available Documentation Files:{RESET}")
    print(f"{CYAN}{'='*70}{RESET}\n")
    
    # Define file categories
    categories = {
        "Architecture & Slides": [
            "ribit_megabite_architecture_docs/"
        ],
        "Offline Installation": [
            "OFFLINE_INSTALLATION.md",
            "download_dependencies.sh",
            "install_offline.sh",
            "requirements-offline.txt"
        ],
        "Package Information": [
            "DOWNLOAD_LINKS.md",
            "MANUAL_DOWNLOAD_GUIDE.md",
            "ROS_INSTALLATION.md"
        ],
        "Setup & Configuration": [
            "setup_credentials.py",
            "setup_vendor.py",
            "check_ribit_dependencies.py"
        ],
        "Other Documentation": [
            "README.md",
            "requirements.txt"
        ]
    }
    
    for category, files in categories.items():
        print(f"{YELLOW}{category}:{RESET}")
        for filename in files:
            file_path = script_dir / filename
            if file_path.exists():
                if file_path.is_dir():
                    count = len(list(file_path.glob('*.html')))
                    print(f"  {GREEN}✓{RESET} {filename} ({count} slides)")
                else:
                    size = file_path.stat().st_size / 1024
                    print(f"  {GREEN}✓{RESET} {filename} ({size:.1f} KB)")
            else:
                print(f"  {RED}✗{RESET} {filename} (not found)")
        print()
    
    print(f"{CYAN}{'='*70}{RESET}\n")

def main():
    """Main function"""
    print_banner()
    
    while True:
        print(print_menu(), end='')
        choice = input().strip()
        
        if choice == '0':
            print(f"\n{GREEN}Thank you for using Ribit 2.0 Documentation Viewer!{RESET}\n")
            sys.exit(0)
        
        elif choice == '1':
            view_architecture_slides()
        
        elif choice == '2':
            view_markdown_file(
                "OFFLINE_INSTALLATION.md",
                "Complete guide for installing Ribit 2.0 without internet"
            )
        
        elif choice == '3':
            view_script_file(
                "download_dependencies.sh",
                "Script to download all 63 packages (43 MB) from PyPI"
            )
        
        elif choice == '4':
            view_script_file(
                "install_offline.sh",
                "Script to install all dependencies from local packages folder"
            )
        
        elif choice == '5':
            view_markdown_file(
                "DOWNLOAD_LINKS.md",
                "Direct PyPI links for all 63 Python packages + ROS repositories"
            )
        
        elif choice == '6':
            view_markdown_file(
                "MANUAL_DOWNLOAD_GUIDE.md",
                "Step-by-step instructions for manual download and copy"
            )
        
        elif choice == '7':
            view_markdown_file(
                "ROS_INSTALLATION.md",
                "Complete guide for ROS 1 (Noetic) and ROS 2 (Humble) installation"
            )
        
        elif choice == '8':
            list_all_files()
        
        else:
            print(f"\n{RED}[ERROR]{RESET} Invalid choice. Please enter a number from 0-8.\n")
        
        # Wait for user to press Enter before showing menu again
        if choice in ['1', '2', '3', '4', '5', '6', '7', '8']:
            input(f"\n{CYAN}Press Enter to continue...{RESET}")
            print("\n" * 2)  # Clear screen a bit

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}[INTERRUPTED]{RESET} Exiting...\n")
        sys.exit(0)
