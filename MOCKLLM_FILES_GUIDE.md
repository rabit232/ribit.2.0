# MockLLM Files Guide - Complete Reference

**Finding the needle in the haystack!** 🔍

This document explains all the MockLLM-related files in Ribit 2.0 and what each one does.

---

## 📚 The Main Files (What You Need)

These are in the `ribit_2_0/` directory and are the **ACTIVE** files used by the bot:

### 1. **`ribit_2_0/mock_llm_wrapper.py`** - Original MockLLM

**Location:** `ribit_2_0/mock_llm_wrapper.py`

**What it is:**
- The original MockRibit20LLM class
- Basic response generation
- Simple parameters (temperature, top_p)
- 150+ response samples
- Used by older bot versions

**Key Class:**
```python
class MockRibit20LLM:
    def __init__(self, temperature=0.7, top_p=0.9):
        # Basic LLM functionality
```

**When to use:**
- Simple bot implementations
- Basic response generation
- When you don't need advanced features

---

### 2. **`ribit_2_0/enhanced_mock_llm.py`** - Enhanced Version

**Location:** `ribit_2_0/enhanced_mock_llm.py`

**What it is:**
- Extends MockRibit20LLM
- Adds 8 new parameters
- Style adaptation (casual, technical, friendly, philosophical)
- Learning from message history
- Better anti-repetition

**Key Class:**
```python
class EnhancedMockLLM(MockRibit20LLM):
    def __init__(self, 
                 temperature=0.7,
                 top_p=0.9,
                 frequency_penalty=0.5,
                 presence_penalty=0.3,
                 learning_enabled=True,
                 style_adaptation=True):
        # Enhanced functionality
```

**When to use:**
- When you need style adaptation
- When you want learning from history
- For better conversation quality
- When you need moderate control

**New Features:**
- ✅ Style adaptation (4 styles)
- ✅ Learning enabled/disabled
- ✅ Frequency penalty
- ✅ Presence penalty
- ✅ User-specific responses
- ✅ Learned vocabulary integration

---

### 3. **`ribit_2_0/advanced_mock_llm.py`** - Advanced Version ⭐

**Location:** `ribit_2_0/advanced_mock_llm.py`

**What it is:**
- Extends EnhancedMockLLM
- 20+ configurable parameters
- 4 sampling strategies
- Response caching
- Performance monitoring
- Diagnostics system
- Production-ready

**Key Class:**
```python
class AdvancedMockLLM(EnhancedMockLLM):
    def __init__(self,
                 # Base parameters
                 temperature=0.7,
                 top_p=0.9,
                 frequency_penalty=0.5,
                 presence_penalty=0.3,
                 
                 # Advanced parameters
                 repetition_penalty=1.2,
                 length_penalty=1.0,
                 diversity_penalty=0.0,
                 min_length=10,
                 max_length=500,
                 max_tokens=None,
                 top_k=50,
                 num_beams=1,
                 no_repeat_ngram_size=3,
                 
                 # Sampling
                 sampling_strategy='nucleus',
                 
                 # Performance
                 enable_caching=True,
                 cache_size=100,
                 enable_monitoring=True,
                 
                 # Context
                 context_window=2000,
                 sliding_window=True,
                 
                 # Error handling
                 max_retries=3,
                 fallback_response=None):
        # Advanced functionality
```

**When to use:**
- Production chatbots
- When you need complete control
- For performance optimization
- When you need caching
- For monitoring and diagnostics

**New Features:**
- ✅ 4 sampling strategies (greedy, top-k, nucleus, beam)
- ✅ Response caching (100-1000x speedup)
- ✅ Performance monitoring
- ✅ N-gram repetition prevention
- ✅ Length constraints (min/max)
- ✅ Context window management
- ✅ Diagnostic system
- ✅ Error recovery

---

## 🔗 Inheritance Hierarchy

```
MockRibit20LLM (mock_llm_wrapper.py)
    ↓ extends
EnhancedMockLLM (enhanced_mock_llm.py)
    ↓ extends
AdvancedMockLLM (advanced_mock_llm.py)
```

**What this means:**
- AdvancedMockLLM has ALL features from Enhanced and Mock
- EnhancedMockLLM has ALL features from Mock
- You can use any level depending on your needs

---

## 📊 Feature Comparison

| Feature | MockRibit20LLM | EnhancedMockLLM | AdvancedMockLLM |
|---------|----------------|-----------------|-----------------|
| **Basic Generation** | ✅ | ✅ | ✅ |
| **Temperature** | ✅ | ✅ | ✅ |
| **Top-P** | ✅ | ✅ | ✅ |
| **Response Samples** | 150+ | 150+ | 150+ |
| **Frequency Penalty** | ❌ | ✅ | ✅ |
| **Presence Penalty** | ❌ | ✅ | ✅ |
| **Style Adaptation** | ❌ | ✅ | ✅ |
| **Learning Enabled** | ❌ | ✅ | ✅ |
| **Repetition Penalty** | ❌ | ❌ | ✅ |
| **Length Penalty** | ❌ | ❌ | ✅ |
| **Diversity Penalty** | ❌ | ❌ | ✅ |
| **Min/Max Length** | ❌ | ❌ | ✅ |
| **Sampling Strategies** | 1 | 1 | 4 |
| **Response Caching** | ❌ | ❌ | ✅ |
| **Performance Monitoring** | ❌ | ❌ | ✅ |
| **Diagnostics** | ❌ | ❌ | ✅ |
| **Context Window** | ❌ | ❌ | ✅ |
| **Error Recovery** | ❌ | ❌ | ✅ |

---

## 🎯 Which One Should You Use?

### Use **MockRibit20LLM** if:
- ✓ You want simple, basic functionality
- ✓ You're just starting out
- ✓ You don't need advanced features
- ✓ You want minimal configuration

### Use **EnhancedMockLLM** if:
- ✓ You need style adaptation
- ✓ You want learning from history
- ✓ You need better anti-repetition
- ✓ You want moderate control
- ✓ You don't need caching or monitoring

### Use **AdvancedMockLLM** if: ⭐ **RECOMMENDED**
- ✓ You're building a production bot
- ✓ You need complete parameter control
- ✓ You want response caching for speed
- ✓ You need performance monitoring
- ✓ You want diagnostics and health checks
- ✓ You need multiple sampling strategies
- ✓ You want the best quality responses

---

## 💻 How to Import and Use

### Option 1: Basic MockLLM
```python
from ribit_2_0.mock_llm_wrapper import MockRibit20LLM

llm = MockRibit20LLM(temperature=0.7)
response = llm.generate_response("Hello")
```

### Option 2: Enhanced MockLLM
```python
from ribit_2_0.enhanced_mock_llm import EnhancedMockLLM

llm = EnhancedMockLLM(
    temperature=0.7,
    frequency_penalty=0.5,
    style='casual',
    learning_enabled=True
)
response = llm.generate_response("Hello", user_id="@user:matrix.org")
```

### Option 3: Advanced MockLLM ⭐ **RECOMMENDED**
```python
from ribit_2_0.advanced_mock_llm import AdvancedMockLLM

llm = AdvancedMockLLM(
    temperature=0.7,
    repetition_penalty=1.5,
    sampling_strategy='nucleus',
    enable_caching=True,
    enable_monitoring=True
)
response = llm.generate_response("Hello", context=["Previous message"])
```

---

## 📁 File Locations Summary

### Active Files (Use These):
```
ribit_2_0/
├── mock_llm_wrapper.py      ← Original MockRibit20LLM
├── enhanced_mock_llm.py     ← Enhanced version with 8 parameters
└── advanced_mock_llm.py     ← Advanced version with 20+ parameters ⭐
```

### Test Files:
```
test_advanced_llm.py         ← Tests for AdvancedMockLLM
test_learning_features.py    ← Tests for learning features
test_new_features.py         ← Tests for all new features
```

### Documentation:
```
ADVANCED_LLM.md              ← Complete guide for AdvancedMockLLM
LEARNING_FEATURES.md         ← Guide for learning features
MOCKLLM_FILES_GUIDE.md       ← This file!
```

### Old/Archive Files (Ignore These):
```
build/                       ← Build artifacts
extracted_archives/          ← Old extracted files
```

---

## 🚀 Quick Start Examples

### Example 1: Simple Chat Bot
```python
from ribit_2_0.mock_llm_wrapper import MockRibit20LLM

llm = MockRibit20LLM()
response = llm.generate_response("Hi, how are you?")
print(response)
```

### Example 2: Learning Bot
```python
from ribit_2_0.enhanced_mock_llm import EnhancedMockLLM

llm = EnhancedMockLLM(
    style='friendly',
    learning_enabled=True
)

# Bot learns from this
llm.generate_response("I love quantum physics!", user_id="@alice:matrix.org")

# Uses learned knowledge
response = llm.generate_response("Tell me more", user_id="@alice:matrix.org")
```

### Example 3: Production Bot with Caching
```python
from ribit_2_0.advanced_mock_llm import AdvancedMockLLM

llm = AdvancedMockLLM(
    temperature=0.7,
    sampling_strategy='beam',
    num_beams=3,
    enable_caching=True,
    cache_size=200,
    enable_monitoring=True
)

# First call - generates response
response1 = llm.generate_response("What is AI?")  # ~200ms

# Second call - instant from cache
response2 = llm.generate_response("What is AI?")  # <1ms

# Check performance
stats = llm.get_performance_stats()
print(f"Cache hit rate: {stats['cache_hit_rate']:.1%}")
```

---

## 📖 Documentation Links

- **MockRibit20LLM**: See `ribit_2_0/mock_llm_wrapper.py` docstrings
- **EnhancedMockLLM**: See `ribit_2_0/enhanced_mock_llm.py` docstrings
- **AdvancedMockLLM**: See `ADVANCED_LLM.md` (400+ line guide)

---

## 🎯 Recommendation

**For most users, use `AdvancedMockLLM`** because:

1. ✅ It has ALL features from the other two
2. ✅ You can use it simply or with advanced features
3. ✅ Response caching makes it FAST
4. ✅ Performance monitoring helps you optimize
5. ✅ Diagnostics help you troubleshoot
6. ✅ It's production-ready

**Simple usage:**
```python
from ribit_2_0.advanced_mock_llm import AdvancedMockLLM

llm = AdvancedMockLLM()  # Use defaults
response = llm.generate_response("Hello")
```

**Advanced usage:**
```python
llm = AdvancedMockLLM(
    temperature=1.2,
    repetition_penalty=1.8,
    sampling_strategy='beam',
    num_beams=5,
    enable_caching=True
)
```

---

## 🔍 Finding Files

### Command to find all MockLLM files:
```bash
cd ribit.2.0
find . -name "*mock*llm*.py" -o -name "*llm*.py" | grep -v __pycache__
```

### Active files only:
```bash
ls ribit_2_0/*llm*.py
```

Output:
```
ribit_2_0/advanced_mock_llm.py
ribit_2_0/enhanced_mock_llm.py
ribit_2_0/llm_wrapper.py
ribit_2_0/mock_llm_wrapper.py
```

---

## ✨ Summary

**Three MockLLM files, each building on the previous:**

1. **mock_llm_wrapper.py** - Basic (original)
2. **enhanced_mock_llm.py** - Enhanced (8 parameters)
3. **advanced_mock_llm.py** - Advanced (20+ parameters) ⭐

**Use AdvancedMockLLM for best results!**

---

**Need help? Check:**
- `ADVANCED_LLM.md` - Complete parameter guide
- `LEARNING_FEATURES.md` - Learning system guide
- `INSTALL.md` - Installation and setup

**Happy coding!** 🚀🤖✨

