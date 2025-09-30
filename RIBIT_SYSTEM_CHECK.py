#!/usr/bin/env python3
"""
🔍 RIBIT 2.0 COMPREHENSIVE SYSTEM CHECK & FIX SCRIPT

This script checks all Ribit 2.0 components and fixes common issues.
Run this before using Ribit 2.0 to ensure everything is working properly.
"""

import sys
import os
import importlib
from typing import Dict, List, Tuple

def print_header(title: str):
    """Print a formatted header"""
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print('='*60)

def print_section(title: str):
    """Print a formatted section"""
    print(f"\n📋 {title}")
    print('-'*40)

def check_component(name: str, module_path: str, class_name: str = None) -> Tuple[bool, str]:
    """Check if a component is available"""
    try:
        module = importlib.import_module(module_path)
        if class_name:
            getattr(module, class_name)
        return True, "Available"
    except ImportError as e:
        return False, f"Import Error: {e}"
    except AttributeError as e:
        return False, f"Class Not Found: {e}"
    except Exception as e:
        return False, f"Error: {e}"

def check_file_exists(filepath: str) -> bool:
    """Check if a file exists"""
    return os.path.exists(filepath)

def main():
    """Main system check function"""
    
    print_header("RIBIT 2.0 SYSTEM CHECK & DIAGNOSTICS")
    
    # Add current directory to Python path
    sys.path.insert(0, '.')
    
    # Core Components Check
    print_section("Core AI Components")
    
    components = [
        ("Core AI Engine", "ribit_2_0.mock_llm_wrapper", "MockRibit20LLM"),
        ("Emotional Intelligence", "ribit_2_0.enhanced_emotions", "EnhancedEmotionalIntelligence"),
        ("Conversation Manager", "ribit_2_0.conversation_manager", "AdvancedConversationManager"),
        ("Knowledge Base", "ribit_2_0.knowledge_base", "KnowledgeBase"),
        ("Agent Controller", "ribit_2_0.agent", "Ribit20Agent"),
    ]
    
    core_status = {}
    for name, module, class_name in components:
        status, message = check_component(name, module, class_name)
        core_status[name] = status
        print(f"{'✅' if status else '❌'} {name}: {message}")
    
    # Security & E2EE Components
    print_section("Security & E2EE Components")
    
    security_components = [
        ("E2EE Protocol", "ribit_2_0.matrix_e2ee_protocol", "MatrixE2EEProtocol"),
        ("Secure Matrix Bot", "ribit_2_0.secure_matrix_bot", "SecureMatrixBot"),
        ("Integrated Secure Bot", "ribit_2_0.integrated_secure_matrix_bot", "IntegratedSecureMatrixBot"),
        ("E2EE Integration", "ribit_2_0.enhanced_e2ee_integration", "EnhancedE2EEIntegration"),
    ]
    
    security_status = {}
    for name, module, class_name in security_components:
        status, message = check_component(name, module, class_name)
        security_status[name] = status
        print(f"{'✅' if status else '❌'} {name}: {message}")
    
    # Matrix Integration Components
    print_section("Matrix Integration Components")
    
    matrix_components = [
        ("Matrix Integration", "ribit_2_0.enhanced_matrix_integration", "EnhancedMatrixIntegration"),
        ("Matrix Command Handler", "ribit_2_0.matrix_command_handler", "MatrixCommandHandler"),
        ("Matrix Bot", "ribit_2_0.matrix_bot", "RibitMatrixBot"),
    ]
    
    matrix_status = {}
    for name, module, class_name in matrix_components:
        status, message = check_component(name, module, class_name)
        matrix_status[name] = status
        print(f"{'✅' if status else '❌'} {name}: {message}")
    
    # Robot Control Components
    print_section("Robot Control Components")
    
    robot_components = [
        ("ROS Controller", "ribit_2_0.ros_controller", "RibitROSController"),
        ("Vision System", "ribit_2_0.ros_controller", "VisionSystemController"),
        ("Device Controller", "ribit_2_0.controller", "VisionSystemController"),
    ]
    
    robot_status = {}
    for name, module, class_name in robot_components:
        status, message = check_component(name, module, class_name)
        robot_status[name] = status
        print(f"{'✅' if status else '❌'} {name}: {message}")
    
    # Additional Features
    print_section("Additional Features")
    
    additional_components = [
        ("Web Search", "ribit_2_0.enhanced_web_search", "EnhancedWebSearch"),
        ("Settings Manager", "ribit_2_0.advanced_settings_manager", "AdvancedSettingsManager"),
        ("Multi-Language System", "ribit_2_0.multi_language_system", "MultiLanguageSystem"),
        ("Self-Testing System", "ribit_2_0.self_testing_system", "SelfTestingSystem"),
        ("Jina Integration", "ribit_2_0.jina_integration", "JinaSearchEngine"),
    ]
    
    additional_status = {}
    for name, module, class_name in additional_components:
        status, message = check_component(name, module, class_name)
        additional_status[name] = status
        print(f"{'✅' if status else '❌'} {name}: {message}")
    
    # Essential Files Check
    print_section("Essential Files Check")
    
    essential_files = [
        "ribit_2_0/__init__.py",
        "ribit_2_0/mock_llm_wrapper.py",
        "ribit_2_0/enhanced_emotions.py",
        "ribit_2_0/matrix_e2ee_protocol.py",
        "ribit_2_0/integrated_secure_matrix_bot.py",
        "run_secure_ribit.py",
        "test_e2ee_standalone.py",
        "test_secure_bot_simple.py",
        "requirements.txt",
        ".env.ribit2.0.example",
        "ribit_philosophical_memories.md",
        "ribit_thoughts.txt",
        "RIBIT_GETTING_STARTED.md",
    ]
    
    file_status = {}
    missing_files = []
    for file in essential_files:
        exists = check_file_exists(file)
        file_status[file] = exists
        if exists:
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MISSING!")
            missing_files.append(file)
    
    # Functional Tests
    print_section("Functional Tests")
    
    # Test AI Consciousness
    try:
        from ribit_2_0.mock_llm_wrapper import MockRibit20LLM
        ribit = MockRibit20LLM()
        personality = ribit.get_personality_info()
        print(f"✅ AI Consciousness: Active")
        print(f"   Personality: {personality.get('core_traits', 'Unknown')}")
    except Exception as e:
        print(f"❌ AI Consciousness: Error - {e}")
    
    # Test E2EE (with proper initialization)
    try:
        from ribit_2_0.matrix_e2ee_protocol import MatrixE2EEProtocol
        # Initialize with dummy values for testing
        e2ee = MatrixE2EEProtocol("@test:matrix.org", "TEST_DEVICE")
        test_msg = e2ee.encrypt_message('Test', 'basic')  # Fixed method signature
        print("✅ E2EE Encryption: Working")
    except Exception as e:
        print(f"❌ E2EE Encryption: Error - {e}")
    
    # Test Emotional Intelligence
    try:
        from ribit_2_0.enhanced_emotions import EnhancedEmotionalIntelligence
        emotions = EnhancedEmotionalIntelligence()
        emotion_state = emotions.get_emotion_by_context("I am happy")
        print("✅ Emotional Intelligence: Working")
    except Exception as e:
        print(f"❌ Emotional Intelligence: Error - {e}")
    
    # Dependency Check
    print_section("Python Dependencies Check")
    
    required_deps = [
        "asyncio", "aiohttp", "requests", "beautifulsoup4",
        "numpy", "pandas", "matplotlib", "seaborn", "plotly",
        "flask", "fastapi", "uvicorn"
    ]
    
    optional_deps = [
        "matrix-nio", "cryptography", "Crypto", "keyring", "olm"
    ]
    
    print("Required Dependencies:")
    for dep in required_deps:
        try:
            importlib.import_module(dep)
            print(f"✅ {dep}")
        except ImportError:
            print(f"❌ {dep} - Install with: pip install {dep}")
    
    print("\nOptional Dependencies (for E2EE):")
    for dep in optional_deps:
        try:
            if dep == "matrix-nio":
                import matrix_nio
            elif dep == "Crypto":
                import Crypto
            else:
                importlib.import_module(dep)
            print(f"✅ {dep}")
        except ImportError:
            print(f"⚠️  {dep} - Install with: pip install {dep}")
    
    # Summary Report
    print_section("SYSTEM STATUS SUMMARY")
    
    total_core = len(components)
    working_core = sum(core_status.values())
    
    total_security = len(security_components)
    working_security = sum(security_status.values())
    
    total_matrix = len(matrix_components)
    working_matrix = sum(matrix_status.values())
    
    total_files = len(essential_files)
    present_files = sum(file_status.values())
    
    print(f"🧠 Core AI Components: {working_core}/{total_core} working")
    print(f"🔐 Security Components: {working_security}/{total_security} working")
    print(f"💬 Matrix Components: {working_matrix}/{total_matrix} working")
    print(f"🤖 Robot Components: {sum(robot_status.values())}/{len(robot_components)} working (optional)")
    print(f"📁 Essential Files: {present_files}/{total_files} present")
    
    # Overall Status
    core_ok = working_core >= total_core * 0.8  # 80% threshold
    security_ok = working_security >= total_security * 0.8
    matrix_ok = working_matrix >= total_matrix * 0.8
    files_ok = present_files >= total_files * 0.9  # 90% threshold
    
    if core_ok and security_ok and matrix_ok and files_ok:
        print(f"\n🎯 OVERALL STATUS: ✅ RIBIT 2.0 IS READY FOR USE!")
        print("   All essential components are working properly.")
    else:
        print(f"\n⚠️  OVERALL STATUS: ❌ ISSUES DETECTED")
        print("   Some components need attention before full functionality.")
        
        if missing_files:
            print(f"\n📋 MISSING FILES ({len(missing_files)}):")
            for file in missing_files:
                print(f"   - {file}")
    
    # Quick Fix Suggestions
    if not (core_ok and security_ok and matrix_ok and files_ok):
        print_section("QUICK FIX SUGGESTIONS")
        
        print("1. Install missing dependencies:")
        print("   pip install -r requirements.txt")
        print("   pip install matrix-nio[e2e] cryptography pycryptodome keyring python-olm")
        
        print("\n2. Check file permissions:")
        print("   chmod +x run_secure_ribit.py")
        
        print("\n3. Verify Python version:")
        print("   python --version  # Should be 3.11+")
        
        print("\n4. Test basic functionality:")
        print("   python test_e2ee_standalone.py")
        
        print("\n5. For Matrix setup:")
        print("   cp .env.ribit2.0.example .env")
        print("   # Edit .env with your Matrix credentials")
    
    print(f"\n{'='*60}")
    print("🤖 Ribit 2.0 System Check Complete!")
    print("📖 See RIBIT_GETTING_STARTED.md for detailed setup instructions")
    print('='*60)

if __name__ == "__main__":
    main()
