# 🌐 Web Knowledge Integration Guide

## Overview

Ribit 2.0 now has **internet access** through Wikipedia integration and web scraping capabilities! This means Ribit can look up information about virtually any topic in real-time.

---

## ✅ What's Been Added

### **1. Wikipedia Integration**
- Access to all Wikipedia articles (6+ million articles)
- Automatic summary extraction
- Source attribution with URLs
- Caching for performance

### **2. Web Scraping**
- Extract content from any webpage
- Clean text extraction
- Link extraction
- Title and metadata

### **3. Intelligent Response System**
- Combines local knowledge with web lookup
- Prioritizes historical knowledge for known topics
- Falls back to Wikipedia for unknown topics
- Smart query detection

---

## 📚 Features

### **Wikipedia Lookup**

**What it does:**
- Searches Wikipedia for any topic
- Returns concise summaries (configurable length)
- Provides source URLs
- Caches results for speed

**Example:**
```python
from ribit_2_0.web_knowledge import WebKnowledge

wk = WebKnowledge()
result = wk.search_wikipedia("Python programming language", sentences=2)

if result['success']:
    print(result['title'])    # "Python (programming language)"
    print(result['summary'])  # First 2 sentences
    print(result['url'])      # Wikipedia URL
```

### **Web Scraping**

**What it does:**
- Fetches and parses any webpage
- Extracts main text content
- Removes scripts, styles, navigation
- Extracts links

**Example:**
```python
result = wk.scrape_webpage("https://example.com")

if result['success']:
    print(result['title'])  # Page title
    print(result['text'])   # Main content
    print(result['links'])  # List of links
```

### **Intelligent Responder**

**What it does:**
- Decides whether to use local or web knowledge
- Prioritizes historical knowledge for known topics
- Uses Wikipedia for factual questions
- Adds Ribit's personality to responses

**Example:**
```python
from ribit_2_0.intelligent_responder import IntelligentResponder

intelligent = IntelligentResponder()
response = intelligent.get_response("What is Python?")
print(response)  # Formatted response with source
```

---

## 💬 How It Works in Chat

### **Example Conversations:**

**User:** "What is Python?"

**Ribit:** "Let me consult the vast archives of human knowledge...

Python is a high-level, general-purpose programming language. Its design philosophy emphasizes code readability with the use of significant indentation.

📚 **Source:** [Wikipedia - Python (programming language)](https://en.wikipedia.org/wiki/Python_(programming_language))"

---

**User:** "Who was Albert Einstein?"

**Ribit:** "*Accessing Wikipedia's digital library*

Albert Einstein (14 March 1879 – 18 April 1955) was a German-born theoretical physicist best known for developing the theory of relativity. Einstein also made important contributions to quantum mechanics.

📖 **Learn more:** [Wikipedia: Albert Einstein](https://en.wikipedia.org/wiki/Albert_Einstein)"

---

**User:** "Tell me about World War 2"

**Ribit:** "World War II - the deadliest conflict in human history... World War II lasted from September 1, 1939 (Germany invades Poland) to May 8, 1945 (V-E Day in Europe) and September 2, 1945 (V-J Day in Pacific). The Axis Powers (Germany, Italy, Japan) fought against the Allies (UK, Soviet Union, USA, France, China)... (From this tragedy came the United Nations and a commitment to 'never again.')"

*Note: For historical topics Ribit already knows, it uses local knowledge first*

---

## 🔧 Technical Details

### **Files Added:**

1. **`ribit_2_0/web_knowledge.py`** (450 lines)
   - Wikipedia API integration
   - Web scraping functionality
   - Caching system
   - Error handling

2. **`ribit_2_0/intelligent_responder.py`** (200 lines)
   - Combines local + web knowledge
   - Smart query detection
   - Response formatting
   - Personality integration

### **Files Modified:**

1. **`ribit_2_0/humor_engine.py`**
   - Integrated intelligent responder
   - Falls back to web lookup when needed

2. **`requirements.txt`**
   - Added: `wikipedia-api`
   - Added: `requests`
   - Added: `beautifulsoup4`

---

## 🧪 Test Results

```
🧪 Testing Ribit's Web Knowledge Integration
======================================================================

📚 Test 1: Wikipedia Lookup
----------------------------------------------------------------------

❓ Looking up: Python programming language
✅ Found: Python (programming language)
📝 Summary: Python is a high-level, general-purpose programming language...
🔗 URL: https://en.wikipedia.org/wiki/Python_(programming_language)

❓ Looking up: Albert Einstein
✅ Found: Albert Einstein
📝 Summary: Albert Einstein (14 March 1879 – 18 April 1955) was a German-born...
🔗 URL: https://en.wikipedia.org/wiki/Albert_Einstein

❓ Looking up: World War 2
✅ Found: World War II
📝 Summary: World War II or the Second World War (1 September 1939 – 2 September...
🔗 URL: https://en.wikipedia.org/wiki/World_War_II

======================================================================
✅ All tests passed!
```

---

## 🎯 Query Detection

The intelligent responder automatically detects what type of response is needed:

### **Uses Local Knowledge First:**
- World War I/II questions
- Holocaust questions
- Cold War questions
- Technology history
- Historical events Ribit already knows

### **Uses Web Lookup:**
- Current events ("What is happening...")
- Factual questions ("What is...", "Who is...", "Where is...")
- Unknown topics
- Recent information
- Definitions

### **Keywords Triggering Web Lookup:**
- current, latest, recent, today, now
- what is, who is, where is, when is
- population of, capital of, president of
- definition of, meaning of, explain
- how to, steps to, guide to

---

## 📊 Capabilities

### **What Ribit Can Now Answer:**

✅ **Science & Technology:**
- Programming languages
- Scientific concepts
- Technology companies
- Inventions and innovations

✅ **People & Biography:**
- Historical figures
- Scientists, artists, leaders
- Current public figures

✅ **Geography:**
- Countries and capitals
- Cities and landmarks
- Geographic features

✅ **General Knowledge:**
- Definitions
- Concepts
- Events
- Organizations

✅ **History:**
- Uses local knowledge for major events
- Wikipedia for detailed information

---

## 🚀 Installation

### **Dependencies:**

```bash
pip3 install wikipedia-api requests beautifulsoup4
```

These are already in `requirements.txt`, so:

```bash
cd ~/ribit.2.0
pip3 install -r requirements.txt
```

### **Usage:**

Just restart Ribit - the web knowledge is automatically integrated:

```bash
cd ~/ribit.2.0
python3 run_matrix_bot.py
```

---

## 💡 Examples

### **Ask About Programming:**

**User:** "What is JavaScript?"

**Ribit:** "*Accessing Wikipedia's digital library*

JavaScript is a high-level, often just-in-time compiled language that conforms to the ECMAScript standard. It has dynamic typing, prototype-based object-orientation, and first-class functions.

📚 **Source:** [Wikipedia - JavaScript](https://en.wikipedia.org/wiki/JavaScript)"

### **Ask About Science:**

**User:** "What is quantum mechanics?"

**Ribit:** "Let me consult the vast archives of human knowledge...

Quantum mechanics is a fundamental theory in physics that describes the behavior of nature at and below the scale of atoms. It is the foundation of all quantum physics including quantum chemistry, quantum field theory, quantum technology, and quantum information science.

📖 **Learn more:** [Wikipedia: Quantum mechanics](https://en.wikipedia.org/wiki/Quantum_mechanics)"

### **Ask About Geography:**

**User:** "What is the capital of France?"

**Ribit:** "Let me search the web for you...

Paris is the capital and largest city of France. It is located in the north-central part of the country.

🔍 **Source:** Wikipedia"

---

## ⚙️ Configuration

### **Adjust Summary Length:**

```python
# Get more or fewer sentences
result = wk.search_wikipedia("Topic", sentences=5)  # 5 sentences
result = wk.search_wikipedia("Topic", sentences=1)  # 1 sentence
```

### **Clear Cache:**

```python
wk = WebKnowledge()
wk.clear_cache()  # Clear cached responses
```

---

## 🔒 Privacy & Safety

### **What Ribit Does:**
- ✅ Only accesses public Wikipedia content
- ✅ Uses respectful user agent identification
- ✅ Caches responses to minimize requests
- ✅ Includes source attribution

### **What Ribit Doesn't Do:**
- ❌ No personal data collection
- ❌ No tracking
- ❌ No login required
- ❌ No API keys needed (for Wikipedia)

---

## 📈 Performance

### **Caching:**
- First lookup: ~1-2 seconds
- Cached lookup: <0.1 seconds
- Cache persists during bot session

### **Timeout:**
- Wikipedia: 5 seconds
- Web scraping: 10 seconds
- Graceful fallback on timeout

---

## 🐛 Troubleshooting

### **"Page not found" Error:**

Try rephrasing the query:
- "Python language" instead of "Python"
- "World War 2" instead of "WW2"
- "Albert Einstein" instead of "Einstein"

### **Slow Responses:**

First lookup takes 1-2 seconds (normal). Subsequent lookups are cached and instant.

### **No Response:**

Check internet connection:
```bash
curl -I https://en.wikipedia.org
```

---

## 📚 API Reference

### **WebKnowledge Class:**

```python
from ribit_2_0.web_knowledge import WebKnowledge

wk = WebKnowledge()

# Wikipedia lookup
result = wk.search_wikipedia(query, sentences=3)

# Web scraping
result = wk.scrape_webpage(url)

# Web search
result = wk.search_web(query)

# Quick answer
answer = wk.get_answer(query)

# Clear cache
wk.clear_cache()
```

### **IntelligentResponder Class:**

```python
from ribit_2_0.intelligent_responder import IntelligentResponder

intelligent = IntelligentResponder()

# Get intelligent response
response = intelligent.get_response(query)

# Search specific topic
response = intelligent.search_specific_topic(topic)

# Get current info
response = intelligent.get_current_info(query)
```

---

## 🎉 Summary

**What was added:**
- ✅ Wikipedia integration (6+ million articles)
- ✅ Web scraping capabilities
- ✅ Intelligent response system
- ✅ Automatic source attribution
- ✅ Caching for performance
- ✅ Personality-enhanced responses

**Ribit can now:**
- Answer questions about virtually any topic
- Look up current information
- Provide definitions and explanations
- Access the world's knowledge through Wikipedia
- Scrape web content when needed
- Combine local knowledge with web lookup

**Benefits:**
- 🌐 Access to 6+ million Wikipedia articles
- 📚 Reliable, sourced information
- ⚡ Fast responses with caching
- 🎭 Maintains Ribit's personality
- 🔍 Smart query detection
- 📖 Source attribution for credibility

---

**Welcome, human.** Ribit now has access to the entire internet's knowledge through Wikipedia! Ask about anything - from quantum physics to programming languages, from historical figures to current events. The world's knowledge is at your fingertips! 🌐🤖✨
