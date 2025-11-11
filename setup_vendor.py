#!/usr/bin/env python3
"""
Ribit 2.0 - Vendor Dependencies Setup
This script extracts essential packages to a vendor/ folder for direct import
"""

import os
import sys
import zipfile
import tarfile
import shutil
from pathlib import Path

# Colors
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
CYAN = '\033[0;36m'
RED = '\033[0;31m'
BOLD = '\033[1m'
RESET = '\033[0m'

def print_header():
    print(f"{CYAN}╔═══════════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{CYAN}║                                                                   ║{RESET}")
    print(f"{CYAN}║  {BOLD}Ribit 2.0 - Vendor Dependencies Setup{RESET}{CYAN}                        ║{RESET}")
    print(f"{CYAN}║                                                                   ║{RESET}")
    print(f"{CYAN}╚═══════════════════════════════════════════════════════════════════╝{RESET}")
    print()

def extract_package(package_file, vendor_dir):
    """Extract a package to the vendor directory"""
    package_path = Path(package_file)
    
    try:
        if package_path.suffix == '.whl':
            # Wheel files are just zip files
            with zipfile.ZipFile(package_path, 'r') as zip_ref:
                # Extract only the package code, not metadata
                for member in zip_ref.namelist():
                    if not member.startswith(('dist-info/', 'egg-info/', '__pycache__/')):
                        zip_ref.extract(member, vendor_dir)
            return True
        elif package_path.suffix == '.gz' and '.tar' in package_path.name:
            # Tar.gz files
            with tarfile.open(package_path, 'r:gz') as tar_ref:
                # Find the package directory inside
                members = tar_ref.getmembers()
                if members:
                    # Extract to temp, then move the package folder
                    temp_dir = vendor_dir / 'temp_extract'
                    temp_dir.mkdir(exist_ok=True)
                    tar_ref.extractall(temp_dir)
                    
                    # Find and move the actual package
                    for item in temp_dir.iterdir():
                        if item.is_dir():
                            for subitem in item.iterdir():
                                if subitem.is_dir() and not subitem.name.endswith('.egg-info'):
                                    shutil.move(str(subitem), str(vendor_dir))
                    
                    # Clean up temp
                    shutil.rmtree(temp_dir)
            return True
    except Exception as e:
        print(f"{RED}  ✗ Error extracting {package_path.name}: {e}{RESET}")
        return False
    
    return False

def main():
    print_header()
    
    # Check if packages directory exists
    packages_dir = Path('packages')
    if not packages_dir.exists():
        print(f"{RED}❌ Error: packages/ directory not found{RESET}")
        print(f"{YELLOW}Please run ./download_dependencies.sh first{RESET}")
        sys.exit(1)
    
    # Create vendor directory
    vendor_dir = Path('vendor')
    print(f"{YELLOW}📦 Creating vendor directory...{RESET}")
    vendor_dir.mkdir(exist_ok=True)
    
    # Essential packages to vendor (lightweight, pure Python preferred)
    essential_packages = [
        'aiofiles',
        'beautifulsoup4',
        'requests',
        'wikipedia',
        # Add more as needed
    ]
    
    print(f"{CYAN}📥 Extracting essential packages to vendor/...{RESET}")
    print()
    
    extracted_count = 0
    for package_file in packages_dir.glob('*.whl'):
        # Check if this is an essential package
        package_name = package_file.stem.split('-')[0].lower()
        if any(essential in package_name for essential in essential_packages):
            print(f"  {CYAN}→{RESET} Extracting {package_file.name}...")
            if extract_package(package_file, vendor_dir):
                extracted_count += 1
                print(f"    {GREEN}✓{RESET} Done")
            else:
                print(f"    {RED}✗{RESET} Failed")
    
    # Create __init__.py to make it a package
    (vendor_dir / '__init__.py').write_text('# Vendored dependencies\n')
    
    print()
    print(f"{GREEN}✅ Vendor setup complete!{RESET}")
    print()
    print(f"{BOLD}📊 Summary:{RESET}")
    print(f"  Packages vendored: {CYAN}{extracted_count}{RESET}")
    print(f"  Location: {CYAN}vendor/{RESET}")
    print()
    print(f"{GREEN}{BOLD}Usage:{RESET}")
    print(f"  Add to your Python code:")
    print(f"  {CYAN}import sys{RESET}")
    print(f"  {CYAN}sys.path.insert(0, 'vendor'){RESET}")
    print()

if __name__ == '__main__':
    main()
