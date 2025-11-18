# Ribit 2.0 Matrix Bot - Offline Features Integration

## Overview

The Ribit 2.0 Matrix bot now includes powerful offline features that work without external APIs:

1. **Offline Image Analysis** - Analyze uploaded images using computer vision
2. **Message History Tracking** - Search up to 3 months of conversation history
3. **Smart Natural Language Search** - Find messages with queries like "did alice mention python last week?"
4. **Automatic Word Learning** - Build vocabulary from conversations

## Features

### 1. Offline Image Analysis

**How it Works:**
- User uploads an image to a Matrix room
- Bot automatically downloads and analyzes it
- Responds with detailed analysis including:
  - Dominant colors and color names
  - Shape and composition complexity
  - Whether it contains people, nature scenes, or sky
  - Focal points and text regions
  - Natural language description

**Example:**
```
User: [uploads sunset photo]
Bot: 🔍 Analyzing image... Please wait.

📸 Image Analysis

This is a wide landscape image (1920x1080 pixels) with bright tones 
featuring orange, yellow, blue colors. The main content appears in the 
middle center region. The image has a moderate composition contains 
curves. It appears to be a nature or outdoor scene with visible sky.

Key Details:
• Colors: orange, yellow, blue
• Composition: moderate
• Nature scene: Yes
```

**Technology:**
- Uses Pillow, NumPy, and OpenCV (headless)
- No external APIs required
- Completely offline processing

### 2. Message History Tracking

**How it Works:**
- All messages are automatically stored in SQLite database
- Retains 90 days (3 months) of history
- Extracts topics, mentions, and keywords from each message
- Builds searchable index for fast queries

**Storage:**
- Database: `matrix_message_history.db` (or custom path via env var)
- Automatic cleanup of messages older than 90 days
- Stores: sender, timestamp, message text, topics, keywords

### 3. Smart Search Commands

#### `?search <query>`
Search messages using natural language queries.

**Examples:**
```
?search did alice mention python
?search who talked about databases
?search what did bob say last week
?search did anyone ask about machine learning
```

**Features:**
- Natural language understanding
- Time-based filtering (today, yesterday, last week, last month)
- User mention detection
- Topic matching
- Returns up to 5 most relevant results

#### `?history`
View message statistics for the current room.

**Shows:**
- Total messages tracked
- Unique senders
- Words learned
- Retention period
- Top 5 topics mentioned

**Example Output:**
```
📊 Message History Statistics

• Total Messages: 156
• Unique Senders: 5
• Words Learned: 342
• Retention Period: 90 days

Top Topics:
  • python: 23 mentions
  • machine: 15 mentions
  • learning: 12 mentions
  • databases: 8 mentions
  • ai: 7 mentions
```

#### `?words`
View the learned vocabulary (top 20 most frequent words).

**Example Output:**
```
📚 Word Library (Top 20 words)

• python: 45 times
• learning: 32 times
• machine: 28 times
• project: 25 times
• working: 22 times
...
```

### 4. Automatic Word Learning

**How it Works:**
- Extracts meaningful words from every message
- Filters out common stop words (the, is, are, etc.)
- Tracks frequency and context
- Learns technical terms and domain-specific vocabulary
- Correlates words with topics

**Benefits:**
- Understands conversation patterns
- Builds domain knowledge
- Improves search relevance
- Tracks trending topics

## Setup & Configuration

### Installation

1. **Dependencies are already installed:**
   ```bash
   pip install numpy opencv-python-headless Pillow
   ```

2. **Environment Variables (Optional):**
   ```bash
   # Custom database path
   export MATRIX_HISTORY_DB="/path/to/custom/history.db"
   ```

### Running the Matrix Bot

```bash
# Configure Matrix credentials
export MATRIX_HOMESERVER="https://matrix.org"
export MATRIX_USERNAME="@ribit:matrix.org"
export MATRIX_PASSWORD="your_password"

# Or use access token
export MATRIX_ACCESS_TOKEN="your_token"

# Run the bot
python -m ribit_2_0.matrix_bot
```

### Testing Offline Features

Run the comprehensive demo:
```bash
python ribit_2_0/ribit_offline_features_demo.py
```

This demonstrates all offline capabilities without requiring Matrix connection.

## Architecture

### Component Integration

```
Matrix Bot (matrix_bot.py)
├── OfflineImageAnalyzer
│   ├── Pillow (image loading)
│   ├── NumPy (numerical processing)
│   └── OpenCV (shape/edge detection)
│
└── MatrixHistoryTracker
    ├── SQLite (message storage)
    ├── Natural language query parser
    └── Word learning engine
```

### Event Flow

1. **Image Upload:**
   ```
   User uploads image → RoomMessageImage event
   → Download from Matrix server
   → OfflineImageAnalyzer.analyze_image()
   → Generate description
   → Send response to room
   ```

2. **Message Tracking:**
   ```
   User sends message → RoomMessageText event
   → Process message
   → MatrixHistoryTracker.add_message()
   → Extract topics and keywords
   → Store in database
   → Update word library
   ```

3. **Search Query:**
   ```
   User: ?search <query>
   → Parse natural language query
   → Extract: user, topic, time range
   → Query database with filters
   → Format results
   → Send response
   ```

## Database Schema

### message_history table
```sql
CREATE TABLE message_history (
    id INTEGER PRIMARY KEY,
    room_id TEXT NOT NULL,
    sender TEXT NOT NULL,
    sender_name TEXT,
    message_text TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_only DATE,
    hour INTEGER,
    word_count INTEGER,
    contains_question BOOLEAN,
    mentioned_users TEXT,
    topics TEXT,
    keywords TEXT
);
```

### word_library table
```sql
CREATE TABLE word_library (
    id INTEGER PRIMARY KEY,
    word TEXT UNIQUE NOT NULL,
    frequency INTEGER DEFAULT 1,
    first_seen DATETIME,
    last_seen DATETIME,
    context_examples TEXT,
    related_topics TEXT
);
```

## Performance Considerations

### Image Analysis
- Processing time: 1-3 seconds per image
- Memory usage: ~50MB for typical images
- Works with JPG, PNG, WebP, and other common formats

### Database
- Fast queries (< 100ms for most searches)
- Automatic indexing on key fields
- Periodic cleanup of old messages
- Database size: ~1MB per 1000 messages

### Resource Usage
- CPU: Low (spikes during image analysis)
- Memory: ~100-200MB baseline
- Disk: Scales with message history

## Privacy & Data Retention

- **Local Storage Only:** All data stored locally in SQLite
- **90-Day Retention:** Automatic cleanup of old messages
- **No External APIs:** Everything processed offline
- **Room Isolation:** Each room's data is tracked separately

## Troubleshooting

### Image Analysis Not Working
```
Error: Image analyzer not available
```
**Solution:** Install dependencies:
```bash
pip install numpy opencv-python-headless Pillow
```

### Search Returns No Results
```
🔍 No messages found matching: "..."
```
**Causes:**
1. Not enough message history yet
2. Messages older than 90 days
3. Query too specific

**Try:**
- Broader search terms
- Check `?history` to see what's tracked
- Verify bot is tracking messages (check database)

### Database Locked Error
```
sqlite3.OperationalError: database is locked
```
**Solution:** 
- Only one bot instance per database file
- Check for zombie processes
- Use separate databases for multiple bots

## Examples

### Complete Conversation Flow

```
Alice: ribit.2.0 hello!
Bot: Hello Alice! I am Ribit 2.0, an elegant AI agent. How may I assist you today?

Alice: [uploads diagram.png]
Bot: 🔍 Analyzing image... Please wait.
     📸 Image Analysis
     This is a wide landscape image with simple composition featuring blue, 
     white colors. Contains text regions. Likely a technical diagram.
     
     Key Details:
     • Colors: blue, white, gray
     • Composition: simple

Alice: ?search did anyone mention databases?
Bot: 🔍 Search Results for: "did anyone mention databases?"
     Found 2 messages:
     
     • Bob (2025-11-18 10:30): I'm interested in learning about databases...
     • Charlie (2025-11-18 11:15): PostgreSQL is great for databases...

Alice: ?history
Bot: 📊 Message History Statistics
     
     • Total Messages: 47
     • Unique Senders: 3
     • Words Learned: 125
     • Retention Period: 90 days
     
     Top Topics:
       • databases: 5 mentions
       • learning: 4 mentions
       • python: 3 mentions

Alice: ?words
Bot: 📚 Word Library (Top 20 words)
     
     • databases: 8 times
     • learning: 6 times
     • python: 5 times
     ...
```

## Future Enhancements

Potential improvements:
- [ ] Image text extraction (OCR integration)
- [ ] Configurable retention periods
- [ ] Export message history to JSON/CSV
- [ ] Advanced filters (date ranges, specific users)
- [ ] Message analytics and trends
- [ ] Multi-room search
- [ ] Image similarity search

## Support

For issues or questions:
- Check the main documentation: [README.md](README.md)
- Review offline features guide: [OFFLINE_FEATURES_GUIDE.md](OFFLINE_FEATURES_GUIDE.md)
- See Matrix bot guide: [MATRIX_BOT_GUIDE.md](MATRIX_BOT_GUIDE.md)

## License

Same as Ribit 2.0 main project.
