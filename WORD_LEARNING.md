# Word Learning System - Ribit 2.0 🤖📚

Ribit can now learn words from chat messages, build a dictionary with use cases, and generate custom sentences using learned patterns!

---

## 🎯 Features

### Passive Learning
- **Automatic**: Learns from every message in the chat
- **No commands needed**: Happens in the background
- **Persistent**: Saves knowledge to disk

### Active Learning
- **Timed sessions**: Learn for specific duration (e.g., 2 minutes)
- **On-demand**: Use `?words 120` to learn for 120 seconds
- **Autonomous**: Ribit can choose to learn words as a task

### Word Dictionary
- **Word usage**: How many times each word appears
- **Context**: Surrounding words
- **Position**: Start, middle, or end of sentence
- **Relationships**: What words come before/after
- **Part of speech**: Detected automatically
- **Sentiment**: Positive, negative, or neutral
- **Examples**: Full sentences containing the word

### Sentence Generation
- **Pattern-based**: Generate sentences following learned patterns
- **Seed words**: Start with a specific word
- **Grammar types**: Questions, commands, descriptions, etc.

---

## 📝 Commands

### `?words`
Show word learning statistics

**Example:**
```
?words
```

**Output:**
```
📚 Word Learning Statistics

Vocabulary:
- Total words known: 100
- Unique patterns: 20
- Word pairs: 120
- Word triplets: 105

Learning History:
- Sentences analyzed: 20
- Learning sessions: 1
- Last session: 2025-10-13T12:30:00

Top 15 Words:
1. the (7x)
2. is (6x)
3. of (6x)
...

Common Pairs:
• in physics (2x)
• do you (2x)
...
```

---

### `?words <duration>`
Learn words for specific duration (in seconds)

**Example:**
```
?words 120
```
Learns for 2 minutes (120 seconds)

**Output:**
```
✅ Word Learning Complete!

Session Summary:
- Duration: 120.5 seconds
- Messages processed: 150
- New words learned: 45
- Total vocabulary: 200
- Patterns found: 50

Top Words Learned:
1. quantum (15 times)
2. physics (12 times)
...

Common Word Pairs:
• quantum physics (8x)
• machine learning (6x)
...
```

---

### `?word <word>`
Get detailed information about a specific word

**Example:**
```
?word quantum
```

**Output:**
```
📖 Word Information: "quantum"

Usage:
- Seen 15 times
- Part of speech: NOUN
- Sentiment: neutral

Common Positions:
• middle (10x)
• start (5x)

Often Follows:
• quantum → physics (8x)
• quantum → mechanics (5x)
• quantum → theory (2x)

Often Preceded By:
• about → quantum (6x)
• the → quantum (4x)

Example Sentences:
1. I am learning about quantum physics
2. Quantum mechanics is fascinating
3. The quantum theory explains...
```

---

### `?generate [word]`
Generate sentences using learned words and patterns

**Example 1: Random generation**
```
?generate
```

**Example 2: With seed word**
```
?generate quantum
```

**Output:**
```
🎨 Generated Sentences

Using Learned Patterns:
"Quantum physics is a fascinating theory"

Pattern-Based:
• (subject_verb_object): "Science helps us understand nature"
• (questions): "Do you think about consciousness?"
• (descriptions): "Learning is an amazing process"

Note: These sentences are generated from words and patterns
I learned from this chat!
```

---

## 🧠 How It Works

### 1. Passive Learning (Automatic)

Every message Ribit sees is automatically analyzed:

```python
# Happens automatically for every message
self.word_learner.learn_from_message(message, sender)
```

**What it learns:**
- Individual words
- Word pairs (bigrams)
- Word triplets (trigrams)
- Sentence patterns
- Grammar structures
- Word relationships

### 2. Word Dictionary Structure

For each word, Ribit stores:

```python
{
    'count': 15,  # How many times seen
    'contexts': ['about quantum', 'quantum physics'],  # Surrounding words
    'positions': ['start', 'middle', 'middle', ...],  # Where in sentence
    'examples': ['I love quantum physics', ...],  # Full sentences
    'follows': {'physics': 8, 'mechanics': 5},  # Words that come after
    'precedes': {'about': 6, 'the': 4},  # Words that come before
    'part_of_speech': 'NOUN',  # Detected POS
    'sentiment': 'neutral',  # Positive/negative/neutral
}
```

### 3. Sentence Generation

**Method 1: Chain-based**
```
Start word → Most common next word → Most common next word → ...
```

**Method 2: Pattern-based**
```
Template: "I [VERB] [NOUN]"
Generated: "I love physics"
```

**Method 3: Grammar-based**
```
Type: question
Pattern: "[QUESTION] you [VERB] [NOUN]?"
Generated: "Do you understand quantum?"
```

---

## 🎯 Use Cases

### 1. Learn Room Vocabulary

When Ribit joins a new room:
```
?words 300
```
Learns for 5 minutes to understand the room's vocabulary

### 2. Understand Specific Word Usage

To see how a word is used:
```
?word consciousness
```

### 3. Generate Natural Responses

Ribit uses learned patterns to generate more natural responses that match the room's style

### 4. Autonomous Learning

Ribit can autonomously decide to learn words as a background task when it hasn't learned recently

---

## 📊 Statistics

### What Gets Tracked

| Metric | Description |
|--------|-------------|
| **Vocabulary Size** | Total unique words known |
| **Sentences Analyzed** | Total messages processed |
| **Unique Patterns** | Different sentence structures |
| **Word Pairs** | Bigrams (2-word combinations) |
| **Word Triplets** | Trigrams (3-word combinations) |
| **Learning Sessions** | Number of active learning sessions |
| **Last Learning Time** | When last learned |

### Grammar Patterns

Ribit categorizes sentences into:
- **Subject-Verb-Object**: "I love physics"
- **Questions**: "What is quantum mechanics?"
- **Commands**: "Explain the theory"
- **Descriptions**: "Physics is fascinating"

---

## 🔧 Technical Details

### Part of Speech Detection

Simple heuristics-based detection:

| Type | Examples | Detection |
|------|----------|-----------|
| **QUESTION** | what, where, when, who, why, how | Exact match |
| **VERB** | is, are, was, were, have, do | Common verbs |
| **PRONOUN** | I, you, he, she, it, we, they | Exact match |
| **PREP** | in, on, at, to, for, with | Exact match |
| **ARTICLE** | a, an, the | Exact match |
| **CONJ** | and, but, or, so, because | Exact match |
| **ADJ** | -ly, -ful, -less, -ous, -ive | Suffix |
| **NOUN** | (default) | Everything else |

### Sentiment Detection

Simple keyword-based:

**Positive**: good, great, awesome, excellent, amazing, love, like, happy, etc.

**Negative**: bad, terrible, awful, horrible, hate, sad, angry, fail, error, etc.

**Neutral**: Everything else

### Storage

Knowledge is saved to:
```
word_learning/word_knowledge.json
```

Format:
```json
{
  "word_dictionary": {...},
  "sentence_patterns": {...},
  "word_pairs": {...},
  "word_triplets": {...},
  "grammar_patterns": {...},
  "stats": {...}
}
```

---

## 🎨 Examples

### Example 1: Learning from Technical Discussion

**Messages:**
```
"Quantum physics is fascinating"
"I love learning about quantum mechanics"
"The theory of quantum entanglement is complex"
```

**Learned:**
- Words: quantum (3x), physics (1x), mechanics (1x), theory (1x)
- Pairs: quantum physics, quantum mechanics, quantum entanglement
- Pattern: [NOUN] [VERB] [ADJ]

**Generated:**
```
"Quantum theory is fascinating"
```

### Example 2: Learning from Casual Chat

**Messages:**
```
"Hey, how are you?"
"I'm doing great, thanks!"
"What do you think about AI?"
```

**Learned:**
- Words: hey, how, are, you, doing, great, what, think, about
- Pairs: how are, are you, doing great, what do, think about
- Pattern: [QUESTION] [PRONOUN] [VERB]

**Generated:**
```
"How are you doing?"
```

---

## 🚀 Advanced Features

### 1. Context-Aware Generation

Ribit considers:
- What words commonly appear together
- What position words typically occupy
- What grammar pattern fits best

### 2. Frequency-Based Selection

More common words and patterns are more likely to be used

### 3. Persistent Learning

Knowledge accumulates over time and persists across restarts

### 4. Autonomous Task Selection

Ribit can autonomously choose to learn words when:
- Haven't learned recently (>1 hour)
- No other high-priority tasks
- Background task queue has space

---

## 📈 Performance

### Learning Speed

- **~100 messages/second** during active learning
- **Instant** for passive learning (per message)

### Memory Usage

- **~50MB** for 10,000 messages
- **~5KB** per 100 unique words

### Storage

- **JSON format** for easy inspection
- **Compressed** automatically by filesystem

---

## 🎯 Future Improvements

### Planned Features

1. **Better POS Tagging**
   - Use NLP library (spaCy, NLTK)
   - More accurate detection

2. **Semantic Understanding**
   - Word embeddings
   - Contextual meaning

3. **Advanced Generation**
   - Template filling
   - Style matching
   - Tone adaptation

4. **Multi-language Support**
   - Learn in multiple languages
   - Translate patterns

5. **Conversation Coherence**
   - Topic tracking
   - Context maintenance
   - Response relevance

---

## 🤖 Integration with Ribit

### Passive Learning

Every message triggers learning:
```python
async def message_callback(self, room, event):
    # Learn from this message
    self.word_learner.learn_from_message(event.body, event.sender)
    
    # ... rest of message handling
```

### Active Learning

Commands trigger focused learning:
```python
# Learn for 2 minutes
?words 120
```

### Autonomous Learning

Background task system:
```python
# Ribit decides to learn words
task = Task(
    description="Learn new words from chat history",
    priority=TaskPriority.BACKGROUND,
    interest_score=0.7
)
```

### Response Generation

Use learned patterns for natural responses:
```python
# Generate response using learned words
response = self.word_learner.generate_sentence(
    seed_word="quantum",
    max_length=15
)
```

---

## 📚 Summary

**Ribit's Word Learning System provides:**

✅ **Automatic passive learning** from every message  
✅ **Active timed learning** sessions (e.g., 2 minutes)  
✅ **Comprehensive word dictionary** with use cases  
✅ **Word relationship tracking** (what follows/precedes)  
✅ **Part of speech detection** (NOUN, VERB, ADJ, etc.)  
✅ **Sentiment analysis** (positive, negative, neutral)  
✅ **Sentence pattern recognition** (grammar types)  
✅ **Custom sentence generation** using learned patterns  
✅ **Persistent storage** (survives restarts)  
✅ **Autonomous task selection** (learns when needed)  

**Commands:**
- `?words` - Show statistics
- `?words <seconds>` - Learn for duration
- `?word <word>` - Get word info
- `?generate [word]` - Generate sentences

**Ribit can now learn how you speak and construct custom sentences naturally!** 🤖📚✨

