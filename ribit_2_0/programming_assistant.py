"""
Programming Assistant for Ribit 2.0
Helps with code, debugging, and programming concepts
"""

import re
import logging

logger = logging.getLogger(__name__)

class ProgrammingAssistant:
    """Helps users with programming questions, debugging, and code explanations"""
    
    def __init__(self):
        # Common programming languages
        self.languages = {
            'python', 'javascript', 'java', 'c++', 'c', 'c#', 'ruby', 'php',
            'go', 'rust', 'swift', 'kotlin', 'typescript', 'html', 'css',
            'sql', 'bash', 'shell', 'powershell', 'r', 'matlab', 'scala'
        }
        
        # Common error patterns
        self.error_patterns = {
            'syntax error': 'syntax',
            'indentation': 'indentation',
            'undefined': 'undefined_variable',
            'not defined': 'undefined_variable',
            'null': 'null_error',
            'none': 'none_error',
            'index': 'index_error',
            'key': 'key_error',
            'type': 'type_error',
            'import': 'import_error',
            'module': 'import_error',
            'permission': 'permission_error',
            'file not found': 'file_error',
            'connection': 'connection_error',
            'timeout': 'timeout_error',
        }
        
        # Programming concepts
        self.concepts = {
            'loop', 'function', 'class', 'object', 'variable', 'array',
            'list', 'dictionary', 'hash', 'map', 'set', 'tuple',
            'recursion', 'algorithm', 'data structure', 'api', 'rest',
            'async', 'promise', 'callback', 'closure', 'scope',
            'inheritance', 'polymorphism', 'encapsulation', 'abstraction',
            'git', 'version control', 'database', 'sql', 'nosql',
            'framework', 'library', 'package', 'dependency', 'npm',
            'pip', 'virtual environment', 'docker', 'container'
        }
    
    def is_programming_question(self, query: str) -> bool:
        """Detect if query is programming-related"""
        query_lower = query.lower()
        
        # Check for programming keywords
        programming_keywords = [
            'code', 'programming', 'script', 'function', 'error', 'bug',
            'debug', 'syntax', 'compile', 'run', 'execute', 'install',
            'import', 'library', 'package', 'module', 'class', 'method',
            'variable', 'array', 'list', 'loop', 'if statement', 'algorithm',
            'git', 'github', 'repository', 'commit', 'push', 'pull',
            'api', 'database', 'sql', 'query', 'server', 'client'
        ]
        
        if any(keyword in query_lower for keyword in programming_keywords):
            return True
        
        # Check for language names
        if any(lang in query_lower for lang in self.languages):
            return True
        
        # Check for error patterns
        if any(pattern in query_lower for pattern in self.error_patterns.keys()):
            return True
        
        # Check for concepts
        if any(concept in query_lower for concept in self.concepts):
            return True
        
        # Check for code-like patterns (contains brackets, semicolons, etc.)
        if re.search(r'[{}\[\]();]', query):
            return True
        
        return False
    
    def get_response(self, query: str) -> str:
        """Get programming-related response"""
        if not self.is_programming_question(query):
            return None
        
        query_lower = query.lower()
        
        # Handle error explanations
        if 'error' in query_lower or 'exception' in query_lower:
            return self._explain_error(query)
        
        # Handle "how to" questions
        if 'how to' in query_lower or 'how do i' in query_lower:
            return self._handle_how_to(query)
        
        # Handle debugging requests
        if 'debug' in query_lower or 'fix' in query_lower or 'wrong' in query_lower:
            return self._handle_debugging(query)
        
        # Handle concept explanations
        if 'what is' in query_lower or 'explain' in query_lower:
            return self._explain_concept(query)
        
        # Handle code review
        if 'review' in query_lower or 'improve' in query_lower or 'better' in query_lower:
            return self._handle_code_review(query)
        
        # General programming response
        return self._general_programming_response(query)
    
    def _explain_error(self, query: str) -> str:
        """Explain programming errors"""
        query_lower = query.lower()
        
        # Detect error type
        error_type = None
        for pattern, etype in self.error_patterns.items():
            if pattern in query_lower:
                error_type = etype
                break
        
        if error_type == 'syntax':
            return (
                "🐛 **Syntax Error** - The code has invalid syntax!\n\n"
                "**Common causes:**\n"
                "• Missing parentheses, brackets, or quotes\n"
                "• Incorrect indentation (especially in Python)\n"
                "• Missing colons (`:`) at end of if/for/while/def statements\n"
                "• Using reserved keywords as variable names\n\n"
                "**How to fix:**\n"
                "1. Check the line number in the error message\n"
                "2. Look for missing or extra punctuation\n"
                "3. Verify indentation is consistent\n"
                "4. Make sure all brackets/quotes are closed\n\n"
                "💡 **Tip:** Most IDEs highlight syntax errors as you type!"
            )
        
        elif error_type == 'indentation':
            return (
                "🐛 **Indentation Error** - Python is picky about spacing!\n\n"
                "**The problem:**\n"
                "Python uses indentation to define code blocks. Mixing tabs and spaces, "
                "or inconsistent indentation causes errors.\n\n"
                "**How to fix:**\n"
                "1. Use **4 spaces** for each indentation level (Python standard)\n"
                "2. Don't mix tabs and spaces\n"
                "3. Make sure all code in the same block has the same indentation\n"
                "4. Check that function/class definitions end with `:` and next line is indented\n\n"
                "💡 **Tip:** Configure your editor to convert tabs to spaces!"
            )
        
        elif error_type == 'undefined_variable':
            return (
                "🐛 **Undefined Variable** - You're using something that doesn't exist!\n\n"
                "**Common causes:**\n"
                "• Typo in variable name\n"
                "• Variable used before being defined\n"
                "• Variable defined in different scope\n"
                "• Forgot to import a module\n\n"
                "**How to fix:**\n"
                "1. Check spelling of variable name\n"
                "2. Make sure variable is defined before use\n"
                "3. Check if variable is in the right scope\n"
                "4. For modules, add `import module_name` at top\n\n"
                "💡 **Tip:** Use descriptive variable names to avoid typos!"
            )
        
        elif error_type in ['null_error', 'none_error']:
            return (
                "🐛 **Null/None Error** - You're trying to use something that's empty!\n\n"
                "**The problem:**\n"
                "You're trying to access a property or call a method on `null` (JavaScript) "
                "or `None` (Python), which represents 'nothing'.\n\n"
                "**How to fix:**\n"
                "1. Check if variable is null/None before using it\n"
                "2. Initialize variables with default values\n"
                "3. Handle cases where functions return None\n\n"
                "**Python example:**\n"
                "```python\n"
                "if my_var is not None:\n"
                "    my_var.do_something()\n"
                "```\n\n"
                "**JavaScript example:**\n"
                "```javascript\n"
                "if (myVar !== null && myVar !== undefined) {\n"
                "    myVar.doSomething();\n"
                "}\n"
                "```\n\n"
                "💡 **Tip:** Use optional chaining (`?.`) in modern JavaScript!"
            )
        
        elif error_type == 'index_error':
            return (
                "🐛 **Index Error** - You're trying to access an element that doesn't exist!\n\n"
                "**The problem:**\n"
                "You're trying to access an index that's outside the bounds of the array/list.\n\n"
                "**Common causes:**\n"
                "• Index is negative (when not intended)\n"
                "• Index is >= length of array\n"
                "• Array is empty\n"
                "• Off-by-one error in loop\n\n"
                "**How to fix:**\n"
                "1. Check array length before accessing\n"
                "2. Remember: arrays start at index 0\n"
                "3. Use `len(array)` or `array.length` to check size\n"
                "4. For loops, use `range(len(array))` in Python\n\n"
                "💡 **Tip:** Use `.get()` method for dictionaries to avoid KeyError!"
            )
        
        elif error_type == 'type_error':
            return (
                "🐛 **Type Error** - You're mixing incompatible types!\n\n"
                "**Common causes:**\n"
                "• Adding string to number\n"
                "• Calling wrong type of function\n"
                "• Passing wrong type of argument\n"
                "• Using wrong operator for type\n\n"
                "**How to fix:**\n"
                "1. Convert types explicitly (e.g., `str()`, `int()`, `float()`)\n"
                "2. Check function parameter types\n"
                "3. Use type hints in Python for clarity\n"
                "4. Validate input types before processing\n\n"
                "**Example:**\n"
                "```python\n"
                "# Wrong\n"
                "result = \"5\" + 3  # TypeError\n\n"
                "# Right\n"
                "result = int(\"5\") + 3  # 8\n"
                "# or\n"
                "result = \"5\" + str(3)  # \"53\"\n"
                "```\n\n"
                "💡 **Tip:** Use `type()` to check variable types when debugging!"
            )
        
        elif error_type == 'import_error':
            return (
                "🐛 **Import Error** - Can't find the module!\n\n"
                "**Common causes:**\n"
                "• Module not installed\n"
                "• Typo in module name\n"
                "• Wrong Python environment\n"
                "• Module in different directory\n\n"
                "**How to fix:**\n"
                "1. Install the module: `pip install module_name`\n"
                "2. Check spelling of module name\n"
                "3. Activate correct virtual environment\n"
                "4. Check if module is in PYTHONPATH\n\n"
                "**Common commands:**\n"
                "```bash\n"
                "# Install package\n"
                "pip install package_name\n\n"
                "# List installed packages\n"
                "pip list\n\n"
                "# Check Python version\n"
                "python --version\n"
                "```\n\n"
                "💡 **Tip:** Use virtual environments to manage dependencies!"
            )
        
        # Generic error response
        return (
            "🐛 **Debugging Help**\n\n"
            "I can help you debug! Here's my general debugging process:\n\n"
            "**1. Read the error message carefully**\n"
            "• What type of error?\n"
            "• Which line number?\n"
            "• What was the program trying to do?\n\n"
            "**2. Check the basics**\n"
            "• Syntax (brackets, quotes, colons)\n"
            "• Indentation (especially Python)\n"
            "• Variable names (typos?)\n"
            "• Types (mixing strings and numbers?)\n\n"
            "**3. Use debugging tools**\n"
            "• Print statements to see values\n"
            "• Debugger to step through code\n"
            "• Error messages for clues\n\n"
            "**4. Search for the error**\n"
            "• Copy exact error message to Google\n"
            "• Check Stack Overflow\n"
            "• Read documentation\n\n"
            "💡 **Share the error message with me and I can help more specifically!**"
        )
    
    def _handle_how_to(self, query: str) -> str:
        """Handle 'how to' programming questions"""
        query_lower = query.lower()
        
        # Common how-to patterns
        if 'install' in query_lower:
            return (
                "📦 **How to Install Packages**\n\n"
                "**Python:**\n"
                "```bash\n"
                "pip install package_name\n"
                "pip3 install package_name  # Python 3 specific\n"
                "```\n\n"
                "**Node.js:**\n"
                "```bash\n"
                "npm install package_name\n"
                "yarn add package_name\n"
                "```\n\n"
                "**System packages (Ubuntu/Debian):**\n"
                "```bash\n"
                "sudo apt install package_name\n"
                "```\n\n"
                "💡 **Tip:** Use virtual environments for Python projects!"
            )
        
        if 'loop' in query_lower or 'iterate' in query_lower:
            return (
                "🔄 **How to Loop/Iterate**\n\n"
                "**Python:**\n"
                "```python\n"
                "# For loop\n"
                "for item in my_list:\n"
                "    print(item)\n\n"
                "# While loop\n"
                "while condition:\n"
                "    do_something()\n\n"
                "# Loop with index\n"
                "for i, item in enumerate(my_list):\n"
                "    print(f\"{i}: {item}\")\n"
                "```\n\n"
                "**JavaScript:**\n"
                "```javascript\n"
                "// For loop\n"
                "for (let item of myArray) {\n"
                "    console.log(item);\n"
                "}\n\n"
                "// forEach\n"
                "myArray.forEach(item => {\n"
                "    console.log(item);\n"
                "});\n\n"
                "// While loop\n"
                "while (condition) {\n"
                "    doSomething();\n"
                "}\n"
                "```\n\n"
                "💡 **Tip:** Use `for...of` for values, `for...in` for keys!"
            )
        
        if 'function' in query_lower or 'def' in query_lower:
            return (
                "⚡ **How to Create Functions**\n\n"
                "**Python:**\n"
                "```python\n"
                "def my_function(param1, param2):\n"
                "    result = param1 + param2\n"
                "    return result\n\n"
                "# Call it\n"
                "answer = my_function(5, 3)  # 8\n"
                "```\n\n"
                "**JavaScript:**\n"
                "```javascript\n"
                "// Regular function\n"
                "function myFunction(param1, param2) {\n"
                "    return param1 + param2;\n"
                "}\n\n"
                "// Arrow function\n"
                "const myFunction = (param1, param2) => {\n"
                "    return param1 + param2;\n"
                "};\n\n"
                "// Short arrow function\n"
                "const myFunction = (param1, param2) => param1 + param2;\n"
                "```\n\n"
                "💡 **Tip:** Use descriptive function names that explain what they do!"
            )
        
        # Generic how-to response
        return (
            "🤔 I can help with that! Could you be more specific?\n\n"
            "I can explain how to:\n"
            "• Install packages\n"
            "• Create loops and iterations\n"
            "• Define functions\n"
            "• Work with arrays/lists\n"
            "• Handle errors (try/catch)\n"
            "• Read/write files\n"
            "• Make API calls\n"
            "• Use Git\n"
            "• And much more!\n\n"
            "Just ask: \"How to [specific task] in [language]?\""
        )
    
    def _handle_debugging(self, query: str) -> str:
        """Handle debugging requests"""
        return (
            "🔍 **Debugging Checklist**\n\n"
            "Let's debug together! Here's what to check:\n\n"
            "**1. Understand the problem**\n"
            "• What were you trying to do?\n"
            "• What actually happened?\n"
            "• Any error messages?\n\n"
            "**2. Isolate the issue**\n"
            "• Which part of code is failing?\n"
            "• Can you reproduce it consistently?\n"
            "• Does it work with simpler input?\n\n"
            "**3. Check common issues**\n"
            "• Print variable values\n"
            "• Check types (string vs number)\n"
            "• Verify logic (especially conditions)\n"
            "• Look for typos\n\n"
            "**4. Use debugging tools**\n"
            "• `print()` statements\n"
            "• `console.log()` in JavaScript\n"
            "• Debugger breakpoints\n"
            "• Error stack traces\n\n"
            "💡 **Share your code and error message, and I'll help you fix it!**"
        )
    
    def _explain_concept(self, query: str) -> str:
        """Explain programming concepts"""
        query_lower = query.lower()
        
        # Try to use web knowledge for detailed explanations
        try:
            from .intelligent_responder import IntelligentResponder
            intelligent = IntelligentResponder()
            web_response = intelligent.get_response(query)
            if web_response:
                return web_response
        except Exception as e:
            logger.debug(f"Web knowledge not available for concept: {e}")
        
        # Fallback to basic explanation
        return (
            "🎓 **Programming Concept Explanation**\n\n"
            "I can explain programming concepts! For detailed information, "
            "I'll search Wikipedia and programming resources.\n\n"
            "**Popular topics I can explain:**\n"
            "• Data structures (arrays, lists, dictionaries, trees)\n"
            "• Algorithms (sorting, searching, recursion)\n"
            "• OOP concepts (classes, inheritance, polymorphism)\n"
            "• Async programming (promises, async/await)\n"
            "• Design patterns\n"
            "• Git and version control\n"
            "• APIs and REST\n"
            "• Databases (SQL, NoSQL)\n\n"
            "Ask me: \"What is [concept]?\" or \"Explain [concept]\""
        )
    
    def _handle_code_review(self, query: str) -> str:
        """Handle code review requests"""
        return (
            "👀 **Code Review Tips**\n\n"
            "I can help review your code! Here's what I look for:\n\n"
            "**1. Readability**\n"
            "• Clear variable names\n"
            "• Consistent formatting\n"
            "• Comments for complex logic\n"
            "• Proper indentation\n\n"
            "**2. Best Practices**\n"
            "• DRY (Don't Repeat Yourself)\n"
            "• Single responsibility principle\n"
            "• Error handling\n"
            "• Input validation\n\n"
            "**3. Performance**\n"
            "• Efficient algorithms\n"
            "• Avoid unnecessary loops\n"
            "• Proper data structures\n"
            "• Resource management\n\n"
            "**4. Security**\n"
            "• Input sanitization\n"
            "• No hardcoded secrets\n"
            "• Proper authentication\n"
            "• Safe file operations\n\n"
            "💡 **Share your code and I'll give specific feedback!**"
        )
    
    def _general_programming_response(self, query: str) -> str:
        """General programming assistance"""
        return (
            "💻 **Programming Assistant Ready!**\n\n"
            "I can help you with:\n\n"
            "**🐛 Debugging**\n"
            "• Explain error messages\n"
            "• Find bugs in code\n"
            "• Suggest fixes\n\n"
            "**📚 Learning**\n"
            "• Explain concepts\n"
            "• Show code examples\n"
            "• Recommend resources\n\n"
            "**⚡ Coding**\n"
            "• Write functions\n"
            "• Review code\n"
            "• Suggest improvements\n\n"
            "**🔧 Tools**\n"
            "• Git commands\n"
            "• Package installation\n"
            "• Environment setup\n\n"
            "Just ask your question, share your code, or describe your problem!"
        )


    # Alias method for compatibility
    def handle_programming_query(self, query: str) -> str:
        """Alias for get_response() for compatibility"""
        return self.get_response(query)

