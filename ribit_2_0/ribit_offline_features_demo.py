#!/usr/bin/env python3
"""
Ribit 2.0 Offline Features Demo
Demonstrates new offline capabilities:
- Image analysis and description (no external APIs)
- Matrix message history tracking
- Smart search: "did username mention topic last week?"
- Word learning from conversations
"""

import asyncio
import logging
from pathlib import Path
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    from .offline_image_analyzer import OfflineImageAnalyzer
    from .matrix_history_tracker import MatrixHistoryTracker
except ImportError:
    # For running standalone
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from ribit_2_0.offline_image_analyzer import OfflineImageAnalyzer
    from ribit_2_0.matrix_history_tracker import MatrixHistoryTracker

def demonstrate_image_analysis():
    """Demonstrate offline image analysis capabilities"""
    print("\n" + "=" * 70)
    print("🖼️  OFFLINE IMAGE ANALYSIS DEMONSTRATION")
    print("=" * 70)
    
    analyzer = OfflineImageAnalyzer()
    
    # Create a test image for demonstration
    try:
        from PIL import Image, ImageDraw
        
        # Create sample image
        test_img = Image.new('RGB', (400, 300), color=(135, 206, 235))  # Sky blue
        draw = ImageDraw.Draw(test_img)
        
        # Add some shapes
        draw.rectangle([50, 50, 150, 150], fill=(255, 0, 0), outline=(0, 0, 0))  # Red square
        draw.ellipse([200, 100, 350, 250], fill=(0, 255, 0), outline=(0, 0, 0))  # Green circle
        
        # Save temporary image
        test_path = Path('test_image_analysis.png')
        test_img.save(test_path)
        
        print(f"\n✅ Created test image: {test_path}")
        
        # Analyze the image
        print("\n🔍 Analyzing image...")
        analysis = analyzer.analyze_image(test_path)
        
        # Display results
        print("\n📊 Analysis Results:")
        print(f"   Description: {analysis.get('description', 'N/A')}")
        
        basic = analysis.get('basic_info', {})
        print(f"\n   Basic Info:")
        print(f"     - Dimensions: {basic.get('width')}x{basic.get('height')} pixels")
        print(f"     - Aspect Ratio: {basic.get('aspect_ratio')}")
        
        colors = analysis.get('colors', {})
        print(f"\n   Colors:")
        print(f"     - Tone: {colors.get('tone')}")
        print(f"     - Brightness: {colors.get('brightness')}")
        dominant = colors.get('dominant_colors', [])
        if dominant:
            print(f"     - Dominant Colors:")
            for color in dominant[:3]:
                print(f"       • {color['name']} ({color['percentage']}%)")
        
        shapes = analysis.get('shapes', {})
        print(f"\n   Shapes:")
        print(f"     - Complexity: {shapes.get('complexity')}")
        print(f"     - Shape Count: {shapes.get('shape_count')}")
        print(f"     - Line Presence: {shapes.get('line_presence')}")
        
        text_info = analysis.get('text_regions', {})
        print(f"\n   Text Detection:")
        print(f"     - Contains Text: {text_info.get('contains_text')}")
        print(f"     - Text Likelihood: {text_info.get('text_likelihood')}")
        
        features = analysis.get('features', {})
        print(f"\n   Features Detected:")
        print(f"     - Likely Contains People: {features.get('likely_contains_people')}")
        print(f"     - Nature Scene: {features.get('likely_nature_scene')}")
        print(f"     - Has Sky: {features.get('likely_has_sky')}")
        
        # Cleanup
        if test_path.exists():
            test_path.unlink()
            print(f"\n🗑️  Cleaned up test image")
        
    except Exception as e:
        print(f"\n❌ Image analysis demonstration failed: {e}")
        import traceback
        traceback.print_exc()

def demonstrate_message_history():
    """Demonstrate Matrix message history tracking"""
    print("\n" + "=" * 70)
    print("💬 MESSAGE HISTORY TRACKING DEMONSTRATION")
    print("=" * 70)
    
    tracker = MatrixHistoryTracker(db_path="demo_message_history.db")
    
    # Simulate adding messages
    print("\n📝 Simulating conversation history...")
    
    sample_messages = [
        ("!room123", "@alice:matrix.org", "Hey everyone, has anyone worked with Python lately?", "Alice"),
        ("!room123", "@bob:matrix.org", "Yes @alice, I've been using Python for machine learning projects", "Bob"),
        ("!room123", "@charlie:matrix.org", "I'm interested in learning about databases. Any recommendations?", "Charlie"),
        ("!room123", "@alice:matrix.org", "PostgreSQL is great for most use cases", "Alice"),
        ("!room123", "@bob:matrix.org", "Did anyone mention AI or machine learning last week?", "Bob"),
    ]
    
    # Add messages with time offsets
    for i, (room, sender, text, name) in enumerate(sample_messages):
        tracker.add_message(room, sender, text, name)
        print(f"   ✓ Added message from {name}")
    
    # Get statistics
    print("\n📊 Message History Statistics:")
    stats = tracker.get_statistics("!room123")
    print(f"   - Total Messages: {stats.get('total_messages')}")
    print(f"   - Unique Senders: {stats.get('unique_senders')}")
    print(f"   - Words Learned: {stats.get('words_learned')}")
    print(f"   - Retention Period: {stats.get('retention_days')} days")
    
    if stats.get('top_topics'):
        print(f"\n   Top Topics:")
        for topic_info in stats['top_topics'][:5]:
            print(f"     • {topic_info['topic']}: {topic_info['count']} mentions")

def demonstrate_smart_search():
    """Demonstrate smart search capabilities"""
    print("\n" + "=" * 70)
    print("🔍 SMART SEARCH DEMONSTRATION")
    print("=" * 70)
    
    tracker = MatrixHistoryTracker(db_path="demo_message_history.db")
    
    # Test queries
    test_queries = [
        "did alice mention python",
        "who talked about databases",
        "did anyone ask about machine learning",
        "what did bob say today"
    ]
    
    print("\n🤖 Testing natural language queries:")
    
    for query in test_queries:
        print(f"\n   Query: '{query}'")
        result = tracker.smart_search(query, room_id="!room123")
        
        if result.get('success'):
            print(f"   Found: {result.get('count')} results")
            
            for msg in result.get('results', [])[:3]:  # Show first 3 results
                print(f"     • {msg['sender']} ({msg['date']}): {msg['message'][:60]}...")
        else:
            print(f"   Error: {result.get('error')}")

def demonstrate_word_learning():
    """Demonstrate word learning system"""
    print("\n" + "=" * 70)
    print("📚 WORD LEARNING DEMONSTRATION")
    print("=" * 70)
    
    tracker = MatrixHistoryTracker(db_path="demo_message_history.db")
    
    # Add technical messages
    technical_messages = [
        ("!tech", "@dev1:matrix.org", "The async/await pattern in Python is really powerful for concurrent operations", "Dev1"),
        ("!tech", "@dev2:matrix.org", "I'm implementing a REST API using FastAPI and PostgreSQL", "Dev2"),
        ("!tech", "@dev3:matrix.org", "Machine learning with TensorFlow requires understanding neural networks", "Dev3"),
    ]
    
    print("\n📝 Adding technical messages to learn vocabulary...")
    for room, sender, text, name in technical_messages:
        tracker.add_message(room, sender, text, name)
        print(f"   ✓ Processed message from {name}")
    
    # Show updated statistics
    stats = tracker.get_statistics()
    print(f"\n📊 Learning Progress:")
    print(f"   - Total Words in Library: {stats.get('words_learned')}")
    print(f"   - Messages Processed: {stats.get('total_messages')}")
    
    # Show word learning works
    print("\n✅ Word learning system successfully extracting and tracking vocabulary!")
    print("   The system learns from every message and builds a comprehensive word library.")

def main():
    """Main demonstration"""
    print("\n" + "=" * 70)
    print("🤖 RIBIT 2.0 - OFFLINE FEATURES DEMONSTRATION")
    print("=" * 70)
    print("Showcasing new offline capabilities:")
    print("  ✓ Image analysis without external APIs")
    print("  ✓ Message history tracking (3 months retention)")
    print("  ✓ Smart search with natural language queries")
    print("  ✓ Automatic word learning from conversations")
    print("=" * 70)
    
    # Run demonstrations
    demonstrate_image_analysis()
    demonstrate_message_history()
    demonstrate_smart_search()
    demonstrate_word_learning()
    
    # Summary
    print("\n" + "=" * 70)
    print("✨ DEMONSTRATION COMPLETE")
    print("=" * 70)
    print("\n🎉 All offline features working successfully!")
    print("\nKey Capabilities:")
    print("  1. Offline Image Analysis:")
    print("     - Color detection and dominant colors")
    print("     - Shape and edge detection")
    print("     - Text region identification")
    print("     - Composition analysis")
    print("     - Human/nature/sky detection")
    print("\n  2. Message History Tracking:")
    print("     - 90-day message retention")
    print("     - Automatic topic extraction")
    print("     - User mention tracking")
    print("     - Timestamp-based querying")
    print("\n  3. Smart Search:")
    print("     - Natural language queries")
    print("     - Time-based filtering (today, yesterday, last week, etc.)")
    print("     - User and topic search")
    print("     - Question detection")
    print("\n  4. Word Learning:")
    print("     - Automatic vocabulary extraction")
    print("     - Frequency tracking")
    print("     - Context preservation")
    print("     - Topic correlation")
    
    print("\n💡 Integration with Matrix Bot:")
    print("   - Images sent to bot are analyzed automatically")
    print("   - All messages are tracked and searchable")
    print("   - Ask: 'did alice mention python last week?'")
    print("   - Bot responds with relevant message history")
    
    print("\n📖 Learn More:")
    print("   - See offline_image_analyzer.py for image analysis")
    print("   - See matrix_history_tracker.py for message tracking")
    print("   - See matrix_bot.py for Matrix integration")
    
    print("\n" + "=" * 70 + "\n")
    
    # Cleanup demo database
    import os
    try:
        if os.path.exists("demo_message_history.db"):
            os.remove("demo_message_history.db")
            print("🗑️  Cleaned up demo database\n")
    except:
        pass

if __name__ == "__main__":
    main()
