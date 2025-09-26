#!/usr/bin/env python3
"""
Ribit 2.0 Performance Optimization Script
Precompiles all Python files to bytecode for faster startup and execution
"""
import os
import py_compile
import sys
from pathlib import Path

def precompile_directory(directory_path: str, recursive: bool = True) -> int:
    """Precompile all Python files in a directory"""
    compiled_count = 0
    directory = Path(directory_path)
    
    if not directory.exists():
        print(f"❌ Directory not found: {directory_path}")
        return 0
    
    # Get all Python files
    if recursive:
        python_files = list(directory.rglob("*.py"))
    else:
        python_files = list(directory.glob("*.py"))
    
    print(f"🔍 Found {len(python_files)} Python files in {directory_path}")
    
    for py_file in python_files:
        try:
            # Skip __pycache__ directories
            if "__pycache__" in str(py_file):
                continue
                
            print(f"⚡ Compiling: {py_file.relative_to(directory)}")
            py_compile.compile(str(py_file), doraise=True)
            compiled_count += 1
            
        except py_compile.PyCompileError as e:
            print(f"❌ Error compiling {py_file}: {e}")
        except Exception as e:
            print(f"❌ Unexpected error with {py_file}: {e}")
    
    return compiled_count

def optimize_ribit_performance():
    """Optimize Ribit 2.0 performance by precompiling all Python files"""
    print("🚀 Ribit 2.0 Performance Optimization Starting...")
    print("=" * 60)
    
    total_compiled = 0
    
    # Core Ribit 2.0 system files
    print("\n🧠 Optimizing Core AI System...")
    core_files = [
        "ribit_2_0/enhanced_emotions.py",
        "ribit_2_0/mock_llm_wrapper.py", 
        "ribit_2_0/enhanced_matrix_integration.py",
        "ribit_2_0/advanced_settings_manager.py",
        "ribit_2_0/enhanced_web_search.py",
        "ribit_2_0/matrix_command_handler.py",
        "ribit_2_0/self_testing_system.py",
        "ribit_2_0/multi_language_system.py",
        "ribit_2_0/conversation_manager.py",
        "ribit_2_0/jina_integration.py",
        "ribit_2_0/matrix_bot.py",
        "ribit_2_0/ros_controller.py",
        "ribit_2_0/agent.py",
        "ribit_2_0/controller.py",
        "ribit_2_0/knowledge_base.py",
        "ribit_2_0/llm_wrapper.py",
        "ribit_2_0/mock_controller.py",
        "ribit_2_0/__init__.py"
    ]
    
    for file_path in core_files:
        if os.path.exists(file_path):
            try:
                print(f"⚡ Compiling core: {file_path}")
                py_compile.compile(file_path, doraise=True)
                total_compiled += 1
            except Exception as e:
                print(f"❌ Error compiling {file_path}: {e}")
        else:
            print(f"⚠️  File not found: {file_path}")
    
    # Example files
    print("\n🧪 Optimizing Example Scripts...")
    example_files = [
        "examples/basic_usage.py",
        "examples/multi_step_tasks.py", 
        "examples/ros_integration.py"
    ]
    
    for file_path in example_files:
        if os.path.exists(file_path):
            try:
                print(f"⚡ Compiling example: {file_path}")
                py_compile.compile(file_path, doraise=True)
                total_compiled += 1
            except Exception as e:
                print(f"❌ Error compiling {file_path}: {e}")
    
    # Main launcher scripts
    print("\n🚀 Optimizing Launcher Scripts...")
    launcher_files = [
        "run_matrix_bot.py",
        "setup.py",
        "optimize_performance.py"
    ]
    
    for file_path in launcher_files:
        if os.path.exists(file_path):
            try:
                print(f"⚡ Compiling launcher: {file_path}")
                py_compile.compile(file_path, doraise=True)
                total_compiled += 1
            except Exception as e:
                print(f"❌ Error compiling {file_path}: {e}")
    
    # Check bytecode files created
    print("\n📊 Performance Optimization Results:")
    print("=" * 60)
    
    pycache_dirs = []
    bytecode_count = 0
    total_size = 0
    
    for root, dirs, files in os.walk("."):
        if "__pycache__" in root:
            pycache_dirs.append(root)
            for file in files:
                if file.endswith(".pyc"):
                    bytecode_count += 1
                    file_path = os.path.join(root, file)
                    total_size += os.path.getsize(file_path)
    
    print(f"✅ Python files compiled: {total_compiled}")
    print(f"✅ Bytecode files created: {bytecode_count}")
    print(f"✅ __pycache__ directories: {len(pycache_dirs)}")
    print(f"✅ Total bytecode size: {total_size / 1024:.1f} KB")
    
    print(f"\n🎯 Performance Benefits:")
    print(f"• Faster startup time (bytecode loading vs source parsing)")
    print(f"• Reduced CPU usage during module imports")
    print(f"• Optimized execution for frequently used modules")
    print(f"• Better performance for Matrix bot commands")
    print(f"• Faster emotional intelligence responses")
    
    print(f"\n🎉 Ribit 2.0 Performance Optimization Complete!")
    print(f"Your AI agent is now running at maximum efficiency! 🤖✨")
    
    return total_compiled, bytecode_count

if __name__ == "__main__":
    try:
        compiled, bytecode = optimize_ribit_performance()
        print(f"\n🏆 SUCCESS: {compiled} files compiled, {bytecode} bytecode files created!")
        sys.exit(0)
    except KeyboardInterrupt:
        print(f"\n⚠️  Optimization interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Optimization failed: {e}")
        sys.exit(1)
