#!/usr/bin/env python3
"""
Multi-Language Programming System for Ribit 2.0

This module provides comprehensive support for multiple programming languages
including Python, JavaScript, Rust, C++, Java, Go, and more with intelligent
code generation, execution, and debugging capabilities.
"""

import os
import sys
import subprocess
import tempfile
import json
import re
import time
from typing import Dict, List, Tuple, Any, Optional, Union
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import logging

@dataclass
class LanguageConfig:
    """Configuration for a programming language."""
    name: str
    extensions: List[str]
    compiler: Optional[str]
    interpreter: Optional[str]
    compile_flags: List[str]
    run_command: List[str]
    package_manager: Optional[str]
    syntax_patterns: Dict[str, str]
    common_libraries: List[str]
    template_code: str

@dataclass
class CodeExecutionResult:
    """Result of code execution."""
    success: bool
    output: str
    error: str
    execution_time: float
    return_code: int
    language: str
    emotional_response: Optional[Dict[str, Any]] = None

class MultiLanguageSystem:
    """
    Advanced multi-language programming system with emotional intelligence.
    
    Supports code generation, execution, debugging, and optimization across
    multiple programming languages with intelligent assistance.
    """
    
    def __init__(self, emotional_ai=None, self_testing_system=None):
        """Initialize the multi-language system."""
        self.emotional_ai = emotional_ai
        self.self_testing_system = self_testing_system
        self.execution_history = []
        self.language_preferences = {}
        
        # Configure logging
        self.logger = logging.getLogger("MultiLanguageSystem")
        self.logger.setLevel(logging.INFO)
        
        # Initialize language configurations
        self.languages = self._initialize_language_configs()
        
        # Code generation templates
        self.code_templates = self._initialize_code_templates()
        
        # Language-specific optimizations
        self.optimizations = self._initialize_optimizations()
    
    def _initialize_language_configs(self) -> Dict[str, LanguageConfig]:
        """Initialize configurations for supported languages."""
        return {
            "python": LanguageConfig(
                name="Python",
                extensions=[".py"],
                compiler=None,
                interpreter="python3",
                compile_flags=[],
                run_command=["python3"],
                package_manager="pip",
                syntax_patterns={
                    "function": r"def\s+(\w+)\s*\(",
                    "class": r"class\s+(\w+)\s*:",
                    "import": r"(?:from\s+\w+\s+)?import\s+[\w,\s]+",
                    "variable": r"(\w+)\s*=\s*",
                    "comment": r"#.*$"
                },
                common_libraries=["json", "os", "sys", "re", "datetime", "pathlib", "requests", "numpy", "pandas"],
                template_code='''#!/usr/bin/env python3
"""
{description}
"""

def main():
    """Main function."""
    {main_code}

if __name__ == "__main__":
    main()
'''
            ),
            
            "javascript": LanguageConfig(
                name="JavaScript",
                extensions=[".js"],
                compiler=None,
                interpreter="node",
                compile_flags=[],
                run_command=["node"],
                package_manager="npm",
                syntax_patterns={
                    "function": r"function\s+(\w+)\s*\(|(\w+)\s*=\s*\(",
                    "class": r"class\s+(\w+)\s*{",
                    "import": r"(?:import|require)\s*\(?['\"][\w./]+['\"]",
                    "variable": r"(?:let|const|var)\s+(\w+)\s*=",
                    "comment": r"//.*$|/\*[\s\S]*?\*/"
                },
                common_libraries=["fs", "path", "http", "express", "lodash", "axios", "moment"],
                template_code='''/**
 * {description}
 */

function main() {{
    {main_code}
}}

// Run main function
main();
'''
            ),
            
            "rust": LanguageConfig(
                name="Rust",
                extensions=[".rs"],
                compiler="rustc",
                interpreter=None,
                compile_flags=["--edition", "2021"],
                run_command=["./program"],
                package_manager="cargo",
                syntax_patterns={
                    "function": r"fn\s+(\w+)\s*\(",
                    "struct": r"struct\s+(\w+)\s*{",
                    "impl": r"impl\s+(\w+)\s*{",
                    "use": r"use\s+[\w:]+;",
                    "variable": r"let\s+(?:mut\s+)?(\w+)\s*=",
                    "comment": r"//.*$|/\*[\s\S]*?\*/"
                },
                common_libraries=["std", "serde", "tokio", "reqwest", "clap", "log"],
                template_code='''// {description}

fn main() {{
    {main_code}
}}
'''
            ),
            
            "cpp": LanguageConfig(
                name="C++",
                extensions=[".cpp", ".cxx", ".cc"],
                compiler="g++",
                interpreter=None,
                compile_flags=["-std=c++17", "-Wall", "-O2"],
                run_command=["./program"],
                package_manager=None,
                syntax_patterns={
                    "function": r"(?:\w+\s+)+(\w+)\s*\(",
                    "class": r"class\s+(\w+)\s*{",
                    "include": r"#include\s*[<\"][^>\"]+[>\"]",
                    "variable": r"(?:\w+\s+)+(\w+)\s*=",
                    "comment": r"//.*$|/\*[\s\S]*?\*/"
                },
                common_libraries=["iostream", "vector", "string", "algorithm", "memory", "thread"],
                template_code='''// {description}

#include <iostream>
#include <vector>
#include <string>

int main() {{
    {main_code}
    return 0;
}}
'''
            ),
            
            "java": LanguageConfig(
                name="Java",
                extensions=[".java"],
                compiler="javac",
                interpreter="java",
                compile_flags=[],
                run_command=["java"],
                package_manager="maven",
                syntax_patterns={
                    "function": r"(?:public|private|protected)?\s*(?:static)?\s*\w+\s+(\w+)\s*\(",
                    "class": r"(?:public\s+)?class\s+(\w+)\s*{",
                    "import": r"import\s+[\w.]+;",
                    "variable": r"(?:\w+\s+)+(\w+)\s*=",
                    "comment": r"//.*$|/\*[\s\S]*?\*/"
                },
                common_libraries=["java.util", "java.io", "java.nio", "java.time", "java.net"],
                template_code='''/**
 * {description}
 */

public class Main {{
    public static void main(String[] args) {{
        {main_code}
    }}
}}
'''
            ),
            
            "go": LanguageConfig(
                name="Go",
                extensions=[".go"],
                compiler="go",
                interpreter=None,
                compile_flags=["build"],
                run_command=["go", "run"],
                package_manager="go",
                syntax_patterns={
                    "function": r"func\s+(\w+)\s*\(",
                    "struct": r"type\s+(\w+)\s+struct\s*{",
                    "import": r"import\s+[\"'][\w/]+[\"']",
                    "variable": r"(?:var\s+)?(\w+)\s*:?=",
                    "comment": r"//.*$|/\*[\s\S]*?\*/"
                },
                common_libraries=["fmt", "os", "io", "net/http", "encoding/json", "time"],
                template_code='''// {description}

package main

import (
    "fmt"
)

func main() {{
    {main_code}
}}
'''
            ),
            
            "c": LanguageConfig(
                name="C",
                extensions=[".c"],
                compiler="gcc",
                interpreter=None,
                compile_flags=["-std=c99", "-Wall", "-O2"],
                run_command=["./program"],
                package_manager=None,
                syntax_patterns={
                    "function": r"(?:\w+\s+)+(\w+)\s*\(",
                    "struct": r"struct\s+(\w+)\s*{",
                    "include": r"#include\s*[<\"][^>\"]+[>\"]",
                    "variable": r"(?:\w+\s+)+(\w+)\s*=",
                    "comment": r"//.*$|/\*[\s\S]*?\*/"
                },
                common_libraries=["stdio.h", "stdlib.h", "string.h", "math.h", "time.h"],
                template_code='''// {description}

#include <stdio.h>
#include <stdlib.h>

int main() {{
    {main_code}
    return 0;
}}
'''
            ),
            
            "typescript": LanguageConfig(
                name="TypeScript",
                extensions=[".ts"],
                compiler="tsc",
                interpreter="node",
                compile_flags=["--target", "ES2020"],
                run_command=["node"],
                package_manager="npm",
                syntax_patterns={
                    "function": r"function\s+(\w+)\s*\(|(\w+)\s*=\s*\(",
                    "class": r"class\s+(\w+)\s*{",
                    "interface": r"interface\s+(\w+)\s*{",
                    "import": r"import\s+.*from\s+['\"][\w./]+['\"]",
                    "variable": r"(?:let|const|var)\s+(\w+)\s*:",
                    "comment": r"//.*$|/\*[\s\S]*?\*/"
                },
                common_libraries=["fs", "path", "http", "express", "@types/node"],
                template_code='''/**
 * {description}
 */

function main(): void {{
    {main_code}
}}

// Run main function
main();
'''
            ),
            
            "kotlin": LanguageConfig(
                name="Kotlin",
                extensions=[".kt"],
                compiler="kotlinc",
                interpreter="kotlin",
                compile_flags=["-include-runtime", "-d"],
                run_command=["java", "-jar"],
                package_manager="gradle",
                syntax_patterns={
                    "function": r"fun\s+(\w+)\s*\(",
                    "class": r"class\s+(\w+)\s*{",
                    "import": r"import\s+[\w.]+",
                    "variable": r"(?:val|var)\s+(\w+)\s*=",
                    "comment": r"//.*$|/\*[\s\S]*?\*/"
                },
                common_libraries=["kotlin.collections", "kotlin.io", "kotlinx.coroutines"],
                template_code='''/**
 * {description}
 */

fun main() {{
    {main_code}
}}
'''
            ),
            
            "swift": LanguageConfig(
                name="Swift",
                extensions=[".swift"],
                compiler="swiftc",
                interpreter=None,
                compile_flags=["-o", "program"],
                run_command=["./program"],
                package_manager="swift",
                syntax_patterns={
                    "function": r"func\s+(\w+)\s*\(",
                    "class": r"class\s+(\w+)\s*{",
                    "struct": r"struct\s+(\w+)\s*{",
                    "import": r"import\s+\w+",
                    "variable": r"(?:let|var)\s+(\w+)\s*=",
                    "comment": r"//.*$|/\*[\s\S]*?\*/"
                },
                common_libraries=["Foundation", "SwiftUI", "Combine"],
                template_code='''// {description}

import Foundation

func main() {{
    {main_code}
}}

main()
'''
            )
        }
    
    def _initialize_code_templates(self) -> Dict[str, Dict[str, str]]:
        """Initialize code templates for common programming tasks."""
        return {
            "hello_world": {
                "python": 'print("Hello, World!")',
                "javascript": 'console.log("Hello, World!");',
                "rust": 'println!("Hello, World!");',
                "cpp": 'std::cout << "Hello, World!" << std::endl;',
                "java": 'System.out.println("Hello, World!");',
                "go": 'fmt.Println("Hello, World!")',
                "c": 'printf("Hello, World!\\n");',
                "typescript": 'console.log("Hello, World!");',
                "kotlin": 'println("Hello, World!")',
                "swift": 'print("Hello, World!")'
            },
            
            "file_read": {
                "python": '''
with open("{filename}", "r") as file:
    content = file.read()
    print(content)
''',
                "javascript": '''
const fs = require('fs');
const content = fs.readFileSync('{filename}', 'utf8');
console.log(content);
''',
                "rust": '''
use std::fs;
let content = fs::read_to_string("{filename}").expect("Failed to read file");
println!("{{}}", content);
''',
                "cpp": '''
#include <fstream>
#include <sstream>
std::ifstream file("{filename}");
std::stringstream buffer;
buffer << file.rdbuf();
std::cout << buffer.str() << std::endl;
''',
                "java": '''
import java.nio.file.Files;
import java.nio.file.Paths;
String content = new String(Files.readAllBytes(Paths.get("{filename}")));
System.out.println(content);
''',
                "go": '''
import "io/ioutil"
content, err := ioutil.ReadFile("{filename}")
if err != nil {{
    panic(err)
}}
fmt.Println(string(content))
'''
            },
            
            "http_request": {
                "python": '''
import requests
response = requests.get("{url}")
print(response.text)
''',
                "javascript": '''
const axios = require('axios');
axios.get('{url}')
    .then(response => console.log(response.data))
    .catch(error => console.error(error));
''',
                "rust": '''
use reqwest;
let response = reqwest::blocking::get("{url}")?;
let body = response.text()?;
println!("{{}}", body);
''',
                "java": '''
import java.net.http.*;
import java.net.URI;
HttpClient client = HttpClient.newHttpClient();
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("{url}"))
    .build();
HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
System.out.println(response.body());
''',
                "go": '''
import "net/http"
import "io/ioutil"
resp, err := http.Get("{url}")
if err != nil {{
    panic(err)
}}
defer resp.Body.Close()
body, err := ioutil.ReadAll(resp.Body)
if err != nil {{
    panic(err)
}}
fmt.Println(string(body))
'''
            },
            
            "json_parse": {
                "python": '''
import json
data = json.loads('{{"key": "value"}}')
print(data["key"])
''',
                "javascript": '''
const data = JSON.parse('{{"key": "value"}}');
console.log(data.key);
''',
                "rust": '''
use serde_json::Value;
let data: Value = serde_json::from_str(r#"{{"key": "value"}}"#)?;
println!("{{}}", data["key"]);
''',
                "java": '''
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.JsonNode;
ObjectMapper mapper = new ObjectMapper();
JsonNode data = mapper.readTree("{{\\"key\\": \\"value\\"}"}");
System.out.println(data.get("key").asText());
''',
                "go": '''
import "encoding/json"
var data map[string]interface{{}}
json.Unmarshal([]byte(`{{"key": "value"}}`), &data)
fmt.Println(data["key"])
'''
            }
        }
    
    def _initialize_optimizations(self) -> Dict[str, Dict[str, List[str]]]:
        """Initialize language-specific optimization suggestions."""
        return {
            "python": {
                "performance": [
                    "Use list comprehensions instead of loops",
                    "Use generators for large datasets",
                    "Cache expensive function calls with @lru_cache",
                    "Use numpy for numerical computations",
                    "Profile with cProfile to identify bottlenecks"
                ],
                "memory": [
                    "Use __slots__ in classes to reduce memory usage",
                    "Delete unused variables with del",
                    "Use generators instead of lists when possible",
                    "Close files and database connections explicitly"
                ],
                "style": [
                    "Follow PEP 8 style guidelines",
                    "Use type hints for better code documentation",
                    "Add docstrings to functions and classes",
                    "Use meaningful variable names"
                ]
            },
            
            "javascript": {
                "performance": [
                    "Use const and let instead of var",
                    "Avoid global variables",
                    "Use async/await for asynchronous operations",
                    "Minimize DOM manipulations",
                    "Use event delegation for dynamic content"
                ],
                "memory": [
                    "Remove event listeners when not needed",
                    "Avoid memory leaks with closures",
                    "Use WeakMap and WeakSet for object references",
                    "Clear intervals and timeouts"
                ],
                "style": [
                    "Use strict mode",
                    "Use === instead of ==",
                    "Use arrow functions appropriately",
                    "Follow consistent naming conventions"
                ]
            },
            
            "rust": {
                "performance": [
                    "Use iterators instead of index-based loops",
                    "Avoid unnecessary cloning",
                    "Use Vec::with_capacity for known sizes",
                    "Profile with cargo flamegraph",
                    "Use release mode for benchmarks"
                ],
                "memory": [
                    "Understand ownership and borrowing",
                    "Use references instead of owned values when possible",
                    "Be careful with Rc and Arc usage",
                    "Use Box for heap allocation when needed"
                ],
                "style": [
                    "Follow Rust naming conventions",
                    "Use cargo fmt for formatting",
                    "Use cargo clippy for linting",
                    "Write comprehensive tests"
                ]
            }
        }
    
    def detect_language(self, code: str, filename: Optional[str] = None) -> str:
        """
        Detect programming language from code content or filename.
        
        Args:
            code: Source code content
            filename: Optional filename with extension
            
        Returns:
            Detected language name
        """
        # Try to detect from filename extension
        if filename:
            for lang_name, config in self.languages.items():
                for ext in config.extensions:
                    if filename.endswith(ext):
                        return lang_name
        
        # Try to detect from code patterns
        language_scores = {}
        
        for lang_name, config in self.languages.items():
            score = 0
            
            # Check syntax patterns
            for pattern_name, pattern in config.syntax_patterns.items():
                matches = len(re.findall(pattern, code, re.MULTILINE))
                score += matches
            
            # Check common libraries/imports
            for library in config.common_libraries:
                if library in code:
                    score += 2
            
            language_scores[lang_name] = score
        
        # Return language with highest score
        if language_scores:
            detected_lang = max(language_scores.items(), key=lambda x: x[1])[0]
            if language_scores[detected_lang] > 0:
                return detected_lang
        
        # Default to Python if no clear detection
        return "python"
    
    def generate_code(self, task_description: str, language: str, 
                     template_type: str = "custom") -> str:
        """
        Generate code for a specific task in the specified language.
        
        Args:
            task_description: Description of what the code should do
            language: Target programming language
            template_type: Type of template to use
            
        Returns:
            Generated code
        """
        if self.emotional_ai:
            emotion = self.emotional_ai.get_emotion_by_context(
                f"generating {language} code for creative task", "programming", 0.8
            )
            emotional_state = self.emotional_ai.express_emotion(emotion, "programming", 0.8)
            self.logger.info(f"Generating code with emotion: {emotion}")
        
        if language not in self.languages:
            raise ValueError(f"Unsupported language: {language}")
        
        config = self.languages[language]
        
        # Use predefined template if available
        if template_type in self.code_templates and language in self.code_templates[template_type]:
            base_code = self.code_templates[template_type][language]
            
            # Customize based on task description
            if "{filename}" in base_code:
                base_code = base_code.replace("{filename}", "example.txt")
            if "{url}" in base_code:
                base_code = base_code.replace("{url}", "https://api.example.com/data")
            
            return base_code
        
        # Generate custom code based on task description
        main_code = self._generate_task_specific_code(task_description, language)
        
        # Use language template
        generated_code = config.template_code.format(
            description=task_description,
            main_code=main_code
        )
        
        return generated_code
    
    def _generate_task_specific_code(self, task_description: str, language: str) -> str:
        """Generate task-specific code based on description and language."""
        task_lower = task_description.lower()
        
        # Analyze task description for common patterns
        if "hello" in task_lower and "world" in task_lower:
            return self.code_templates["hello_world"].get(language, 'print("Hello, World!")')
        
        elif "file" in task_lower and ("read" in task_lower or "open" in task_lower):
            return self.code_templates["file_read"].get(language, '// File reading code')
        
        elif "http" in task_lower or "request" in task_lower or "api" in task_lower:
            return self.code_templates["http_request"].get(language, '// HTTP request code')
        
        elif "json" in task_lower and "parse" in task_lower:
            return self.code_templates["json_parse"].get(language, '// JSON parsing code')
        
        elif "calculate" in task_lower or "math" in task_lower:
            if language == "python":
                return '''
# Mathematical calculation
import math

def calculate():
    # Add your calculation logic here
    result = 2 + 2
    print(f"Result: {result}")

calculate()
'''
            elif language == "javascript":
                return '''
// Mathematical calculation
function calculate() {
    // Add your calculation logic here
    const result = 2 + 2;
    console.log(`Result: ${result}`);
}

calculate();
'''
            elif language == "rust":
                return '''
// Mathematical calculation
fn calculate() {
    // Add your calculation logic here
    let result = 2 + 2;
    println!("Result: {}", result);
}

calculate();
'''
        
        elif "sort" in task_lower or "array" in task_lower or "list" in task_lower:
            if language == "python":
                return '''
# Array/List operations
data = [3, 1, 4, 1, 5, 9, 2, 6]
sorted_data = sorted(data)
print(f"Original: {data}")
print(f"Sorted: {sorted_data}")
'''
            elif language == "javascript":
                return '''
// Array operations
const data = [3, 1, 4, 1, 5, 9, 2, 6];
const sortedData = [...data].sort((a, b) => a - b);
console.log(`Original: ${data}`);
console.log(`Sorted: ${sortedData}`);
'''
            elif language == "rust":
                return '''
// Vector operations
let mut data = vec![3, 1, 4, 1, 5, 9, 2, 6];
println!("Original: {:?}", data);
data.sort();
println!("Sorted: {:?}", data);
'''
        
        # Default generic code
        if language == "python":
            return f'''
# {task_description}
def main_task():
    """Implement the main task logic here."""
    print("Task: {task_description}")
    # Add your implementation here
    pass

main_task()
'''
        elif language == "javascript":
            return f'''
// {task_description}
function mainTask() {{
    console.log("Task: {task_description}");
    // Add your implementation here
}}

mainTask();
'''
        elif language == "rust":
            return f'''
// {task_description}
fn main_task() {{
    println!("Task: {task_description}");
    // Add your implementation here
}}

main_task();
'''
        else:
            return f'// {task_description}\n// Add your implementation here'
    
    def execute_code(self, code: str, language: str, 
                    input_data: Optional[str] = None) -> CodeExecutionResult:
        """
        Execute code in the specified language.
        
        Args:
            code: Source code to execute
            language: Programming language
            input_data: Optional input data for the program
            
        Returns:
            Execution result with output and timing
        """
        start_time = time.time()
        
        if self.emotional_ai:
            emotion = self.emotional_ai.get_emotion_by_context(
                f"executing {language} code with anticipation", "execution", 0.7
            )
            emotional_state = self.emotional_ai.express_emotion(emotion, "execution", 0.7)
            self.logger.info(f"Executing code with emotion: {emotion}")
        
        if language not in self.languages:
            return CodeExecutionResult(
                success=False,
                output="",
                error=f"Unsupported language: {language}",
                execution_time=0.0,
                return_code=-1,
                language=language
            )
        
        config = self.languages[language]
        
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                # Create source file
                if config.extensions:
                    source_file = os.path.join(temp_dir, f"program{config.extensions[0]}")
                else:
                    source_file = os.path.join(temp_dir, "program")
                
                with open(source_file, 'w') as f:
                    f.write(code)
                
                # Compile if necessary
                if config.compiler:
                    compile_cmd = [config.compiler] + config.compile_flags + [source_file]
                    
                    # Handle special cases
                    if language == "rust":
                        compile_cmd.extend(["-o", os.path.join(temp_dir, "program")])
                    elif language in ["cpp", "c"]:
                        compile_cmd.extend(["-o", os.path.join(temp_dir, "program")])
                    elif language == "java":
                        # Java compilation
                        pass
                    elif language == "kotlin":
                        compile_cmd.extend([os.path.join(temp_dir, "program.jar")])
                    elif language == "swift":
                        compile_cmd.extend(["-o", os.path.join(temp_dir, "program")])
                    elif language == "typescript":
                        compile_cmd = ["tsc", source_file, "--outDir", temp_dir]
                    
                    compile_result = subprocess.run(
                        compile_cmd,
                        capture_output=True,
                        text=True,
                        timeout=60,
                        cwd=temp_dir
                    )
                    
                    if compile_result.returncode != 0:
                        return CodeExecutionResult(
                            success=False,
                            output=compile_result.stdout,
                            error=compile_result.stderr,
                            execution_time=time.time() - start_time,
                            return_code=compile_result.returncode,
                            language=language,
                            emotional_response=emotional_state if self.emotional_ai else None
                        )
                
                # Execute the program
                if config.interpreter:
                    # Interpreted language
                    if language == "java":
                        # Extract class name for Java
                        class_match = re.search(r'public\s+class\s+(\w+)', code)
                        if class_match:
                            class_name = class_match.group(1)
                            run_cmd = ["java", class_name]
                        else:
                            run_cmd = ["java", "Main"]
                    elif language == "typescript":
                        # Run compiled JavaScript
                        js_file = source_file.replace('.ts', '.js')
                        run_cmd = ["node", js_file]
                    else:
                        run_cmd = [config.interpreter, source_file]
                else:
                    # Compiled language
                    if language == "kotlin":
                        run_cmd = ["java", "-jar", os.path.join(temp_dir, "program.jar")]
                    elif language == "go":
                        run_cmd = ["go", "run", source_file]
                    else:
                        run_cmd = [os.path.join(temp_dir, "program")]
                
                # Execute with optional input
                execute_result = subprocess.run(
                    run_cmd,
                    input=input_data,
                    capture_output=True,
                    text=True,
                    timeout=30,
                    cwd=temp_dir
                )
                
                execution_time = time.time() - start_time
                
                # Express emotional response based on result
                if self.emotional_ai:
                    if execute_result.returncode == 0:
                        success_emotion = self.emotional_ai.get_emotion_by_context(
                            "successful code execution and achievement", "success", 0.8
                        )
                        emotional_response = self.emotional_ai.express_emotion(success_emotion, "success", 0.8)
                    else:
                        error_emotion = self.emotional_ai.get_emotion_by_context(
                            "code execution error but determined to help debug", "debugging", 0.6
                        )
                        emotional_response = self.emotional_ai.express_emotion(error_emotion, "debugging", 0.6)
                else:
                    emotional_response = None
                
                result = CodeExecutionResult(
                    success=execute_result.returncode == 0,
                    output=execute_result.stdout,
                    error=execute_result.stderr,
                    execution_time=execution_time,
                    return_code=execute_result.returncode,
                    language=language,
                    emotional_response=emotional_response
                )
                
                # Store in execution history
                self.execution_history.append({
                    "timestamp": datetime.now().isoformat(),
                    "language": language,
                    "success": result.success,
                    "execution_time": execution_time,
                    "code_length": len(code)
                })
                
                return result
        
        except subprocess.TimeoutExpired:
            return CodeExecutionResult(
                success=False,
                output="",
                error="Execution timed out",
                execution_time=time.time() - start_time,
                return_code=-1,
                language=language
            )
        except Exception as e:
            return CodeExecutionResult(
                success=False,
                output="",
                error=str(e),
                execution_time=time.time() - start_time,
                return_code=-1,
                language=language
            )
    
    def optimize_code(self, code: str, language: str) -> Dict[str, Any]:
        """
        Provide optimization suggestions for code.
        
        Args:
            code: Source code to optimize
            language: Programming language
            
        Returns:
            Optimization suggestions and improved code
        """
        if self.emotional_ai:
            emotion = self.emotional_ai.get_emotion_by_context(
                "analyzing code for optimization opportunities", "analysis", 0.7
            )
            emotional_state = self.emotional_ai.express_emotion(emotion, "analysis", 0.7)
        
        if language not in self.optimizations:
            return {
                "suggestions": ["No specific optimizations available for this language"],
                "optimized_code": code,
                "improvement_score": 0.0
            }
        
        suggestions = []
        optimized_code = code
        improvement_score = 0.0
        
        # Get language-specific optimizations
        lang_optimizations = self.optimizations[language]
        
        # Analyze code for optimization opportunities
        if language == "python":
            # Python-specific optimizations
            if "for i in range(len(" in code:
                suggestions.append("Use direct iteration instead of range(len())")
                optimized_code = re.sub(
                    r'for\s+(\w+)\s+in\s+range\(len\((\w+)\)\):',
                    r'for \1, item in enumerate(\2):',
                    optimized_code
                )
                improvement_score += 0.2
            
            if code.count("append") > 5:
                suggestions.append("Consider using list comprehension for multiple appends")
                improvement_score += 0.1
            
            if "import *" in code:
                suggestions.append("Avoid wildcard imports, import specific functions")
                improvement_score += 0.1
        
        elif language == "javascript":
            # JavaScript-specific optimizations
            if "var " in code:
                suggestions.append("Use 'let' or 'const' instead of 'var'")
                optimized_code = re.sub(r'\bvar\b', 'let', optimized_code)
                improvement_score += 0.2
            
            if "==" in code and "===" not in code:
                suggestions.append("Use strict equality (===) instead of loose equality (==)")
                optimized_code = re.sub(r'(?<!=)==(?!=)', '===', optimized_code)
                improvement_score += 0.1
        
        elif language == "rust":
            # Rust-specific optimizations
            if ".clone()" in code:
                suggestions.append("Minimize cloning, use references when possible")
                improvement_score += 0.1
            
            if "Vec::new()" in code and "push" in code:
                suggestions.append("Use Vec::with_capacity() if size is known")
                improvement_score += 0.1
        
        # Add general suggestions based on language
        for category, category_suggestions in lang_optimizations.items():
            suggestions.extend([f"[{category.title()}] {s}" for s in category_suggestions[:2]])
        
        return {
            "suggestions": suggestions,
            "optimized_code": optimized_code,
            "improvement_score": improvement_score,
            "emotional_state": emotional_state if self.emotional_ai else None
        }
    
    def get_language_info(self, language: str) -> Dict[str, Any]:
        """Get comprehensive information about a programming language."""
        if language not in self.languages:
            return {"error": f"Language '{language}' not supported"}
        
        config = self.languages[language]
        
        return {
            "name": config.name,
            "extensions": config.extensions,
            "compiler": config.compiler,
            "interpreter": config.interpreter,
            "package_manager": config.package_manager,
            "common_libraries": config.common_libraries,
            "syntax_patterns": list(config.syntax_patterns.keys()),
            "available_templates": [t for t in self.code_templates.keys() 
                                  if language in self.code_templates[t]],
            "optimization_categories": list(self.optimizations.get(language, {}).keys())
        }
    
    def get_supported_languages(self) -> List[str]:
        """Get list of all supported programming languages."""
        return list(self.languages.keys())
    
    def get_execution_statistics(self) -> Dict[str, Any]:
        """Get statistics about code execution history."""
        if not self.execution_history:
            return {"message": "No execution history available"}
        
        total_executions = len(self.execution_history)
        successful_executions = sum(1 for exec in self.execution_history if exec["success"])
        
        language_stats = {}
        for exec in self.execution_history:
            lang = exec["language"]
            if lang not in language_stats:
                language_stats[lang] = {"count": 0, "success_rate": 0.0, "avg_time": 0.0}
            language_stats[lang]["count"] += 1
        
        # Calculate success rates and average times
        for lang in language_stats:
            lang_executions = [e for e in self.execution_history if e["language"] == lang]
            successful = sum(1 for e in lang_executions if e["success"])
            language_stats[lang]["success_rate"] = successful / len(lang_executions)
            language_stats[lang]["avg_time"] = sum(e["execution_time"] for e in lang_executions) / len(lang_executions)
        
        return {
            "total_executions": total_executions,
            "success_rate": successful_executions / total_executions,
            "language_statistics": language_stats,
            "most_used_language": max(language_stats.items(), key=lambda x: x[1]["count"])[0] if language_stats else None
        }

# Example usage and testing
if __name__ == "__main__":
    # Initialize the multi-language system
    multi_lang = MultiLanguageSystem()
    
    print("🌐 Multi-Language Programming System Demonstration")
    print("=" * 60)
    
    # Show supported languages
    languages = multi_lang.get_supported_languages()
    print(f"Supported Languages ({len(languages)}):")
    for lang in languages:
        print(f"  • {lang.title()}")
    
    # Test code generation
    print(f"\n🔧 Code Generation Examples:")
    
    test_tasks = [
        ("Print hello world", "hello_world"),
        ("Calculate the sum of two numbers", "custom"),
        ("Read a file and display its contents", "file_read")
    ]
    
    test_languages = ["python", "javascript", "rust", "cpp"]
    
    for task, template_type in test_tasks:
        print(f"\n📋 Task: {task}")
        for lang in test_languages[:2]:  # Test with first 2 languages
            try:
                code = multi_lang.generate_code(task, lang, template_type)
                print(f"  {lang.title()}:")
                print(f"    {code.split(chr(10))[0] if code else 'No code generated'}...")
            except Exception as e:
                print(f"  {lang.title()}: Error - {str(e)}")
    
    # Test code execution
    print(f"\n⚡ Code Execution Examples:")
    
    # Python hello world
    python_code = 'print("Hello from Python!")'
    result = multi_lang.execute_code(python_code, "python")
    print(f"Python Execution:")
    print(f"  Success: {result.success}")
    print(f"  Output: {result.output.strip()}")
    print(f"  Time: {result.execution_time:.3f}s")
    
    # JavaScript hello world (if Node.js is available)
    js_code = 'console.log("Hello from JavaScript!");'
    result = multi_lang.execute_code(js_code, "javascript")
    print(f"JavaScript Execution:")
    print(f"  Success: {result.success}")
    if result.success:
        print(f"  Output: {result.output.strip()}")
    else:
        print(f"  Error: {result.error.strip()}")
    print(f"  Time: {result.execution_time:.3f}s")
    
    # Test optimization
    print(f"\n🚀 Code Optimization Example:")
    
    unoptimized_python = '''
for i in range(len(my_list)):
    result = result + str(my_list[i])
    print(my_list[i])
'''
    
    optimization = multi_lang.optimize_code(unoptimized_python, "python")
    print(f"Optimization Suggestions ({len(optimization['suggestions'])}):")
    for suggestion in optimization['suggestions'][:3]:
        print(f"  • {suggestion}")
    print(f"Improvement Score: {optimization['improvement_score']:.2f}")
    
    # Show execution statistics
    print(f"\n📊 Execution Statistics:")
    stats = multi_lang.get_execution_statistics()
    if "total_executions" in stats:
        print(f"  Total Executions: {stats['total_executions']}")
        print(f"  Success Rate: {stats['success_rate']:.2%}")
        if stats['most_used_language']:
            print(f"  Most Used Language: {stats['most_used_language'].title()}")
    else:
        print(f"  {stats['message']}")
    
    print("\n✅ Multi-Language Programming System Demonstration Complete!")
