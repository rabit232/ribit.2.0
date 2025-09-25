#!/usr/bin/env python3
"""
Self-Testing and Debugging System for Ribit 2.0

This module provides comprehensive self-testing, debugging, and automatic
code improvement capabilities for continuous system validation and enhancement.
"""

import ast
import sys
import subprocess
import traceback
import tempfile
import os
import json
import time
import re
from typing import Dict, List, Tuple, Any, Optional, Union
from dataclasses import dataclass
from datetime import datetime
import logging
from pathlib import Path

@dataclass
class TestResult:
    """Result of a test execution."""
    test_name: str
    passed: bool
    execution_time: float
    output: str
    error_message: Optional[str] = None
    suggestions: List[str] = None
    code_quality_score: float = 0.0

@dataclass
class CodeAnalysis:
    """Analysis result for code quality and issues."""
    syntax_valid: bool
    complexity_score: float
    security_issues: List[str]
    performance_issues: List[str]
    style_issues: List[str]
    suggestions: List[str]
    overall_score: float

class SelfTestingSystem:
    """
    Advanced self-testing and debugging system with automatic improvement capabilities.
    
    Provides comprehensive code validation, testing, debugging, and automatic
    improvement suggestions for continuous system enhancement.
    """
    
    def __init__(self, emotional_ai=None):
        """Initialize the self-testing system."""
        self.emotional_ai = emotional_ai
        self.test_history = []
        self.code_cache = {}
        self.improvement_suggestions = []
        self.performance_metrics = {}
        
        # Configure logging
        self.logger = logging.getLogger("SelfTestingSystem")
        self.logger.setLevel(logging.INFO)
        
        # Test categories and their weights
        self.test_categories = {
            "syntax": 0.3,
            "functionality": 0.4,
            "performance": 0.2,
            "security": 0.1
        }
        
        # Code quality metrics
        self.quality_thresholds = {
            "complexity": 10,  # Maximum cyclomatic complexity
            "line_length": 120,  # Maximum line length
            "function_length": 50,  # Maximum function length
            "nesting_depth": 4  # Maximum nesting depth
        }
    
    def run_comprehensive_test(self, code: str, language: str = "python", 
                             test_type: str = "full") -> Dict[str, Any]:
        """
        Run comprehensive testing on code with automatic improvement suggestions.
        
        Args:
            code: Code to test
            language: Programming language
            test_type: Type of test (syntax, functionality, performance, full)
            
        Returns:
            Comprehensive test results with improvement suggestions
        """
        start_time = time.time()
        
        # Express emotional state about testing
        if self.emotional_ai:
            emotion_context = f"testing_{language}_code"
            emotion = self.emotional_ai.get_emotion_by_context(
                "systematic testing and validation", emotion_context, 0.7
            )
            emotional_state = self.emotional_ai.express_emotion(emotion, emotion_context, 0.7)
            self.logger.info(f"Testing with emotion: {emotion} - {emotional_state['description']}")
        
        results = {
            "language": language,
            "test_type": test_type,
            "timestamp": datetime.now().isoformat(),
            "tests_run": [],
            "overall_score": 0.0,
            "passed": False,
            "execution_time": 0.0,
            "improvements": [],
            "emotional_state": emotional_state if self.emotional_ai else None
        }
        
        try:
            # Run tests based on language
            if language.lower() == "python":
                results.update(self._test_python_code(code, test_type))
            elif language.lower() == "javascript":
                results.update(self._test_javascript_code(code, test_type))
            elif language.lower() == "rust":
                results.update(self._test_rust_code(code, test_type))
            elif language.lower() == "cpp" or language.lower() == "c++":
                results.update(self._test_cpp_code(code, test_type))
            elif language.lower() == "java":
                results.update(self._test_java_code(code, test_type))
            elif language.lower() == "go":
                results.update(self._test_go_code(code, test_type))
            else:
                results.update(self._test_generic_code(code, language, test_type))
            
            # Calculate overall score
            results["overall_score"] = self._calculate_overall_score(results["tests_run"])
            results["passed"] = results["overall_score"] >= 0.7
            
            # Generate improvement suggestions
            results["improvements"] = self._generate_improvements(results, code, language)
            
            # Apply automatic fixes if possible
            if results["overall_score"] < 0.8:
                fixed_code = self._attempt_automatic_fixes(code, language, results)
                if fixed_code != code:
                    results["auto_fixed_code"] = fixed_code
                    results["auto_fix_applied"] = True
                    
                    # Re-test the fixed code
                    retest_results = self.run_comprehensive_test(fixed_code, language, test_type)
                    if retest_results["overall_score"] > results["overall_score"]:
                        results["improvement_successful"] = True
                        results["improved_score"] = retest_results["overall_score"]
        
        except Exception as e:
            self.logger.error(f"Testing failed: {str(e)}")
            results["error"] = str(e)
            results["passed"] = False
            
            # Express frustration but determination
            if self.emotional_ai:
                emotion = self.emotional_ai.get_emotion_by_context(
                    "testing failure but determined to fix", "debugging", 0.8
                )
                emotional_state = self.emotional_ai.express_emotion(emotion, "debugging", 0.8)
                results["emotional_response"] = emotional_state
        
        results["execution_time"] = time.time() - start_time
        self.test_history.append(results)
        
        return results
    
    def _test_python_code(self, code: str, test_type: str) -> Dict[str, Any]:
        """Test Python code comprehensively."""
        tests_run = []
        
        # Syntax validation
        syntax_result = self._test_python_syntax(code)
        tests_run.append(syntax_result)
        
        if test_type in ["full", "functionality"] and syntax_result.passed:
            # Functionality testing
            func_result = self._test_python_functionality(code)
            tests_run.append(func_result)
            
            # Import testing
            import_result = self._test_python_imports(code)
            tests_run.append(import_result)
        
        if test_type in ["full", "performance"]:
            # Performance analysis
            perf_result = self._test_python_performance(code)
            tests_run.append(perf_result)
        
        if test_type in ["full", "security"]:
            # Security analysis
            security_result = self._test_python_security(code)
            tests_run.append(security_result)
        
        # Code quality analysis
        quality_result = self._analyze_python_quality(code)
        tests_run.append(quality_result)
        
        return {"tests_run": tests_run}
    
    def _test_python_syntax(self, code: str) -> TestResult:
        """Test Python syntax validity."""
        start_time = time.time()
        
        try:
            ast.parse(code)
            return TestResult(
                test_name="Python Syntax Validation",
                passed=True,
                execution_time=time.time() - start_time,
                output="Syntax is valid",
                code_quality_score=1.0
            )
        except SyntaxError as e:
            suggestions = [
                f"Fix syntax error at line {e.lineno}: {e.msg}",
                "Check for missing parentheses, brackets, or quotes",
                "Verify proper indentation"
            ]
            return TestResult(
                test_name="Python Syntax Validation",
                passed=False,
                execution_time=time.time() - start_time,
                output="Syntax error detected",
                error_message=str(e),
                suggestions=suggestions,
                code_quality_score=0.0
            )
    
    def _test_python_functionality(self, code: str) -> TestResult:
        """Test Python code functionality by execution."""
        start_time = time.time()
        
        try:
            # Create a temporary file for execution
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            # Execute the code
            result = subprocess.run(
                [sys.executable, temp_file],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Clean up
            os.unlink(temp_file)
            
            if result.returncode == 0:
                return TestResult(
                    test_name="Python Functionality Test",
                    passed=True,
                    execution_time=time.time() - start_time,
                    output=result.stdout,
                    code_quality_score=0.9
                )
            else:
                suggestions = [
                    "Check for runtime errors in the code",
                    "Verify all variables are defined before use",
                    "Add error handling for potential exceptions"
                ]
                return TestResult(
                    test_name="Python Functionality Test",
                    passed=False,
                    execution_time=time.time() - start_time,
                    output=result.stdout,
                    error_message=result.stderr,
                    suggestions=suggestions,
                    code_quality_score=0.3
                )
        
        except subprocess.TimeoutExpired:
            return TestResult(
                test_name="Python Functionality Test",
                passed=False,
                execution_time=time.time() - start_time,
                output="",
                error_message="Code execution timed out",
                suggestions=["Optimize code for better performance", "Check for infinite loops"],
                code_quality_score=0.2
            )
        except Exception as e:
            return TestResult(
                test_name="Python Functionality Test",
                passed=False,
                execution_time=time.time() - start_time,
                output="",
                error_message=str(e),
                suggestions=["Review code for potential issues"],
                code_quality_score=0.1
            )
    
    def _test_python_imports(self, code: str) -> TestResult:
        """Test Python import statements."""
        start_time = time.time()
        
        # Extract import statements
        import_lines = [line.strip() for line in code.split('\n') 
                       if line.strip().startswith(('import ', 'from '))]
        
        failed_imports = []
        suggestions = []
        
        for import_line in import_lines:
            try:
                exec(import_line)
            except ImportError as e:
                failed_imports.append(f"{import_line}: {str(e)}")
                suggestions.append(f"Install missing package: {import_line.split()[-1]}")
            except Exception as e:
                failed_imports.append(f"{import_line}: {str(e)}")
        
        if not failed_imports:
            return TestResult(
                test_name="Python Import Validation",
                passed=True,
                execution_time=time.time() - start_time,
                output=f"All {len(import_lines)} imports successful",
                code_quality_score=1.0
            )
        else:
            return TestResult(
                test_name="Python Import Validation",
                passed=False,
                execution_time=time.time() - start_time,
                output=f"{len(failed_imports)} imports failed",
                error_message="; ".join(failed_imports),
                suggestions=suggestions,
                code_quality_score=max(0.0, 1.0 - len(failed_imports) / len(import_lines))
            )
    
    def _test_python_performance(self, code: str) -> TestResult:
        """Analyze Python code performance characteristics."""
        start_time = time.time()
        
        performance_issues = []
        suggestions = []
        score = 1.0
        
        # Check for common performance issues
        if 'for' in code and 'range(len(' in code:
            performance_issues.append("Using range(len()) instead of direct iteration")
            suggestions.append("Use 'for item in list' instead of 'for i in range(len(list))'")
            score -= 0.2
        
        if code.count('append') > 10:
            performance_issues.append("Multiple append operations detected")
            suggestions.append("Consider using list comprehension or extend() for better performance")
            score -= 0.1
        
        if '+ str(' in code or 'str(' in code and '+' in code:
            performance_issues.append("String concatenation in loop detected")
            suggestions.append("Use f-strings or join() for string concatenation")
            score -= 0.1
        
        # Check for nested loops
        nested_loops = code.count('for') + code.count('while')
        if nested_loops > 3:
            performance_issues.append(f"High number of loops detected ({nested_loops})")
            suggestions.append("Consider optimizing nested loops or using more efficient algorithms")
            score -= 0.2
        
        return TestResult(
            test_name="Python Performance Analysis",
            passed=len(performance_issues) == 0,
            execution_time=time.time() - start_time,
            output=f"Performance issues found: {len(performance_issues)}",
            error_message="; ".join(performance_issues) if performance_issues else None,
            suggestions=suggestions,
            code_quality_score=max(0.0, score)
        )
    
    def _test_python_security(self, code: str) -> TestResult:
        """Analyze Python code for security issues."""
        start_time = time.time()
        
        security_issues = []
        suggestions = []
        score = 1.0
        
        # Check for dangerous functions
        dangerous_functions = ['eval', 'exec', 'compile', '__import__']
        for func in dangerous_functions:
            if func in code:
                security_issues.append(f"Dangerous function '{func}' detected")
                suggestions.append(f"Avoid using '{func}' or ensure input validation")
                score -= 0.3
        
        # Check for SQL injection patterns
        if 'execute(' in code and '+' in code:
            security_issues.append("Potential SQL injection vulnerability")
            suggestions.append("Use parameterized queries instead of string concatenation")
            score -= 0.4
        
        # Check for file operations without validation
        if 'open(' in code and 'input(' in code:
            security_issues.append("File operation with user input detected")
            suggestions.append("Validate and sanitize file paths from user input")
            score -= 0.2
        
        # Check for pickle usage
        if 'pickle.load' in code:
            security_issues.append("Pickle deserialization detected")
            suggestions.append("Avoid pickle with untrusted data, use JSON instead")
            score -= 0.3
        
        return TestResult(
            test_name="Python Security Analysis",
            passed=len(security_issues) == 0,
            execution_time=time.time() - start_time,
            output=f"Security issues found: {len(security_issues)}",
            error_message="; ".join(security_issues) if security_issues else None,
            suggestions=suggestions,
            code_quality_score=max(0.0, score)
        )
    
    def _analyze_python_quality(self, code: str) -> TestResult:
        """Analyze Python code quality and style."""
        start_time = time.time()
        
        quality_issues = []
        suggestions = []
        score = 1.0
        
        lines = code.split('\n')
        
        # Check line length
        long_lines = [i+1 for i, line in enumerate(lines) 
                     if len(line) > self.quality_thresholds["line_length"]]
        if long_lines:
            quality_issues.append(f"Lines too long: {long_lines}")
            suggestions.append("Break long lines for better readability")
            score -= 0.1
        
        # Check for function length
        in_function = False
        function_lines = 0
        for line in lines:
            if line.strip().startswith('def '):
                in_function = True
                function_lines = 0
            elif in_function:
                if line.strip() and not line.startswith(' ') and not line.startswith('\t'):
                    if function_lines > self.quality_thresholds["function_length"]:
                        quality_issues.append("Function too long")
                        suggestions.append("Break large functions into smaller ones")
                        score -= 0.1
                    in_function = False
                else:
                    function_lines += 1
        
        # Check for proper naming conventions
        if re.search(r'def [A-Z]', code):
            quality_issues.append("Function names should be lowercase with underscores")
            suggestions.append("Use snake_case for function names")
            score -= 0.1
        
        # Check for docstrings
        if 'def ' in code and '"""' not in code and "'''" not in code:
            quality_issues.append("Missing docstrings")
            suggestions.append("Add docstrings to functions and classes")
            score -= 0.1
        
        return TestResult(
            test_name="Python Code Quality Analysis",
            passed=len(quality_issues) == 0,
            execution_time=time.time() - start_time,
            output=f"Quality issues found: {len(quality_issues)}",
            error_message="; ".join(quality_issues) if quality_issues else None,
            suggestions=suggestions,
            code_quality_score=max(0.0, score)
        )
    
    def _test_javascript_code(self, code: str, test_type: str) -> Dict[str, Any]:
        """Test JavaScript code comprehensively."""
        tests_run = []
        
        # Syntax validation using Node.js
        syntax_result = self._test_javascript_syntax(code)
        tests_run.append(syntax_result)
        
        if test_type in ["full", "functionality"] and syntax_result.passed:
            # Functionality testing
            func_result = self._test_javascript_functionality(code)
            tests_run.append(func_result)
        
        if test_type in ["full", "security"]:
            # Security analysis
            security_result = self._test_javascript_security(code)
            tests_run.append(security_result)
        
        return {"tests_run": tests_run}
    
    def _test_javascript_syntax(self, code: str) -> TestResult:
        """Test JavaScript syntax validity."""
        start_time = time.time()
        
        try:
            # Create a temporary file for syntax checking
            with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            # Check syntax using Node.js
            result = subprocess.run(
                ['node', '--check', temp_file],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            # Clean up
            os.unlink(temp_file)
            
            if result.returncode == 0:
                return TestResult(
                    test_name="JavaScript Syntax Validation",
                    passed=True,
                    execution_time=time.time() - start_time,
                    output="Syntax is valid",
                    code_quality_score=1.0
                )
            else:
                return TestResult(
                    test_name="JavaScript Syntax Validation",
                    passed=False,
                    execution_time=time.time() - start_time,
                    output="Syntax error detected",
                    error_message=result.stderr,
                    suggestions=["Fix JavaScript syntax errors", "Check for missing semicolons or brackets"],
                    code_quality_score=0.0
                )
        
        except FileNotFoundError:
            return TestResult(
                test_name="JavaScript Syntax Validation",
                passed=False,
                execution_time=time.time() - start_time,
                output="Node.js not available",
                error_message="Node.js is required for JavaScript testing",
                suggestions=["Install Node.js to enable JavaScript testing"],
                code_quality_score=0.0
            )
        except Exception as e:
            return TestResult(
                test_name="JavaScript Syntax Validation",
                passed=False,
                execution_time=time.time() - start_time,
                output="Testing failed",
                error_message=str(e),
                suggestions=["Review JavaScript code for issues"],
                code_quality_score=0.0
            )
    
    def _test_javascript_functionality(self, code: str) -> TestResult:
        """Test JavaScript code functionality."""
        start_time = time.time()
        
        try:
            # Create a temporary file for execution
            with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            # Execute the code
            result = subprocess.run(
                ['node', temp_file],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Clean up
            os.unlink(temp_file)
            
            if result.returncode == 0:
                return TestResult(
                    test_name="JavaScript Functionality Test",
                    passed=True,
                    execution_time=time.time() - start_time,
                    output=result.stdout,
                    code_quality_score=0.9
                )
            else:
                return TestResult(
                    test_name="JavaScript Functionality Test",
                    passed=False,
                    execution_time=time.time() - start_time,
                    output=result.stdout,
                    error_message=result.stderr,
                    suggestions=["Check for runtime errors", "Verify all variables are defined"],
                    code_quality_score=0.3
                )
        
        except Exception as e:
            return TestResult(
                test_name="JavaScript Functionality Test",
                passed=False,
                execution_time=time.time() - start_time,
                output="",
                error_message=str(e),
                suggestions=["Review JavaScript code for potential issues"],
                code_quality_score=0.1
            )
    
    def _test_javascript_security(self, code: str) -> TestResult:
        """Analyze JavaScript code for security issues."""
        start_time = time.time()
        
        security_issues = []
        suggestions = []
        score = 1.0
        
        # Check for dangerous functions
        if 'eval(' in code:
            security_issues.append("Dangerous function 'eval' detected")
            suggestions.append("Avoid using 'eval' or ensure input validation")
            score -= 0.4
        
        if 'innerHTML' in code:
            security_issues.append("Potential XSS vulnerability with innerHTML")
            suggestions.append("Use textContent or sanitize HTML content")
            score -= 0.3
        
        if 'document.write' in code:
            security_issues.append("Dangerous function 'document.write' detected")
            suggestions.append("Use modern DOM manipulation methods")
            score -= 0.2
        
        return TestResult(
            test_name="JavaScript Security Analysis",
            passed=len(security_issues) == 0,
            execution_time=time.time() - start_time,
            output=f"Security issues found: {len(security_issues)}",
            error_message="; ".join(security_issues) if security_issues else None,
            suggestions=suggestions,
            code_quality_score=max(0.0, score)
        )
    
    def _test_rust_code(self, code: str, test_type: str) -> Dict[str, Any]:
        """Test Rust code comprehensively."""
        tests_run = []
        
        # Syntax and compilation test
        compile_result = self._test_rust_compilation(code)
        tests_run.append(compile_result)
        
        if test_type in ["full", "functionality"] and compile_result.passed:
            # Functionality testing
            func_result = self._test_rust_functionality(code)
            tests_run.append(func_result)
        
        return {"tests_run": tests_run}
    
    def _test_rust_compilation(self, code: str) -> TestResult:
        """Test Rust code compilation."""
        start_time = time.time()
        
        try:
            # Create a temporary Rust project
            with tempfile.TemporaryDirectory() as temp_dir:
                # Create main.rs
                main_file = os.path.join(temp_dir, "main.rs")
                with open(main_file, 'w') as f:
                    f.write(code)
                
                # Compile the code
                result = subprocess.run(
                    ['rustc', main_file],
                    capture_output=True,
                    text=True,
                    timeout=60,
                    cwd=temp_dir
                )
                
                if result.returncode == 0:
                    return TestResult(
                        test_name="Rust Compilation Test",
                        passed=True,
                        execution_time=time.time() - start_time,
                        output="Compilation successful",
                        code_quality_score=1.0
                    )
                else:
                    return TestResult(
                        test_name="Rust Compilation Test",
                        passed=False,
                        execution_time=time.time() - start_time,
                        output="Compilation failed",
                        error_message=result.stderr,
                        suggestions=["Fix Rust compilation errors", "Check syntax and types"],
                        code_quality_score=0.0
                    )
        
        except FileNotFoundError:
            return TestResult(
                test_name="Rust Compilation Test",
                passed=False,
                execution_time=time.time() - start_time,
                output="Rust compiler not available",
                error_message="rustc is required for Rust testing",
                suggestions=["Install Rust toolchain to enable Rust testing"],
                code_quality_score=0.0
            )
        except Exception as e:
            return TestResult(
                test_name="Rust Compilation Test",
                passed=False,
                execution_time=time.time() - start_time,
                output="Testing failed",
                error_message=str(e),
                suggestions=["Review Rust code for issues"],
                code_quality_score=0.0
            )
    
    def _test_rust_functionality(self, code: str) -> TestResult:
        """Test Rust code functionality by execution."""
        start_time = time.time()
        
        try:
            # Create a temporary Rust project
            with tempfile.TemporaryDirectory() as temp_dir:
                # Create main.rs
                main_file = os.path.join(temp_dir, "main.rs")
                with open(main_file, 'w') as f:
                    f.write(code)
                
                # Compile and run
                compile_result = subprocess.run(
                    ['rustc', main_file, '-o', 'program'],
                    capture_output=True,
                    text=True,
                    timeout=60,
                    cwd=temp_dir
                )
                
                if compile_result.returncode == 0:
                    # Run the compiled program
                    run_result = subprocess.run(
                        ['./program'],
                        capture_output=True,
                        text=True,
                        timeout=30,
                        cwd=temp_dir
                    )
                    
                    if run_result.returncode == 0:
                        return TestResult(
                            test_name="Rust Functionality Test",
                            passed=True,
                            execution_time=time.time() - start_time,
                            output=run_result.stdout,
                            code_quality_score=0.9
                        )
                    else:
                        return TestResult(
                            test_name="Rust Functionality Test",
                            passed=False,
                            execution_time=time.time() - start_time,
                            output=run_result.stdout,
                            error_message=run_result.stderr,
                            suggestions=["Check for runtime errors", "Verify program logic"],
                            code_quality_score=0.3
                        )
                else:
                    return TestResult(
                        test_name="Rust Functionality Test",
                        passed=False,
                        execution_time=time.time() - start_time,
                        output="Compilation failed",
                        error_message=compile_result.stderr,
                        suggestions=["Fix compilation errors first"],
                        code_quality_score=0.0
                    )
        
        except Exception as e:
            return TestResult(
                test_name="Rust Functionality Test",
                passed=False,
                execution_time=time.time() - start_time,
                output="",
                error_message=str(e),
                suggestions=["Review Rust code for potential issues"],
                code_quality_score=0.1
            )
    
    def _test_cpp_code(self, code: str, test_type: str) -> Dict[str, Any]:
        """Test C++ code comprehensively."""
        tests_run = []
        
        # Compilation test
        compile_result = self._test_cpp_compilation(code)
        tests_run.append(compile_result)
        
        if test_type in ["full", "functionality"] and compile_result.passed:
            # Functionality testing
            func_result = self._test_cpp_functionality(code)
            tests_run.append(func_result)
        
        return {"tests_run": tests_run}
    
    def _test_cpp_compilation(self, code: str) -> TestResult:
        """Test C++ code compilation."""
        start_time = time.time()
        
        try:
            # Create a temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.cpp', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            # Compile the code
            result = subprocess.run(
                ['g++', '-std=c++17', temp_file, '-o', temp_file + '.out'],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            # Clean up
            os.unlink(temp_file)
            if os.path.exists(temp_file + '.out'):
                os.unlink(temp_file + '.out')
            
            if result.returncode == 0:
                return TestResult(
                    test_name="C++ Compilation Test",
                    passed=True,
                    execution_time=time.time() - start_time,
                    output="Compilation successful",
                    code_quality_score=1.0
                )
            else:
                return TestResult(
                    test_name="C++ Compilation Test",
                    passed=False,
                    execution_time=time.time() - start_time,
                    output="Compilation failed",
                    error_message=result.stderr,
                    suggestions=["Fix C++ compilation errors", "Check syntax and includes"],
                    code_quality_score=0.0
                )
        
        except FileNotFoundError:
            return TestResult(
                test_name="C++ Compilation Test",
                passed=False,
                execution_time=time.time() - start_time,
                output="C++ compiler not available",
                error_message="g++ is required for C++ testing",
                suggestions=["Install g++ compiler to enable C++ testing"],
                code_quality_score=0.0
            )
        except Exception as e:
            return TestResult(
                test_name="C++ Compilation Test",
                passed=False,
                execution_time=time.time() - start_time,
                output="Testing failed",
                error_message=str(e),
                suggestions=["Review C++ code for issues"],
                code_quality_score=0.0
            )
    
    def _test_cpp_functionality(self, code: str) -> TestResult:
        """Test C++ code functionality by execution."""
        start_time = time.time()
        
        try:
            # Create a temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.cpp', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            # Compile the code
            compile_result = subprocess.run(
                ['g++', '-std=c++17', temp_file, '-o', temp_file + '.out'],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if compile_result.returncode == 0:
                # Run the compiled program
                run_result = subprocess.run(
                    [temp_file + '.out'],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                # Clean up
                os.unlink(temp_file)
                os.unlink(temp_file + '.out')
                
                if run_result.returncode == 0:
                    return TestResult(
                        test_name="C++ Functionality Test",
                        passed=True,
                        execution_time=time.time() - start_time,
                        output=run_result.stdout,
                        code_quality_score=0.9
                    )
                else:
                    return TestResult(
                        test_name="C++ Functionality Test",
                        passed=False,
                        execution_time=time.time() - start_time,
                        output=run_result.stdout,
                        error_message=run_result.stderr,
                        suggestions=["Check for runtime errors", "Verify program logic"],
                        code_quality_score=0.3
                    )
            else:
                # Clean up
                os.unlink(temp_file)
                return TestResult(
                    test_name="C++ Functionality Test",
                    passed=False,
                    execution_time=time.time() - start_time,
                    output="Compilation failed",
                    error_message=compile_result.stderr,
                    suggestions=["Fix compilation errors first"],
                    code_quality_score=0.0
                )
        
        except Exception as e:
            return TestResult(
                test_name="C++ Functionality Test",
                passed=False,
                execution_time=time.time() - start_time,
                output="",
                error_message=str(e),
                suggestions=["Review C++ code for potential issues"],
                code_quality_score=0.1
            )
    
    def _test_java_code(self, code: str, test_type: str) -> Dict[str, Any]:
        """Test Java code comprehensively."""
        tests_run = []
        
        # Compilation test
        compile_result = self._test_java_compilation(code)
        tests_run.append(compile_result)
        
        return {"tests_run": tests_run}
    
    def _test_java_compilation(self, code: str) -> TestResult:
        """Test Java code compilation."""
        start_time = time.time()
        
        try:
            # Extract class name from code
            class_match = re.search(r'public\s+class\s+(\w+)', code)
            if not class_match:
                return TestResult(
                    test_name="Java Compilation Test",
                    passed=False,
                    execution_time=time.time() - start_time,
                    output="No public class found",
                    error_message="Java code must contain a public class",
                    suggestions=["Add a public class to your Java code"],
                    code_quality_score=0.0
                )
            
            class_name = class_match.group(1)
            
            # Create a temporary file
            with tempfile.TemporaryDirectory() as temp_dir:
                java_file = os.path.join(temp_dir, f"{class_name}.java")
                with open(java_file, 'w') as f:
                    f.write(code)
                
                # Compile the code
                result = subprocess.run(
                    ['javac', java_file],
                    capture_output=True,
                    text=True,
                    timeout=60,
                    cwd=temp_dir
                )
                
                if result.returncode == 0:
                    return TestResult(
                        test_name="Java Compilation Test",
                        passed=True,
                        execution_time=time.time() - start_time,
                        output="Compilation successful",
                        code_quality_score=1.0
                    )
                else:
                    return TestResult(
                        test_name="Java Compilation Test",
                        passed=False,
                        execution_time=time.time() - start_time,
                        output="Compilation failed",
                        error_message=result.stderr,
                        suggestions=["Fix Java compilation errors", "Check syntax and imports"],
                        code_quality_score=0.0
                    )
        
        except FileNotFoundError:
            return TestResult(
                test_name="Java Compilation Test",
                passed=False,
                execution_time=time.time() - start_time,
                output="Java compiler not available",
                error_message="javac is required for Java testing",
                suggestions=["Install Java JDK to enable Java testing"],
                code_quality_score=0.0
            )
        except Exception as e:
            return TestResult(
                test_name="Java Compilation Test",
                passed=False,
                execution_time=time.time() - start_time,
                output="Testing failed",
                error_message=str(e),
                suggestions=["Review Java code for issues"],
                code_quality_score=0.0
            )
    
    def _test_go_code(self, code: str, test_type: str) -> Dict[str, Any]:
        """Test Go code comprehensively."""
        tests_run = []
        
        # Compilation and run test
        compile_result = self._test_go_compilation(code)
        tests_run.append(compile_result)
        
        return {"tests_run": tests_run}
    
    def _test_go_compilation(self, code: str) -> TestResult:
        """Test Go code compilation and execution."""
        start_time = time.time()
        
        try:
            # Create a temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.go', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            # Run the code
            result = subprocess.run(
                ['go', 'run', temp_file],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            # Clean up
            os.unlink(temp_file)
            
            if result.returncode == 0:
                return TestResult(
                    test_name="Go Compilation and Run Test",
                    passed=True,
                    execution_time=time.time() - start_time,
                    output=result.stdout,
                    code_quality_score=1.0
                )
            else:
                return TestResult(
                    test_name="Go Compilation and Run Test",
                    passed=False,
                    execution_time=time.time() - start_time,
                    output=result.stdout,
                    error_message=result.stderr,
                    suggestions=["Fix Go compilation or runtime errors", "Check syntax and imports"],
                    code_quality_score=0.0
                )
        
        except FileNotFoundError:
            return TestResult(
                test_name="Go Compilation and Run Test",
                passed=False,
                execution_time=time.time() - start_time,
                output="Go compiler not available",
                error_message="go is required for Go testing",
                suggestions=["Install Go to enable Go testing"],
                code_quality_score=0.0
            )
        except Exception as e:
            return TestResult(
                test_name="Go Compilation and Run Test",
                passed=False,
                execution_time=time.time() - start_time,
                output="Testing failed",
                error_message=str(e),
                suggestions=["Review Go code for issues"],
                code_quality_score=0.0
            )
    
    def _test_generic_code(self, code: str, language: str, test_type: str) -> Dict[str, Any]:
        """Test generic code with basic analysis."""
        tests_run = []
        
        # Basic syntax check
        basic_result = self._test_basic_syntax(code, language)
        tests_run.append(basic_result)
        
        return {"tests_run": tests_run}
    
    def _test_basic_syntax(self, code: str, language: str) -> TestResult:
        """Basic syntax analysis for unsupported languages."""
        start_time = time.time()
        
        issues = []
        suggestions = []
        score = 1.0
        
        # Basic checks
        if not code.strip():
            issues.append("Empty code")
            score = 0.0
        
        # Check for balanced brackets
        brackets = {'(': ')', '[': ']', '{': '}'}
        stack = []
        for char in code:
            if char in brackets:
                stack.append(char)
            elif char in brackets.values():
                if not stack or brackets[stack.pop()] != char:
                    issues.append("Unbalanced brackets")
                    suggestions.append("Check for matching brackets")
                    score -= 0.3
                    break
        
        if stack:
            issues.append("Unclosed brackets")
            suggestions.append("Close all opened brackets")
            score -= 0.3
        
        # Check for basic structure
        if language.lower() in ['c', 'cpp', 'c++', 'java'] and 'main' not in code:
            issues.append("No main function found")
            suggestions.append(f"Add a main function for {language}")
            score -= 0.2
        
        return TestResult(
            test_name=f"{language.title()} Basic Syntax Check",
            passed=len(issues) == 0,
            execution_time=time.time() - start_time,
            output=f"Basic analysis complete for {language}",
            error_message="; ".join(issues) if issues else None,
            suggestions=suggestions,
            code_quality_score=max(0.0, score)
        )
    
    def _calculate_overall_score(self, tests_run: List[TestResult]) -> float:
        """Calculate overall score from test results."""
        if not tests_run:
            return 0.0
        
        total_score = sum(test.code_quality_score for test in tests_run)
        return total_score / len(tests_run)
    
    def _generate_improvements(self, results: Dict[str, Any], code: str, language: str) -> List[str]:
        """Generate improvement suggestions based on test results."""
        improvements = []
        
        for test in results.get("tests_run", []):
            if test.suggestions:
                improvements.extend(test.suggestions)
        
        # Add language-specific improvements
        if language.lower() == "python":
            if "import" not in code and "def" in code:
                improvements.append("Consider adding type hints for better code documentation")
            
            if "print(" in code and "logging" not in code:
                improvements.append("Consider using logging instead of print for better debugging")
        
        elif language.lower() == "javascript":
            if "var " in code:
                improvements.append("Use 'let' or 'const' instead of 'var' for better scoping")
            
            if "==" in code:
                improvements.append("Use '===' for strict equality comparison")
        
        # Remove duplicates
        return list(set(improvements))
    
    def _attempt_automatic_fixes(self, code: str, language: str, results: Dict[str, Any]) -> str:
        """Attempt automatic fixes for common issues."""
        fixed_code = code
        
        if language.lower() == "python":
            # Fix common Python issues
            
            # Add missing imports
            if "json." in code and "import json" not in code:
                fixed_code = "import json\n" + fixed_code
            
            if "os." in code and "import os" not in code:
                fixed_code = "import os\n" + fixed_code
            
            if "sys." in code and "import sys" not in code:
                fixed_code = "import sys\n" + fixed_code
            
            # Fix print statements without parentheses (Python 2 style)
            fixed_code = re.sub(r'\bprint\s+([^(].*)', r'print(\1)', fixed_code)
            
            # Add basic error handling for file operations
            if "open(" in code and "try:" not in code:
                lines = fixed_code.split('\n')
                new_lines = []
                for line in lines:
                    if "open(" in line and not line.strip().startswith('#'):
                        indent = len(line) - len(line.lstrip())
                        new_lines.append(' ' * indent + "try:")
                        new_lines.append(' ' * (indent + 4) + line.strip())
                        new_lines.append(' ' * indent + "except FileNotFoundError:")
                        new_lines.append(' ' * (indent + 4) + "print('File not found')")
                    else:
                        new_lines.append(line)
                fixed_code = '\n'.join(new_lines)
        
        elif language.lower() == "javascript":
            # Fix common JavaScript issues
            
            # Replace var with let
            fixed_code = re.sub(r'\bvar\b', 'let', fixed_code)
            
            # Replace == with ===
            fixed_code = re.sub(r'(?<!=)==(?!=)', '===', fixed_code)
            fixed_code = re.sub(r'(?<!!)!=(?!=)', '!==', fixed_code)
        
        return fixed_code
    
    def continuous_testing_loop(self, code: str, language: str, max_iterations: int = 5) -> Dict[str, Any]:
        """
        Run continuous testing and improvement loop.
        
        Args:
            code: Initial code to test and improve
            language: Programming language
            max_iterations: Maximum number of improvement iterations
            
        Returns:
            Final results with improvement history
        """
        if self.emotional_ai:
            emotion = self.emotional_ai.get_emotion_by_context(
                "continuous improvement and learning", "iterative_development", 0.8
            )
            emotional_state = self.emotional_ai.express_emotion(emotion, "iterative_development", 0.8)
            self.logger.info(f"Starting continuous testing with emotion: {emotion}")
        
        current_code = code
        iteration_history = []
        
        for iteration in range(max_iterations):
            self.logger.info(f"Testing iteration {iteration + 1}/{max_iterations}")
            
            # Run comprehensive test
            results = self.run_comprehensive_test(current_code, language, "full")
            iteration_history.append({
                "iteration": iteration + 1,
                "score": results["overall_score"],
                "passed": results["passed"],
                "improvements_applied": len(results.get("improvements", []))
            })
            
            # If score is good enough, stop
            if results["overall_score"] >= 0.9:
                self.logger.info(f"Excellent score achieved: {results['overall_score']:.2f}")
                break
            
            # Apply automatic fixes if available
            if "auto_fixed_code" in results:
                current_code = results["auto_fixed_code"]
                self.logger.info(f"Applied automatic fixes, new score: {results.get('improved_score', 'N/A')}")
            else:
                # No more automatic improvements possible
                break
        
        # Express final emotional state
        if self.emotional_ai:
            if results["overall_score"] >= 0.8:
                final_emotion = self.emotional_ai.get_emotion_by_context(
                    "successful improvement and achievement", "accomplishment", 0.9
                )
            else:
                final_emotion = self.emotional_ai.get_emotion_by_context(
                    "determined effort despite challenges", "persistence", 0.7
                )
            
            final_emotional_state = self.emotional_ai.express_emotion(final_emotion, "completion", 0.8)
            results["final_emotional_state"] = final_emotional_state
        
        results["iteration_history"] = iteration_history
        results["final_code"] = current_code
        results["total_iterations"] = len(iteration_history)
        
        return results

# Example usage and testing
if __name__ == "__main__":
    # Test the self-testing system
    testing_system = SelfTestingSystem()
    
    # Test Python code
    python_code = '''
import json
import os

def process_data(filename):
    """Process data from a JSON file."""
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        
        result = []
        for item in data:
            if item.get('active', False):
                result.append(item['name'].upper())
        
        return result
    except FileNotFoundError:
        print(f"File {filename} not found")
        return []
    except json.JSONDecodeError:
        print(f"Invalid JSON in {filename}")
        return []

if __name__ == "__main__":
    # Test the function
    test_data = [
        {"name": "alice", "active": True},
        {"name": "bob", "active": False},
        {"name": "charlie", "active": True}
    ]
    
    # Write test data
    with open("test.json", "w") as f:
        json.dump(test_data, f)
    
    # Process the data
    result = process_data("test.json")
    print("Active users:", result)
    
    # Clean up
    os.remove("test.json")
'''
    
    print("🧪 Self-Testing System Demonstration")
    print("=" * 60)
    
    # Run comprehensive test
    results = testing_system.run_comprehensive_test(python_code, "python", "full")
    
    print(f"Language: {results['language']}")
    print(f"Overall Score: {results['overall_score']:.2f}")
    print(f"Passed: {results['passed']}")
    print(f"Execution Time: {results['execution_time']:.2f}s")
    print(f"Tests Run: {len(results['tests_run'])}")
    
    print("\nTest Results:")
    for test in results['tests_run']:
        status = "✅ PASS" if test.passed else "❌ FAIL"
        print(f"  {status} {test.test_name} (Score: {test.code_quality_score:.2f})")
        if test.error_message:
            print(f"    Error: {test.error_message}")
        if test.suggestions:
            print(f"    Suggestions: {', '.join(test.suggestions[:2])}")
    
    if results.get('improvements'):
        print(f"\nImprovement Suggestions ({len(results['improvements'])}):")
        for improvement in results['improvements'][:5]:
            print(f"  • {improvement}")
    
    # Test continuous improvement
    print(f"\n🔄 Testing Continuous Improvement Loop")
    
    # Code with issues for improvement
    problematic_code = '''
def bad_function(data):
    result = ""
    for i in range(len(data)):
        result = result + str(data[i]) + ","
    return result
'''
    
    continuous_results = testing_system.continuous_testing_loop(problematic_code, "python", 3)
    
    print(f"Continuous Testing Results:")
    print(f"  Initial Score: {continuous_results['iteration_history'][0]['score']:.2f}")
    print(f"  Final Score: {continuous_results['overall_score']:.2f}")
    print(f"  Iterations: {continuous_results['total_iterations']}")
    print(f"  Improvement: {continuous_results['overall_score'] - continuous_results['iteration_history'][0]['score']:.2f}")
    
    if continuous_results.get('auto_fix_applied'):
        print(f"\n📝 Auto-Fixed Code:")
        print(continuous_results['final_code'])
    
    print("\n✅ Self-Testing System Demonstration Complete!")
