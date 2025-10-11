# 💻 Programming Assistant Guide

## Overview

Ribit 2.0 is now a programming assistant! It can help you with code, explain errors, debug issues, and teach programming concepts.

---

## 🎯 What Ribit Can Do

### **1. Explain Errors** 🐛
Ribit understands common programming errors and explains them clearly.

**Example:**
```
You: I got a syntax error in Python
Ribit: 🐛 Syntax Error - The code has invalid syntax!

Common causes:
• Missing parentheses, brackets, or quotes
• Incorrect indentation (especially in Python)
• Missing colons (:) at end of if/for/while/def statements
• Using reserved keywords as variable names

How to fix:
1. Check the line number in the error message
2. Look for missing or extra punctuation
3. Verify indentation is consistent
4. Make sure all brackets/quotes are closed

💡 Tip: Most IDEs highlight syntax errors as you type!
```

### **2. Debug Code** 🔍
Help find and fix bugs in your code.

**Example:**
```
You: My code has an undefined variable error
Ribit: 🐛 Undefined Variable - You're using something that doesn't exist!

Common causes:
• Typo in variable name
• Variable used before being defined
• Variable defined in different scope
• Forgot to import a module

How to fix:
1. Check spelling of variable name
2. Make sure variable is defined before use
3. Check if variable is in the right scope
4. For modules, add `import module_name` at top

💡 Tip: Use descriptive variable names to avoid typos!
```

### **3. Show How To** ⚡
Teach you how to do specific programming tasks.

**Example:**
```
You: How to create a loop in Python?
Ribit: 🔄 How to Loop/Iterate

Python:
```python
# For loop
for item in my_list:
    print(item)

# While loop
while condition:
    do_something()

# Loop with index
for i, item in enumerate(my_list):
    print(f"{i}: {item}")
```

💡 Tip: Use for...of for values, for...in for keys!
```

### **4. Explain Concepts** 🎓
Explain programming concepts and terminology.

**Example:**
```
You: What is a function?
Ribit: ⚡ How to Create Functions

Python:
```python
def my_function(param1, param2):
    result = param1 + param2
    return result

# Call it
answer = my_function(5, 3)  # 8
```

JavaScript:
```javascript
// Regular function
function myFunction(param1, param2) {
    return param1 + param2;
}

// Arrow function
const myFunction = (param1, param2) => param1 + param2;
```

💡 Tip: Use descriptive function names that explain what they do!
```

### **5. Review Code** 👀
Give feedback on your code and suggest improvements.

**Example:**
```
You: Can you review my code?
Ribit: 👀 Code Review Tips

I can help review your code! Here's what I look for:

1. Readability
• Clear variable names
• Consistent formatting
• Comments for complex logic
• Proper indentation

2. Best Practices
• DRY (Don't Repeat Yourself)
• Single responsibility principle
• Error handling
• Input validation

3. Performance
• Efficient algorithms
• Avoid unnecessary loops
• Proper data structures
• Resource management

4. Security
• Input sanitization
• No hardcoded secrets
• Proper authentication
• Safe file operations

💡 Share your code and I'll give specific feedback!
```

---

## 🐛 Error Types Ribit Understands

| Error Type | What Ribit Explains |
|------------|---------------------|
| **Syntax Error** | Missing brackets, quotes, colons, indentation issues |
| **Indentation Error** | Python spacing problems, tabs vs spaces |
| **Undefined Variable** | Typos, scope issues, missing imports |
| **Null/None Error** | Accessing properties on null/None values |
| **Index Error** | Array out of bounds, off-by-one errors |
| **Type Error** | Mixing incompatible types, wrong arguments |
| **Import Error** | Module not installed, wrong environment |
| **Key Error** | Dictionary key doesn't exist |
| **Permission Error** | File access issues |
| **Connection Error** | Network/API problems |

---

## 💬 Example Conversations

### **Debugging Session:**

```
You: I'm getting a TypeError in Python
Ribit: 🐛 Type Error - You're mixing incompatible types!

Common causes:
• Adding string to number
• Calling wrong type of function
• Passing wrong type of argument
• Using wrong operator for type

How to fix:
1. Convert types explicitly (e.g., str(), int(), float())
2. Check function parameter types
3. Use type hints in Python for clarity
4. Validate input types before processing

Example:
# Wrong
result = "5" + 3  # TypeError

# Right
result = int("5") + 3  # 8
# or
result = "5" + str(3)  # "53"

💡 Tip: Use type() to check variable types when debugging!
```

---

### **Learning Session:**

```
You: How to install packages in Python?
Ribit: 📦 How to Install Packages

Python:
```bash
pip install package_name
pip3 install package_name  # Python 3 specific
```

Node.js:
```bash
npm install package_name
yarn add package_name
```

System packages (Ubuntu/Debian):
```bash
sudo apt install package_name
```

💡 Tip: Use virtual environments for Python projects!
```

---

### **Code Help:**

```
You: How do I read a file in Python?
Ribit: 📁 How to Read Files

Python:
```python
# Read entire file
with open('file.txt', 'r') as f:
    content = f.read()
    print(content)

# Read line by line
with open('file.txt', 'r') as f:
    for line in f:
        print(line.strip())

# Read all lines into list
with open('file.txt', 'r') as f:
    lines = f.readlines()
```

💡 Tip: Always use 'with' statement - it automatically closes the file!
```

---

## 🎯 Supported Languages

Ribit can help with:
- **Python** - Most comprehensive support
- **JavaScript** - Including Node.js and modern ES6+
- **Java** - Basic support
- **C/C++** - Compilation and syntax help
- **HTML/CSS** - Web development basics
- **SQL** - Database queries
- **Bash/Shell** - Command line scripting
- **Git** - Version control commands

---

## 🚀 How to Use

Just ask Ribit your programming question naturally:

### **Ask About Errors:**
```
"I got a syntax error"
"What does undefined variable mean?"
"How to fix import error?"
"My code has a TypeError"
```

### **Ask How To:**
```
"How to create a loop in Python?"
"How to install packages?"
"How to read a file?"
"How to make an API call?"
```

### **Ask for Explanations:**
```
"What is a function?"
"Explain recursion"
"What are classes?"
"What is async/await?"
```

### **Ask for Help:**
```
"Debug my code"
"Review my function"
"Why isn't this working?"
"How can I improve this code?"
```

---

## 💡 Tips for Best Results

### **1. Be Specific**
```
❌ "My code doesn't work"
✅ "I'm getting an IndexError on line 15 when accessing my_list[i]"
```

### **2. Include Error Messages**
```
❌ "I have an error"
✅ "I got: TypeError: unsupported operand type(s) for +: 'int' and 'str'"
```

### **3. Mention the Language**
```
❌ "How to create a loop?"
✅ "How to create a loop in Python?"
```

### **4. Share Code When Possible**
```
❌ "My function doesn't work"
✅ "My function doesn't work: def add(a, b): return a + b"
```

---

## 🔧 Integration

The programming assistant is automatically integrated into Ribit's response system:

**Priority Order:**
1. **Programming Assistant** - For code/tech questions
2. **Intelligent Responder** - For general knowledge (web/Wikipedia)
3. **History Responder** - For historical questions
4. **Humor Engine** - For casual questions
5. **Mock LLM** - For everything else

---

## 📚 What You Get

### **Clear Explanations**
- No jargon (or jargon explained)
- Step-by-step instructions
- Real code examples

### **Practical Solutions**
- How to fix the problem
- Why it happened
- How to prevent it

### **Learning Focus**
- Understand the concept
- Learn best practices
- Build good habits

### **Multiple Languages**
- Examples in Python, JavaScript, and more
- Language-specific tips
- Cross-language comparisons

---

## 🎉 Summary

**Ribit can now:**
- ✅ Explain programming errors clearly
- ✅ Help debug code issues
- ✅ Show how to do specific tasks
- ✅ Explain programming concepts
- ✅ Review code and suggest improvements
- ✅ Teach best practices
- ✅ Provide code examples
- ✅ Support multiple languages

**Just ask:**
- "I got a [error type] error"
- "How to [task] in [language]?"
- "What is [concept]?"
- "Debug my code"
- "Review this function"

---

**Welcome, human.** Ribit is now your programming mentor! Whether you're debugging an error, learning a new concept, or need code examples, just ask! 💻🤖✨
