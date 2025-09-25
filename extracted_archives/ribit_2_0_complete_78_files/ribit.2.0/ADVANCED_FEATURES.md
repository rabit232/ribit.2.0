# Ribit 2.0 - Advanced Features Documentation

## 🌐 Internet Search Integration with Jina.ai

Ribit 2.0 now includes sophisticated internet search capabilities powered by Jina.ai, bringing emotional intelligence to web exploration and content analysis.

### Features

#### 🔍 **Intelligent Web Search**
- **Jina.ai Integration**: Direct access to web search through Jina's powerful API
- **Emotional Context**: Each search is performed with emotional awareness (CURIOSITY, EXCITEMENT, WONDER)
- **Advanced Caching**: SQLite-based caching system for performance optimization
- **Rate Limiting**: Respectful API usage with intelligent delays
- **Context-Aware Results**: Search results enhanced with relevance scoring

#### 📄 **URL Content Analysis**
- **Automatic Content Extraction**: Fetch and analyze any URL content
- **Intelligent Summarization**: Generate meaningful summaries with emotional context
- **Content Classification**: Automatically categorize content (Educational, Technical, Informational)
- **Performance Caching**: 7-day cache for analyzed URLs
- **Emotional Content Analysis**: Detect emotional patterns in web content

#### 💾 **Advanced Caching System**
- **Hybrid Storage**: SQLite for structured data + efficient indexing
- **Performance Optimization**: O(1) lookups with proper database indexes
- **Content Deduplication**: Hash-based duplicate detection
- **Intelligent Expiration**: 24-hour cache for searches, 7-day for URL analysis
- **Metadata Storage**: Source, timestamp, relevance scores, emotion context

### Usage Examples

#### Basic Web Search
```python
import asyncio
from ribit_2_0.jina_integration import JinaSearchEngine

async def search_example():
    async with JinaSearchEngine() as search_engine:
        results = await search_engine.search_web("Python machine learning tutorials")
        
        print(f"Search emotion: {results['emotion']}")
        print(f"Found {len(results['results'])} results")
        
        for result in results['results']:
            print(f"Title: {result.get('title', 'Untitled')}")
            print(f"URL: {result.get('url', 'No URL')}")
            print(f"Snippet: {result.get('snippet', 'No description')}")

# Run the search
asyncio.run(search_example())
```

#### URL Content Analysis
```python
async def analyze_url_example():
    async with JinaSearchEngine() as analyzer:
        analysis = await analyzer.analyze_url("https://docs.python.org/3/")
        
        print(f"Analysis emotion: {analysis['emotion']}")
        print(f"Title: {analysis['title']}")
        print(f"Content type: {analysis['content_type']}")
        print(f"Word count: {analysis['word_count']}")
        print(f"Summary: {analysis['summary'][:200]}...")

asyncio.run(analyze_url_example())
```

#### Emotional Search Manager
```python
class EmotionalSearchManager:
    def __init__(self):
        self.feeling = 'PASSIONATE about information discovery'
        self.search_emotions = ['curiosity', 'excitement', 'wonder']
    
    async def contextual_search(self, query, context=None):
        print('Performing contextual search with INTELLIGENCE!')
        
        # Enhanced query with context
        if context:
            enhanced_query = f'{query} {context}'
        else:
            enhanced_query = query
        
        async with JinaSearchEngine() as engine:
            results = await engine.search_web(enhanced_query)
            print(f'Search emotion: {results.get("emotion", "NEUTRAL")}')
            return results
```

---

## 💬 Advanced Conversation Management

Ribit 2.0 features a sophisticated conversation tracking system with room-based history, emotional analysis, and comprehensive analytics.

### Features

#### 🏠 **Room-Based Conversation History**
- **Multi-Room Support**: Track conversations across different Matrix rooms/channels
- **User Context Tracking**: Individual user interaction patterns and preferences
- **Message Deduplication**: Hash-based duplicate detection and prevention
- **Relevance Scoring**: Intelligent message importance calculation
- **Emotional State Tracking**: Monitor emotional context throughout conversations

#### 📊 **Comprehensive Analytics**
- **Daily Summaries**: Automatic generation of conversation summaries
- **User Interaction Patterns**: Analyze individual user behavior and preferences
- **Peak Activity Detection**: Identify most active hours and engagement patterns
- **Sentiment Analysis**: Track emotional tone and sentiment trends
- **Topic Extraction**: Automatic identification of key conversation topics

#### ⚡ **Performance Optimization**
- **Intelligent Caching**: Multi-level caching for context, summaries, and patterns
- **Database Indexing**: Optimized SQLite schema with proper indexes
- **Efficient Queries**: O(log n) lookups with relevance-based filtering
- **Data Cleanup**: Automatic cleanup of old data while preserving summaries
- **Memory Management**: Smart cache invalidation and memory optimization

### Usage Examples

#### Adding Messages with Emotional Context
```python
from ribit_2_0.conversation_manager import AdvancedConversationManager, ConversationMessage
from datetime import datetime

manager = AdvancedConversationManager()

# Add a user message
user_message = ConversationMessage(
    room_id="!example:matrix.org",
    user_id="@user:matrix.org",
    message_type="user",
    content="Hello Ribit! Can you help me with Python programming?",
    timestamp=datetime.now(),
    emotion_state="CURIOSITY",
    context_tags=["greeting", "python", "help"],
    metadata={"platform": "matrix", "client": "element"}
)

message_id = manager.add_message(user_message)
print(f"Message added with ID: {message_id}")
```

#### Getting Conversation Context
```python
# Get recent conversation context with relevance filtering
context = manager.get_conversation_context(
    room_id="!example:matrix.org",
    limit=20,
    min_relevance=0.3  # Only messages with relevance > 0.3
)

for msg in context:
    print(f"{msg['user_id']}: {msg['content'][:50]}...")
    print(f"Emotion: {msg['emotion_state']}, Relevance: {msg['relevance_score']}")
```

#### Generating Daily Summaries
```python
# Generate comprehensive daily summary
summary = manager.generate_daily_summary("!example:matrix.org")

print(f"Summary: {summary.summary_text}")
print(f"Messages: {summary.message_count}")
print(f"Participants: {len(summary.participants)}")
print(f"Key topics: {summary.key_topics}")
print(f"Dominant emotions: {summary.dominant_emotions}")
print(f"Peak activity: {summary.peak_activity_hour}:00")
```

#### User Interaction Pattern Analysis
```python
# Analyze user behavior patterns
pattern = manager.get_user_interaction_pattern(
    room_id="!example:matrix.org",
    user_id="@user:matrix.org",
    days_back=7
)

print(f"User activity analysis:")
print(f"Messages: {pattern['message_count']}")
print(f"Avg message length: {pattern['avg_message_length']}")
print(f"Avg sentiment: {pattern['avg_sentiment']}")
print(f"Most active hour: {pattern['most_active_hour']}:00")
print(f"Dominant emotions: {pattern['dominant_emotions']}")
```

#### Contextual Summary
```python
# Get contextual summary of recent activity
contextual = manager.get_contextual_summary(
    room_id="!example:matrix.org",
    hours_back=24
)

print(f"Last 24 hours summary:")
print(f"Messages: {contextual['message_count']}")
print(f"Unique participants: {contextual['unique_participants']}")
print(f"Average relevance: {contextual['avg_relevance']}")
print(f"Average sentiment: {contextual['avg_sentiment']}")
print(f"Key topics: {contextual['key_topics']}")
print(f"Dominant emotions: {contextual['dominant_emotions']}")
```

---

## 🧠 Context-Aware Responses

Ribit 2.0's enhanced LLM emulator now includes sophisticated context awareness and conversation history integration.

### Features

#### 🎯 **Intelligent Response Routing**
- **Priority-Based Routing**: Technical queries get highest priority
- **Context-Aware Decisions**: Responses based on conversation history
- **Emotional State Tracking**: Maintain emotional continuity across messages
- **Multi-Step Task Support**: Handle complex, multi-part requests
- **Knowledge Integration**: Combine search results with conversation context

#### 🔄 **Conversation Continuity**
- **Thread Awareness**: Understand conversation threads and references
- **Context Preservation**: Maintain context across multiple interactions
- **Emotional Memory**: Remember and reference previous emotional states
- **Topic Tracking**: Follow conversation topics and provide relevant responses
- **User Preference Learning**: Adapt responses based on user interaction patterns

### Integration with Matrix Bot

The Matrix bot now automatically integrates all advanced features:

```python
# Enhanced Matrix bot with full context awareness
from ribit_2_0.matrix_bot import RibitMatrixBot
from ribit_2_0.conversation_manager import AdvancedConversationManager
from ribit_2_0.jina_integration import JinaSearchEngine

class AdvancedRibitBot(RibitMatrixBot):
    def __init__(self):
        super().__init__()
        self.conversation_manager = AdvancedConversationManager()
        
    async def handle_message(self, room, event):
        # Get conversation context
        context = self.conversation_manager.get_conversation_context(
            room_id=room.room_id,
            limit=10,
            min_relevance=0.2
        )
        
        # Perform web search if needed
        if "search" in event.body.lower():
            async with JinaSearchEngine() as search_engine:
                results = await search_engine.search_web(event.body)
                # Integrate search results into response
        
        # Generate context-aware response
        response = await self.generate_contextual_response(
            message=event.body,
            context=context,
            user_id=event.sender,
            room_id=room.room_id
        )
        
        # Send response and track conversation
        await self.send_message(room, response)
```

---

## 🚀 Performance Optimizations

### Database Performance
- **Proper Indexing**: All frequently queried columns have indexes
- **Query Optimization**: Efficient SQL queries with minimal overhead
- **Connection Pooling**: Reuse database connections for better performance
- **Batch Operations**: Group multiple operations for efficiency

### Caching Strategy
- **Multi-Level Caching**: Memory cache + SQLite cache + Redis (optional)
- **Intelligent Invalidation**: Smart cache invalidation based on relevance
- **Cache Warming**: Pre-populate frequently accessed data
- **Memory Management**: Automatic cleanup of stale cache entries

### Rate Limiting
- **Respectful API Usage**: Intelligent delays between external API calls
- **Exponential Backoff**: Progressive delays on API errors
- **Request Queuing**: Queue requests during high-load periods
- **Circuit Breaker**: Automatic fallback when services are unavailable

---

## 🔧 Configuration

### Environment Variables
```bash
# Jina.ai Configuration
JINA_SEARCH_CACHE_TTL=86400  # 24 hours
JINA_URL_CACHE_TTL=604800    # 7 days
JINA_RATE_LIMIT_DELAY=1.0    # 1 second between requests

# Conversation Management
CONVERSATION_DB_PATH="ribit_conversations.db"
CONVERSATION_CACHE_SIZE=1000
CONVERSATION_CLEANUP_DAYS=30

# Performance Optimization
REDIS_URL="redis://localhost:6379"  # Optional Redis cache
ENABLE_PERFORMANCE_LOGGING=true
```

### Database Configuration
```python
# Custom database configuration
manager = AdvancedConversationManager(
    db_path="custom_conversations.db"
)

# Custom search engine configuration
search_engine = JinaSearchEngine(
    db_path="custom_search_cache.db"
)
```

---

## 📈 Monitoring and Analytics

### Performance Metrics
- **Response Times**: Track average response times for all operations
- **Cache Hit Rates**: Monitor cache effectiveness
- **Database Performance**: Query execution times and optimization
- **Memory Usage**: Track memory consumption and optimization

### Conversation Analytics
- **Daily Activity Reports**: Automated daily conversation summaries
- **User Engagement Metrics**: Track user interaction patterns
- **Emotional Analysis**: Monitor emotional trends and patterns
- **Topic Trending**: Identify popular conversation topics

### Search Analytics
- **Search Query Analysis**: Track popular search terms and patterns
- **Content Analysis**: Monitor types of content being analyzed
- **Cache Performance**: Track search and URL analysis cache effectiveness
- **API Usage**: Monitor external API usage and optimization

---

## 🛠️ Troubleshooting

### Common Issues

#### Search Not Working
```bash
# Check Jina.ai connectivity
curl -I https://s.jina.ai/test

# Verify database permissions
ls -la ribit_search_cache.db

# Check logs
tail -f ribit.log | grep -i jina
```

#### Conversation History Issues
```bash
# Check database integrity
sqlite3 ribit_conversations.db "PRAGMA integrity_check;"

# Verify indexes
sqlite3 ribit_conversations.db ".schema"

# Clear cache if needed
rm -f ribit_conversations.db
```

#### Performance Issues
```bash
# Monitor database size
du -h *.db

# Check memory usage
ps aux | grep ribit

# Enable performance logging
export ENABLE_PERFORMANCE_LOGGING=true
```

### Debug Mode
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Enable detailed logging for all components
logger = logging.getLogger('ribit_2_0')
logger.setLevel(logging.DEBUG)
```

---

## 🎯 Future Enhancements

### Planned Features
- **Advanced NLP Integration**: Enhanced topic extraction and sentiment analysis
- **Machine Learning Models**: Personalized response generation
- **Multi-Language Support**: International conversation support
- **Voice Integration**: Speech-to-text and text-to-speech capabilities
- **Advanced Analytics Dashboard**: Web-based analytics interface

### Performance Improvements
- **Distributed Caching**: Redis cluster support for high-scale deployments
- **Database Sharding**: Horizontal scaling for large conversation volumes
- **Async Optimization**: Further async/await optimizations
- **Memory Optimization**: Advanced memory management techniques

---

## 🤝 Contributing

We welcome contributions to enhance Ribit 2.0's advanced features! Areas of focus:

- **Search Engine Improvements**: Enhanced Jina.ai integration
- **Conversation Analytics**: Advanced pattern recognition
- **Performance Optimization**: Database and caching improvements
- **Documentation**: Examples and tutorials
- **Testing**: Comprehensive test coverage

---

## 📚 API Reference

### JinaSearchEngine
```python
class JinaSearchEngine:
    async def search_web(query: str, max_results: int = 5) -> Dict
    async def analyze_url(url: str) -> Dict
    def _get_cached_search(query: str) -> Optional[Dict]
    def _cache_search_results(query: str, results: List[Dict], emotion_context: str)
```

### AdvancedConversationManager
```python
class AdvancedConversationManager:
    def add_message(message: ConversationMessage) -> int
    def get_conversation_context(room_id: str, limit: int = 50, min_relevance: float = 0.0) -> List[Dict]
    def generate_daily_summary(room_id: str, date: str = None) -> ConversationSummary
    def get_user_interaction_pattern(room_id: str, user_id: str, days_back: int = 7) -> Dict
    def cleanup_old_data(days_to_keep: int = 30) -> Dict
```

### ConversationMessage
```python
@dataclass
class ConversationMessage:
    room_id: str
    user_id: str
    message_type: str
    content: str
    timestamp: datetime
    emotion_state: str = ""
    context_tags: List[str] = None
    relevance_score: float = 0.0
    response_time_ms: int = 0
    metadata: Dict[str, Any] = None
```

---

*Ribit 2.0 - Bringing emotional intelligence and advanced capabilities to AI automation* 🤖✨
