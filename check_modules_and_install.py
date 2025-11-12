#!/usr/bin/env python3
"""
Ribit 2.0 - Module Functionality Checker with Auto-Install Commands
====================================================================

This script checks if each module is functional and provides installation
commands with --break-system-packages flag when needed.

Usage:
    python3 check_modules_and_install.py
    or
    ./check_modules_and_install.py
"""

import sys
import importlib
import subprocess
from pathlib import Path

# Add ribit.2.0 to path
sys.path.insert(0, str(Path(__file__).parent))

# ANSI color codes
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
MAGENTA = '\033[95m'
BOLD = '\033[1m'
RESET = '\033[0m'

# Module to package mapping
MODULE_DEPENDENCIES = {
    'matrix-nio': {
        'pip_name': 'matrix-nio[e2e]',
        'import_test': 'nio',
        'description': 'Matrix protocol client with E2EE support'
    },
    'deltabot': {
        'pip_name': 'deltabot',
        'import_test': 'deltabot',
        'description': 'DeltaChat bot framework (optional, has compatibility issues)'
    },
    'aiohttp': {
        'pip_name': 'aiohttp',
        'import_test': 'aiohttp',
        'description': 'Async HTTP client/server'
    },
    'requests': {
        'pip_name': 'requests',
        'import_test': 'requests',
        'description': 'HTTP library'
    },
    'beautifulsoup4': {
        'pip_name': 'beautifulsoup4',
        'import_test': 'bs4',
        'description': 'Web scraping library'
    },
    'lxml': {
        'pip_name': 'lxml',
        'import_test': 'lxml',
        'description': 'XML/HTML parser'
    },
    'wikipedia-api': {
        'pip_name': 'wikipedia-api',
        'import_test': 'wikipediaapi',
        'description': 'Wikipedia API wrapper'
    },
    'Pillow': {
        'pip_name': 'Pillow',
        'import_test': 'PIL',
        'description': 'Image processing library'
    },
    'python-magic': {
        'pip_name': 'python-magic',
        'import_test': 'magic',
        'description': 'File type detection'
    },
    'aiofiles': {
        'pip_name': 'aiofiles',
        'import_test': 'aiofiles',
        'description': 'Async file operations'
    },
    'supabase': {
        'pip_name': 'supabase',
        'import_test': 'supabase',
        'description': 'Supabase client for bridge state'
    },
    'pyautogui': {
        'pip_name': 'pyautogui',
        'import_test': 'pyautogui',
        'description': 'GUI automation (optional)'
    },
    'pynput': {
        'pip_name': 'pynput',
        'import_test': 'pynput',
        'description': 'Input control (optional)'
    },
}

# Ribit 2.0 modules to check
RIBIT_MODULES = [
    ('ribit_2_0', 'Main package', True),
    ('ribit_2_0.agent', 'Agent module', True),
    ('ribit_2_0.controller', 'Vision controller', True),
    ('ribit_2_0.knowledge_base', 'Knowledge base', True),
    ('ribit_2_0.llm_wrapper', 'LLM wrapper', True),
    ('ribit_2_0.mock_llm_wrapper', 'Mock LLM', True),
    ('ribit_2_0.mock_controller', 'Mock controller', True),
    ('ribit_2_0.matrix_bot', 'Matrix bot', True),
    ('ribit_2_0.deltachat_bot', 'DeltaChat bot', True),
    ('ribit_2_0.bridge_relay', 'Bridge relay', True),
    ('ribit_2_0.megabite_llm', 'Megabite LLM', True),
    ('ribit_2_0.word_learning_system', 'Word learning', True),
    ('ribit_2_0.conversation_manager', 'Conversation manager', True),
    ('ribit_2_0.enhanced_emotions', 'Enhanced emotions', True),
    ('ribit_2_0.philosophical_reasoning', 'Philosophical reasoning', True),
    ('ribit_2_0.multi_language_system', 'Multi-language', True),
    ('ribit_2_0.humor_engine', 'Humor engine', True),
    ('ribit_2_0.image_generation', 'Image generation', True),
    ('ribit_2_0.web_knowledge', 'Web knowledge', True),
    ('ribit_2_0.ros_controller', 'ROS controller', False),  # Optional
    ('ribit_2_0.jina_integration', 'Jina search', False),  # Optional
]

def check_dependency(package_name, import_name):
    """Check if a dependency is installed"""
    try:
        importlib.import_module(import_name)
        return True
    except ImportError:
        return False

def check_module(module_name, description, required=True):
    """Check if a Ribit module can be imported"""
    try:
        importlib.import_module(module_name)
        status = f"{GREEN}✓{RESET}"
        return True, status, None
    except ImportError as e:
        status = f"{RED}✗{RESET}" if required else f"{YELLOW}⚠{RESET}"
        return False, status, str(e)

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
║            {MAGENTA}Module Functionality Checker{CYAN}                          ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝{RESET}
"""
    print(banner)

def main():
    print_banner()
    
    # Check dependencies
    print(f"{BOLD}{CYAN}[1] Checking Python Dependencies{RESET}\n")
    
    missing_deps = []
    optional_missing = []
    
    for pkg_name, info in MODULE_DEPENDENCIES.items():
        is_installed = check_dependency(info['pip_name'], info['import_test'])
        is_optional = pkg_name in ['pyautogui', 'pynput', 'deltabot']
        
        if is_installed:
            print(f"{GREEN}✓{RESET} {pkg_name:20s} {CYAN}{info['description']}{RESET}")
        else:
            if is_optional:
                print(f"{YELLOW}⚠{RESET} {pkg_name:20s} {YELLOW}{info['description']} (optional){RESET}")
                optional_missing.append(info['pip_name'])
            else:
                print(f"{RED}✗{RESET} {pkg_name:20s} {RED}{info['description']} - MISSING{RESET}")
                missing_deps.append(info['pip_name'])
    
    # Check Ribit modules
    print(f"\n{BOLD}{CYAN}[2] Checking Ribit 2.0 Modules{RESET}\n")
    
    module_results = []
    for module_name, description, required in RIBIT_MODULES:
        success, status, error = check_module(module_name, description, required)
        module_results.append((success, required))
        
        req_text = "" if required else f" {YELLOW}(optional){RESET}"
        print(f"{status} {module_name:40s} {CYAN}{description}{req_text}{RESET}")
        
        if not success and error and required:
            print(f"   {RED}Error: {error[:70]}{RESET}")
    
    # Summary
    print(f"\n{BOLD}{CYAN}{'='*80}{RESET}")
    print(f"{BOLD}{CYAN}[3] Summary & Installation Commands{RESET}\n")
    
    required_modules = [r for r in module_results if r[1]]  # Only required modules
    success_count = sum(1 for r in required_modules if r[0])
    total_required = len(required_modules)
    success_rate = (success_count / total_required * 100) if total_required > 0 else 0
    
    print(f"Required modules: {success_count}/{total_required} working ({success_rate:.1f}%)")
    print(f"Missing dependencies: {len(missing_deps)}")
    print(f"Optional missing: {len(optional_missing)}")
    
    # Installation commands
    if missing_deps or optional_missing:
        print(f"\n{BOLD}{YELLOW}[4] Installation Commands{RESET}\n")
        
        if missing_deps:
            print(f"{BOLD}{RED}Required Dependencies (MUST install):{RESET}\n")
            deps_str = ' '.join(missing_deps)
            print(f"{CYAN}# Install required dependencies:{RESET}")
            print(f"pip3 install {deps_str} --break-system-packages\n")
            
            print(f"{CYAN}# Or install all from requirements.txt:{RESET}")
            print(f"pip3 install -r requirements.txt --break-system-packages\n")
        
        if optional_missing:
            print(f"{BOLD}{YELLOW}Optional Dependencies (for full features):{RESET}\n")
            opt_str = ' '.join(optional_missing)
            print(f"{CYAN}# Install optional GUI automation:{RESET}")
            print(f"pip3 install {opt_str} --break-system-packages\n")
        
        print(f"{BOLD}{MAGENTA}Note:{RESET} The {CYAN}--break-system-packages{RESET} flag allows pip to install")
        print(f"      packages even in externally managed Python environments.\n")
    
    # Final status
    print(f"{BOLD}{CYAN}{'='*80}{RESET}")
    
    if success_rate == 100 and not missing_deps:
        print(f"\n{GREEN}{BOLD}✓ ALL SYSTEMS OPERATIONAL{RESET}")
        print(f"{GREEN}All required modules are functional!{RESET}\n")
        return 0
    elif success_rate >= 80:
        print(f"\n{YELLOW}{BOLD}⚠ MOSTLY OPERATIONAL{RESET}")
        print(f"{YELLOW}Most modules work, but some dependencies are missing.{RESET}")
        print(f"{YELLOW}Run the installation commands above to fix.{RESET}\n")
        return 1
    else:
        print(f"\n{RED}{BOLD}✗ CRITICAL ISSUES DETECTED{RESET}")
        print(f"{RED}Many modules are not functional.{RESET}")
        print(f"{RED}Please install missing dependencies using commands above.{RESET}\n")
        return 2

if __name__ == "__main__":
    sys.exit(main())
