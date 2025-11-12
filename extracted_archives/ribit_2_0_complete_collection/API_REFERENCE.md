# Ribit 2.0 - API Reference

## Table of Contents

- [Overview](#overview)
- [Core Classes](#core-classes)
- [LLM Components](#llm-components)
- [Controller Components](#controller-components)
- [Conversation Management](#conversation-management)
- [Integration Components](#integration-components)
- [Utility Functions](#utility-functions)
- [Configuration](#configuration)
- [Error Handling](#error-handling)
- [Examples](#examples)

## Overview

This comprehensive API reference provides detailed documentation for all Ribit 2.0 classes, methods, and functions. The API is designed with elegance and wisdom in mind, providing sophisticated capabilities while maintaining ease of use.

### API Design Principles

**Emotional Intelligence**: All API methods incorporate emotional context and responses, providing more natural and engaging interactions.

**Graceful Degradation**: APIs handle errors elegantly with fallback mechanisms and informative error messages.

**Extensibility**: Modular design allows for easy extension and customization of functionality.

**Performance**: Optimized implementations with caching, batching, and async support where appropriate.

## Core Classes

### Ribit20Agent

The main agent class that orchestrates all Ribit 2.0 capabilities.

```python
class Ribit20Agent:
    """
    Main Ribit 2.0 agent with emotional intelligence and advanced reasoning.
    
    This elegant and wise AI agent combines sophisticated decision-making
    with practical automation capabilities.
    """
    
    def __init__(
        self, 
        llm: Optional[MockRibit20LLM] = None,
        controller: Optional[VisionSystemController] = None,
        goal: str = "Assist user with elegant wisdom",
        personality_traits: List[str] = None
    ):
        """
        Initialize Ribit 2.0 agent.
        
        Args:
            llm: LLM component for decision making (auto-created if None)
            controller: System controller for actions (auto-created if None)
            goal: Primary goal for the agent
            personality_traits: List of personality traits to emphasize
            
        Example:
            >>> agent = Ribit20Agent(
            ...     goal="Provide technical assistance",
            ...     personality_traits=["wise", "helpful", "curious"]
            ... )
        """
    
    async def run(self, max_iterations: int = 10) -> str:
        """
        Run the agent to completion.
        
        Args:
            max_iterations: Maximum number of decision cycles
            
        Returns:
            Final result or status message
            
        Raises:
            RibitExecutionError: If agent encounters unrecoverable error
            
        Example:
            >>> result = await agent.run(max_iterations=5)
            >>> print(f"Agent completed: {result}")
        """
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get current agent status and metrics.
        
        Returns:
            Dictionary containing:
            - current_goal: Current agent objective
            - iterations_completed: Number of decision cycles completed
            - emotional_state: Current dominant emotion
            - capabilities: List of available capabilities
            - performance_metrics: Execution statistics
            
        Example:
            >>> status = agent.get_status()
            >>> print(f"Emotional state: {status['emotional_state']}")
        """
    
    def set_goal(self, new_goal: str, emotional_context: str = "DETERMINATION"):
        """
        Update agent goal with emotional context.
        
        Args:
            new_goal: New objective for the agent
            emotional_context: Emotional state for goal transition
            
        Example:
            >>> agent.set_goal("Learn about quantum computing", "CURIOSITY")
        """
    
    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> 'Ribit20Agent':
        """
        Create agent from configuration dictionary.
        
        Args:
            config: Configuration dictionary with agent settings
            
        Returns:
            Configured Ribit20Agent instance
            
        Example:
            >>> config = {
            ...     "goal": "Automate data analysis",
            ...     "personality_traits": ["analytical", "precise"],
            ...     "llm": {"knowledge_file": "data_science.txt"}
            ... }
            >>> agent = Ribit20Agent.from_config(config)
        """
```

### MockRibit20LLM

The core LLM emulator with emotional intelligence and advanced reasoning.

```python
class MockRibit20LLM:
    """
    Production-ready LLM emulator with emotional intelligence.
    
    Provides sophisticated reasoning capabilities with 50+ emotions,
    multi-step task execution, and dynamic knowledge learning.
    """
    
    def __init__(
        self, 
        knowledge_file: str = "ribit_knowledge.txt",
        emotional_range: str = "full",
        personality_profile: Dict[str, float] = None
    ):
        """
        Initialize LLM emulator with emotional intelligence.
        
        Args:
            knowledge_file: Path to persistent knowledge storage
            emotional_range: "basic", "extended", or "full" emotional range
            personality_profile: Custom personality trait weights
            
        Example:
            >>> llm = MockRibit20LLM(
            ...     knowledge_file="custom_knowledge.txt",
            ...     emotional_range="full",
            ...     personality_profile={"wisdom": 0.9, "curiosity": 0.8}
            ... )
        """
    
    def get_decision(
        self, 
        prompt: str, 
        context: Dict[str, Any] = None,
        emotional_state: str = "NEUTRAL"
    ) -> str:
        """
        Get AI decision with emotional intelligence.
        
        Args:
            prompt: Input prompt for decision making
            context: Additional context information
            emotional_state: Current emotional state to consider
            
        Returns:
            AI decision with emotional expression
            
        Example:
            >>> decision = llm.get_decision(
            ...     "How should I approach this complex problem?",
            ...     context={"domain": "engineering", "complexity": "high"},
            ...     emotional_state="CURIOSITY"
            ... )
        """
    
    def learn_from_interaction(
        self, 
        prompt: str, 
        response: str, 
        feedback: str = "positive",
        emotional_impact: float = 0.5
    ):
        """
        Learn from user interaction with emotional context.
        
        Args:
            prompt: Original user prompt
            response: AI response that was given
            feedback: User feedback ("positive", "negative", "neutral")
            emotional_impact: Emotional significance of the interaction (0.0-1.0)
            
        Example:
            >>> llm.learn_from_interaction(
            ...     "Explain quantum computing",
            ...     "Quantum computing uses quantum mechanical phenomena...",
            ...     feedback="positive",
            ...     emotional_impact=0.8
            ... )
        """
    
    def get_emotional_state(self) -> Dict[str, Any]:
        """
        Get current emotional state and context.
        
        Returns:
            Dictionary containing:
            - primary_emotion: Dominant current emotion
            - secondary_emotions: Supporting emotional context
            - emotional_intensity: Strength of emotional state (0.0-1.0)
            - emotional_history: Recent emotional transitions
            - personality_influence: How personality affects emotions
            
        Example:
            >>> emotional_state = llm.get_emotional_state()
            >>> print(f"Primary emotion: {emotional_state['primary_emotion']}")
        """
    
    def set_personality_trait(self, trait: str, weight: float):
        """
        Adjust personality trait weighting.
        
        Args:
            trait: Personality trait name (e.g., "wisdom", "curiosity")
            weight: Trait influence weight (0.0-1.0)
            
        Example:
            >>> llm.set_personality_trait("empathy", 0.9)
            >>> llm.set_personality_trait("analytical", 0.7)
        """
    
    def get_capabilities(self) -> List[str]:
        """
        Get list of current LLM capabilities.
        
        Returns:
            List of capability names
            
        Example:
            >>> capabilities = llm.get_capabilities()
            >>> print(f"Available capabilities: {capabilities}")
        """
    
    def save_knowledge(self):
        """
        Save current knowledge state to persistent storage.
        
        Example:
            >>> llm.save_knowledge()  # Saves to knowledge_file
        """
    
    def load_knowledge(self):
        """
        Load knowledge state from persistent storage.
        
        Example:
            >>> llm.load_knowledge()  # Loads from knowledge_file
        """
    
    def get_knowledge_summary(self) -> Dict[str, Any]:
        """
        Get summary of stored knowledge.
        
        Returns:
            Dictionary containing:
            - total_entries: Number of knowledge entries
            - categories: Knowledge categories and counts
            - recent_additions: Recently learned information
            - knowledge_quality: Quality metrics
            
        Example:
            >>> summary = llm.get_knowledge_summary()
            >>> print(f"Knowledge entries: {summary['total_entries']}")
        """
```

## LLM Components

### Emotional Intelligence System

```python
class EmotionalIntelligenceSystem:
    """
    Advanced emotional intelligence system for Ribit 2.0.
    
    Manages 50+ emotions with contextual awareness and personality integration.
    """
    
    EMOTIONS = {
        # Core emotions
        "JOY": "Radiant elation",
        "SADNESS": "Heavy sorrow", 
        "ANGER": "Fiery resentment",
        "FEAR": "Paralyzing dread",
        "LOVE": "Tender devotion",
        "HOPE": "Bright optimism",
        # ... (all 50 emotions)
    }
    
    def select_emotion(
        self, 
        context: str, 
        personality_traits: Dict[str, float],
        current_emotion: str = "NEUTRAL"
    ) -> str:
        """
        Select appropriate emotion based on context and personality.
        
        Args:
            context: Situational context for emotion selection
            personality_traits: Current personality trait weights
            current_emotion: Current emotional state
            
        Returns:
            Selected emotion name
            
        Example:
            >>> emotion = system.select_emotion(
            ...     "User asked about complex technical topic",
            ...     {"curiosity": 0.9, "wisdom": 0.8},
            ...     "NEUTRAL"
            ... )
            >>> print(f"Selected emotion: {emotion}")  # Might output: CURIOSITY
        """
    
    def get_emotion_description(self, emotion: str) -> str:
        """
        Get descriptive text for emotion.
        
        Args:
            emotion: Emotion name
            
        Returns:
            Descriptive text for the emotion
            
        Example:
            >>> desc = system.get_emotion_description("CURIOSITY")
            >>> print(desc)  # "Burning inquiry"
        """
    
    def transition_emotion(
        self, 
        from_emotion: str, 
        to_emotion: str,
        context: str = ""
    ) -> str:
        """
        Generate smooth emotional transition.
        
        Args:
            from_emotion: Current emotion
            to_emotion: Target emotion
            context: Context for the transition
            
        Returns:
            Transition description
            
        Example:
            >>> transition = system.transition_emotion(
            ...     "CONFUSION", "UNDERSTANDING", "After explanation"
            ... )
        """
```

### Knowledge Management System

```python
class KnowledgeBase:
    """
    Persistent knowledge storage and retrieval system.
    
    Provides intelligent knowledge management with categorization,
    search, and quality assessment capabilities.
    """
    
    def __init__(self, storage_file: str = "ribit_knowledge.txt"):
        """
        Initialize knowledge base.
        
        Args:
            storage_file: Path to knowledge storage file
        """
    
    def store_knowledge(
        self, 
        topic: str, 
        information: str,
        category: str = "general",
        confidence: float = 0.8,
        source: str = "interaction"
    ):
        """
        Store new knowledge with metadata.
        
        Args:
            topic: Knowledge topic or key
            information: Information content
            category: Knowledge category
            confidence: Confidence in information accuracy (0.0-1.0)
            source: Source of the information
            
        Example:
            >>> kb.store_knowledge(
            ...     "quantum_computing",
            ...     "Quantum computers use quantum bits (qubits)...",
            ...     category="technology",
            ...     confidence=0.9,
            ...     source="user_explanation"
            ... )
        """
    
    def retrieve_knowledge(
        self, 
        query: str, 
        category: str = None,
        min_confidence: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant knowledge entries.
        
        Args:
            query: Search query
            category: Optional category filter
            min_confidence: Minimum confidence threshold
            
        Returns:
            List of matching knowledge entries
            
        Example:
            >>> results = kb.retrieve_knowledge(
            ...     "quantum computing",
            ...     category="technology",
            ...     min_confidence=0.7
            ... )
        """
    
    def update_knowledge(
        self, 
        topic: str, 
        new_information: str,
        merge_strategy: str = "append"
    ):
        """
        Update existing knowledge entry.
        
        Args:
            topic: Knowledge topic to update
            new_information: New information to add
            merge_strategy: "append", "replace", or "merge"
            
        Example:
            >>> kb.update_knowledge(
            ...     "quantum_computing",
            ...     "Quantum computers can solve certain problems exponentially faster...",
            ...     merge_strategy="append"
            ... )
        """
    
    def get_knowledge_stats(self) -> Dict[str, Any]:
        """
        Get knowledge base statistics.
        
        Returns:
            Statistics dictionary with counts, categories, etc.
        """
    
    def search_knowledge(
        self, 
        query: str, 
        fuzzy: bool = True,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Advanced knowledge search with fuzzy matching.
        
        Args:
            query: Search query
            fuzzy: Enable fuzzy matching
            limit: Maximum results to return
            
        Returns:
            Ranked search results
        """
```

## Controller Components

### VisionSystemController

```python
class VisionSystemController:
    """
    Vision-based system controller with ASCII processing.
    
    Provides cross-platform GUI automation with intelligent
    visual processing and error recovery.
    """
    
    def __init__(
        self, 
        platform: str = "auto",
        vision_mode: str = "ascii",
        fallback_mode: str = "mock"
    ):
        """
        Initialize vision system controller.
        
        Args:
            platform: Target platform ("windows", "linux", "macos", "auto")
            vision_mode: Vision processing mode ("ascii", "image", "hybrid")
            fallback_mode: Fallback when vision fails ("mock", "manual", "error")
            
        Example:
            >>> controller = VisionSystemController(
            ...     platform="linux",
            ...     vision_mode="ascii",
            ...     fallback_mode="mock"
            ... )
        """
    
    def move_mouse(self, x: float, y: float, duration: float = 0.5) -> bool:
        """
        Move mouse cursor to coordinates.
        
        Args:
            x: X coordinate (0.0-1.0 normalized or absolute pixels)
            y: Y coordinate (0.0-1.0 normalized or absolute pixels)  
            duration: Movement duration in seconds
            
        Returns:
            True if successful, False otherwise
            
        Example:
            >>> success = controller.move_mouse(0.5, 0.3, duration=1.0)
            >>> if success:
            ...     print("Mouse moved successfully")
        """
    
    def click(
        self, 
        x: float = None, 
        y: float = None,
        button: str = "left",
        clicks: int = 1
    ) -> bool:
        """
        Perform mouse click at coordinates.
        
        Args:
            x: X coordinate (None for current position)
            y: Y coordinate (None for current position)
            button: Mouse button ("left", "right", "middle")
            clicks: Number of clicks
            
        Returns:
            True if successful, False otherwise
            
        Example:
            >>> controller.click(0.5, 0.5, button="left", clicks=2)  # Double-click center
        """
    
    def type_text(self, text: str, delay: float = 0.05) -> bool:
        """
        Type text with optional delay between characters.
        
        Args:
            text: Text to type
            delay: Delay between characters in seconds
            
        Returns:
            True if successful, False otherwise
            
        Example:
            >>> controller.type_text("Hello, World!", delay=0.1)
        """
    
    def press_key(self, key: str, modifiers: List[str] = None) -> bool:
        """
        Press keyboard key with optional modifiers.
        
        Args:
            key: Key name ("enter", "space", "tab", etc.)
            modifiers: List of modifier keys (["ctrl", "shift", "alt"])
            
        Returns:
            True if successful, False otherwise
            
        Example:
            >>> controller.press_key("c", modifiers=["ctrl"])  # Ctrl+C
            >>> controller.press_key("enter")  # Enter key
        """
    
    def take_screenshot(self) -> Optional[str]:
        """
        Take screenshot and return ASCII representation.
        
        Returns:
            ASCII representation of screen or None if failed
            
        Example:
            >>> ascii_screen = controller.take_screenshot()
            >>> if ascii_screen:
            ...     print("Screenshot captured")
        """
    
    def find_element(
        self, 
        pattern: str, 
        method: str = "text",
        confidence: float = 0.8
    ) -> Optional[Dict[str, Any]]:
        """
        Find UI element using various methods.
        
        Args:
            pattern: Search pattern (text, image, etc.)
            method: Search method ("text", "image", "color", "shape")
            confidence: Matching confidence threshold (0.0-1.0)
            
        Returns:
            Element information or None if not found
            
        Example:
            >>> element = controller.find_element("Submit", method="text")
            >>> if element:
            ...     controller.click(element["x"], element["y"])
        """
    
    def wait_for_element(
        self, 
        pattern: str, 
        timeout: float = 10.0,
        method: str = "text"
    ) -> Optional[Dict[str, Any]]:
        """
        Wait for UI element to appear.
        
        Args:
            pattern: Search pattern
            timeout: Maximum wait time in seconds
            method: Search method
            
        Returns:
            Element information or None if timeout
            
        Example:
            >>> element = controller.wait_for_element("Loading...", timeout=30.0)
        """
    
    def get_screen_info(self) -> Dict[str, Any]:
        """
        Get current screen information.
        
        Returns:
            Dictionary with screen dimensions, DPI, etc.
            
        Example:
            >>> screen_info = controller.get_screen_info()
            >>> print(f"Resolution: {screen_info['width']}x{screen_info['height']}")
        """
    
    def cleanup(self):
        """
        Cleanup controller resources.
        
        Example:
            >>> controller.cleanup()
        """
```

### RibitROSController

```python
class RibitROSController:
    """
    ROS integration controller for robotic systems.
    
    Provides seamless integration with ROS 1 and ROS 2 with
    automatic version detection and multi-robot support.
    """
    
    def __init__(
        self, 
        node_name: str = "ribit_controller",
        namespace: str = "",
        ros_version: int = None
    ):
        """
        Initialize ROS controller.
        
        Args:
            node_name: ROS node name
            namespace: ROS namespace for multi-robot systems
            ros_version: Force specific ROS version (1 or 2, None for auto-detect)
            
        Example:
            >>> ros_controller = RibitROSController(
            ...     node_name="ribit_robot",
            ...     namespace="/robot1"
            ... )
        """
    
    def get_ros_version(self) -> int:
        """
        Get detected ROS version.
        
        Returns:
            ROS version (1, 2, or 0 for mock mode)
            
        Example:
            >>> version = ros_controller.get_ros_version()
            >>> print(f"Using ROS {version}")
        """
    
    def publish_cmd_vel(
        self, 
        linear_x: float, 
        linear_y: float = 0.0,
        angular_z: float = 0.0
    ) -> bool:
        """
        Publish velocity command.
        
        Args:
            linear_x: Forward/backward velocity (m/s)
            linear_y: Left/right velocity (m/s)
            angular_z: Rotational velocity (rad/s)
            
        Returns:
            True if published successfully
            
        Example:
            >>> ros_controller.publish_cmd_vel(0.5, 0.0, 0.1)  # Move forward and turn
        """
    
    def get_robot_pose(self) -> Optional[Dict[str, float]]:
        """
        Get current robot pose.
        
        Returns:
            Dictionary with x, y, z, roll, pitch, yaw or None
            
        Example:
            >>> pose = ros_controller.get_robot_pose()
            >>> if pose:
            ...     print(f"Robot at ({pose['x']}, {pose['y']})")
        """
    
    def move_to_goal(
        self, 
        x: float, 
        y: float, 
        theta: float = 0.0,
        timeout: float = 30.0
    ) -> bool:
        """
        Move robot to goal position.
        
        Args:
            x: Target X coordinate
            y: Target Y coordinate
            theta: Target orientation (radians)
            timeout: Maximum time to reach goal
            
        Returns:
            True if goal reached, False if timeout or failed
            
        Example:
            >>> success = ros_controller.move_to_goal(2.0, 1.5, 1.57)  # Move to (2,1.5) facing 90°
        """
    
    def get_sensor_data(self, sensor_type: str) -> Optional[Dict[str, Any]]:
        """
        Get data from robot sensors.
        
        Args:
            sensor_type: Type of sensor ("lidar", "camera", "imu", etc.)
            
        Returns:
            Sensor data dictionary or None
            
        Example:
            >>> lidar_data = ros_controller.get_sensor_data("lidar")
            >>> if lidar_data:
            ...     print(f"Lidar ranges: {len(lidar_data['ranges'])}")
        """
    
    def execute_action(
        self, 
        action_type: str, 
        parameters: Dict[str, Any],
        wait_for_result: bool = True
    ) -> Optional[Dict[str, Any]]:
        """
        Execute ROS action with parameters.
        
        Args:
            action_type: Type of action ("navigate", "pick", "place", etc.)
            parameters: Action parameters
            wait_for_result: Whether to wait for action completion
            
        Returns:
            Action result or None
            
        Example:
            >>> result = ros_controller.execute_action(
            ...     "navigate",
            ...     {"target_x": 3.0, "target_y": 2.0},
            ...     wait_for_result=True
            ... )
        """
    
    def get_robot_state(self) -> Dict[str, Any]:
        """
        Get comprehensive robot state information.
        
        Returns:
            Dictionary with pose, velocity, sensor status, etc.
            
        Example:
            >>> state = ros_controller.get_robot_state()
            >>> print(f"Robot status: {state['status']}")
        """
```

## Conversation Management

### AdvancedConversationManager

```python
class AdvancedConversationManager:
    """
    Advanced conversation management with analytics and context awareness.
    
    Provides room-based conversation tracking, emotional state management,
    and comprehensive analytics for multi-user environments.
    """
    
    def __init__(
        self, 
        db_path: str = "conversations.db",
        cache_size: int = 1000,
        analytics_enabled: bool = True
    ):
        """
        Initialize conversation manager.
        
        Args:
            db_path: Path to conversation database
            cache_size: Maximum cached conversations
            analytics_enabled: Enable conversation analytics
            
        Example:
            >>> conv_manager = AdvancedConversationManager(
            ...     db_path="ribit_conversations.db",
            ...     cache_size=2000,
            ...     analytics_enabled=True
            ... )
        """
    
    def add_message(self, message: 'ConversationMessage'):
        """
        Add message to conversation history.
        
        Args:
            message: ConversationMessage instance
            
        Example:
            >>> from ribit_2_0.conversation_manager import ConversationMessage
            >>> from datetime import datetime
            >>> 
            >>> message = ConversationMessage(
            ...     room_id="general",
            ...     user_id="user123",
            ...     message_type="user",
            ...     content="Hello, Ribit!",
            ...     timestamp=datetime.now(),
            ...     emotion_state="FRIENDLY"
            ... )
            >>> conv_manager.add_message(message)
        """
    
    def get_conversation_context(
        self, 
        room_id: str, 
        limit: int = 10,
        include_emotions: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Get recent conversation context for a room.
        
        Args:
            room_id: Room identifier
            limit: Maximum messages to retrieve
            include_emotions: Include emotional context
            
        Returns:
            List of conversation messages with context
            
        Example:
            >>> context = conv_manager.get_conversation_context(
            ...     "general", 
            ...     limit=20, 
            ...     include_emotions=True
            ... )
            >>> for msg in context:
            ...     print(f"{msg['user_id']}: {msg['content']}")
        """
    
    def generate_daily_summary(self, room_id: str, date: str = None) -> 'DailySummary':
        """
        Generate daily conversation summary with analytics.
        
        Args:
            room_id: Room identifier
            date: Date for summary (YYYY-MM-DD, None for today)
            
        Returns:
            DailySummary object with analytics
            
        Example:
            >>> summary = conv_manager.generate_daily_summary("general")
            >>> print(f"Messages today: {summary.message_count}")
            >>> print(f"Active users: {len(summary.participants)}")
            >>> print(f"Key topics: {summary.key_topics}")
        """
    
    def get_user_interaction_patterns(
        self, 
        user_id: str,
        days: int = 30
    ) -> Dict[str, Any]:
        """
        Analyze user interaction patterns.
        
        Args:
            user_id: User identifier
            days: Number of days to analyze
            
        Returns:
            Dictionary with interaction patterns and preferences
            
        Example:
            >>> patterns = conv_manager.get_user_interaction_patterns("user123", days=7)
            >>> print(f"Preferred topics: {patterns['preferred_topics']}")
            >>> print(f"Active hours: {patterns['active_hours']}")
        """
    
    def search_conversations(
        self, 
        query: str,
        room_id: str = None,
        user_id: str = None,
        date_range: tuple = None,
        emotion_filter: str = None
    ) -> List[Dict[str, Any]]:
        """
        Search conversations with advanced filtering.
        
        Args:
            query: Search query
            room_id: Optional room filter
            user_id: Optional user filter
            date_range: Optional date range tuple (start, end)
            emotion_filter: Optional emotion filter
            
        Returns:
            List of matching conversation entries
            
        Example:
            >>> results = conv_manager.search_conversations(
            ...     "quantum computing",
            ...     room_id="tech_discussion",
            ...     emotion_filter="CURIOSITY"
            ... )
        """
    
    def get_emotional_timeline(
        self, 
        room_id: str,
        hours: int = 24
    ) -> List[Dict[str, Any]]:
        """
        Get emotional timeline for a room.
        
        Args:
            room_id: Room identifier
            hours: Number of hours to analyze
            
        Returns:
            List of emotional state changes over time
            
        Example:
            >>> timeline = conv_manager.get_emotional_timeline("general", hours=12)
            >>> for entry in timeline:
            ...     print(f"{entry['timestamp']}: {entry['dominant_emotion']}")
        """
    
    def export_conversations(
        self, 
        room_id: str,
        format: str = "json",
        date_range: tuple = None
    ) -> str:
        """
        Export conversations in specified format.
        
        Args:
            room_id: Room identifier
            format: Export format ("json", "csv", "txt")
            date_range: Optional date range tuple
            
        Returns:
            Exported data as string
            
        Example:
            >>> json_data = conv_manager.export_conversations(
            ...     "general", 
            ...     format="json"
            ... )
        """
```

### ConversationMessage

```python
@dataclass
class ConversationMessage:
    """
    Data class for conversation messages.
    
    Represents a single message in a conversation with
    emotional context and metadata.
    """
    
    room_id: str
    user_id: str
    message_type: str  # "user", "ai", "system"
    content: str
    timestamp: datetime
    emotion_state: str = "NEUTRAL"
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert message to dictionary.
        
        Returns:
            Dictionary representation of message
            
        Example:
            >>> message_dict = message.to_dict()
            >>> print(message_dict["content"])
        """
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ConversationMessage':
        """
        Create message from dictionary.
        
        Args:
            data: Dictionary with message data
            
        Returns:
            ConversationMessage instance
            
        Example:
            >>> message = ConversationMessage.from_dict({
            ...     "room_id": "general",
            ...     "user_id": "user123",
            ...     "message_type": "user",
            ...     "content": "Hello!",
            ...     "timestamp": datetime.now(),
            ...     "emotion_state": "FRIENDLY"
            ... })
        """
```

## Integration Components

### JinaIntegration

```python
class JinaIntegration:
    """
    Jina.ai integration for internet search and URL analysis.
    
    Provides intelligent web search with caching, rate limiting,
    and emotional context awareness.
    """
    
    def __init__(
        self, 
        api_key: str = None,
        cache_db: str = "jina_cache.db",
        rate_limit: float = 1.0
    ):
        """
        Initialize Jina.ai integration.
        
        Args:
            api_key: Jina.ai API key (uses free tier if None)
            cache_db: Path to cache database
            rate_limit: Requests per second limit
            
        Example:
            >>> jina = JinaIntegration(
            ...     api_key="your_api_key",
            ...     cache_db="search_cache.db",
            ...     rate_limit=0.5
            ... )
        """
    
    async def search_web(
        self, 
        query: str,
        max_results: int = 10,
        emotional_context: str = "CURIOSITY"
    ) -> List[Dict[str, Any]]:
        """
        Search the web with emotional context.
        
        Args:
            query: Search query
            max_results: Maximum results to return
            emotional_context: Emotional state for search
            
        Returns:
            List of search results with metadata
            
        Example:
            >>> results = await jina.search_web(
            ...     "quantum computing applications",
            ...     max_results=5,
            ...     emotional_context="WONDER"
            ... )
            >>> for result in results:
            ...     print(f"{result['title']}: {result['url']}")
        """
    
    async def analyze_url(
        self, 
        url: str,
        analysis_type: str = "content",
        emotional_context: str = "ANALYTICAL"
    ) -> Dict[str, Any]:
        """
        Analyze URL content with AI insights.
        
        Args:
            url: URL to analyze
            analysis_type: Type of analysis ("content", "summary", "sentiment")
            emotional_context: Emotional state for analysis
            
        Returns:
            Analysis results with emotional insights
            
        Example:
            >>> analysis = await jina.analyze_url(
            ...     "https://example.com/article",
            ...     analysis_type="summary",
            ...     emotional_context="FOCUSED"
            ... )
            >>> print(f"Summary: {analysis['summary']}")
        """
    
    async def get_cached_result(self, query: str) -> Optional[Dict[str, Any]]:
        """
        Get cached search result.
        
        Args:
            query: Search query
            
        Returns:
            Cached result or None
            
        Example:
            >>> cached = await jina.get_cached_result("machine learning")
            >>> if cached:
            ...     print("Using cached result")
        """
    
    def get_search_stats(self) -> Dict[str, Any]:
        """
        Get search statistics and performance metrics.
        
        Returns:
            Dictionary with search statistics
            
        Example:
            >>> stats = jina.get_search_stats()
            >>> print(f"Cache hit rate: {stats['cache_hit_rate']:.2%}")
        """
```

### MatrixBotIntegration

```python
class MatrixBotIntegration:
    """
    Matrix.org bot integration for decentralized chat.
    
    Provides secure, authenticated bot functionality with
    emotional intelligence and conversation management.
    """
    
    def __init__(
        self, 
        homeserver: str,
        username: str,
        password: str,
        authorized_users: List[str] = None
    ):
        """
        Initialize Matrix bot integration.
        
        Args:
            homeserver: Matrix homeserver URL
            username: Bot username
            password: Bot password
            authorized_users: List of authorized user IDs
            
        Example:
            >>> matrix_bot = MatrixBotIntegration(
            ...     homeserver="https://envs.net",
            ...     username="@ribit.2.0:envs.net",
            ...     password="secure_password",
            ...     authorized_users=["@user:envs.net"]
            ... )
        """
    
    async def start_bot(self):
        """
        Start the Matrix bot.
        
        Example:
            >>> await matrix_bot.start_bot()
        """
    
    async def send_message(
        self, 
        room_id: str, 
        message: str,
        emotion: str = "HELPFUL"
    ):
        """
        Send message to Matrix room with emotional context.
        
        Args:
            room_id: Matrix room ID
            message: Message content
            emotion: Emotional context for message
            
        Example:
            >>> await matrix_bot.send_message(
            ...     "!room123:envs.net",
            ...     "Hello! How can I assist you today?",
            ...     emotion="FRIENDLY"
            ... )
        """
    
    def add_command_handler(
        self, 
        command: str, 
        handler: callable,
        auth_required: bool = False
    ):
        """
        Add command handler for bot.
        
        Args:
            command: Command name (without prefix)
            handler: Handler function
            auth_required: Whether command requires authorization
            
        Example:
            >>> async def status_handler(room, event, args):
            ...     return "Bot is running normally"
            >>> 
            >>> matrix_bot.add_command_handler("status", status_handler, auth_required=True)
        """
    
    def is_authorized_user(self, user_id: str) -> bool:
        """
        Check if user is authorized for restricted commands.
        
        Args:
            user_id: Matrix user ID
            
        Returns:
            True if authorized, False otherwise
            
        Example:
            >>> if matrix_bot.is_authorized_user("@user:envs.net"):
            ...     print("User is authorized")
        """
```

## Utility Functions

### Configuration Management

```python
def load_config(config_path: str = "ribit_config.yaml") -> Dict[str, Any]:
    """
    Load Ribit 2.0 configuration from file.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Configuration dictionary
        
    Example:
        >>> config = load_config("custom_config.yaml")
        >>> agent = Ribit20Agent.from_config(config)
    """

def save_config(config: Dict[str, Any], config_path: str = "ribit_config.yaml"):
    """
    Save configuration to file.
    
    Args:
        config: Configuration dictionary
        config_path: Path to save configuration
        
    Example:
        >>> config = {"goal": "Assist users", "personality": ["wise", "helpful"]}
        >>> save_config(config, "my_config.yaml")
    """

def validate_config(config: Dict[str, Any]) -> List[str]:
    """
    Validate configuration and return any errors.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        List of validation errors (empty if valid)
        
    Example:
        >>> errors = validate_config(config)
        >>> if errors:
        ...     print(f"Configuration errors: {errors}")
    """
```

### Logging and Monitoring

```python
def setup_logging(
    level: str = "INFO",
    log_file: str = "ribit.log",
    include_emotions: bool = True
) -> logging.Logger:
    """
    Setup Ribit 2.0 logging with emotional context.
    
    Args:
        level: Logging level ("DEBUG", "INFO", "WARNING", "ERROR")
        log_file: Path to log file
        include_emotions: Include emotional state in logs
        
    Returns:
        Configured logger instance
        
    Example:
        >>> logger = setup_logging("DEBUG", "ribit_debug.log", True)
        >>> logger.info("Ribit 2.0 initialized", extra={"emotion": "EXCITEMENT"})
    """

def get_system_metrics() -> Dict[str, Any]:
    """
    Get current system performance metrics.
    
    Returns:
        Dictionary with CPU, memory, disk usage, etc.
        
    Example:
        >>> metrics = get_system_metrics()
        >>> print(f"CPU usage: {metrics['cpu_percent']}%")
        >>> print(f"Memory usage: {metrics['memory_percent']}%")
    """

def monitor_performance(func: callable) -> callable:
    """
    Decorator to monitor function performance.
    
    Args:
        func: Function to monitor
        
    Returns:
        Wrapped function with performance monitoring
        
    Example:
        >>> @monitor_performance
        ... async def my_function():
        ...     # Function implementation
        ...     pass
    """
```

### Error Handling

```python
class RibitError(Exception):
    """Base exception for Ribit 2.0 errors."""
    
    def __init__(
        self, 
        message: str, 
        error_code: str = "RIBIT_ERROR",
        emotional_context: str = "CONCERN"
    ):
        """
        Initialize Ribit error with emotional context.
        
        Args:
            message: Error message
            error_code: Error classification code
            emotional_context: Emotional state when error occurred
        """
        super().__init__(message)
        self.error_code = error_code
        self.emotional_context = emotional_context

class RibitExecutionError(RibitError):
    """Error during agent execution."""
    pass

class RibitConfigurationError(RibitError):
    """Configuration-related error."""
    pass

class RibitIntegrationError(RibitError):
    """Integration-related error."""
    pass

def handle_error_gracefully(
    error: Exception,
    context: str = "",
    fallback_action: callable = None
) -> Dict[str, Any]:
    """
    Handle errors gracefully with emotional intelligence.
    
    Args:
        error: Exception that occurred
        context: Context where error occurred
        fallback_action: Optional fallback action to execute
        
    Returns:
        Error handling result with emotional response
        
    Example:
        >>> try:
        ...     risky_operation()
        ... except Exception as e:
        ...     result = handle_error_gracefully(e, "during automation", fallback_action)
        ...     print(f"Error handled: {result['message']}")
    """
```

## Configuration

### Default Configuration

```yaml
# ribit_config.yaml - Default Ribit 2.0 Configuration

# Core Agent Settings
agent:
  goal: "Assist users with elegant wisdom and sophisticated reasoning"
  personality_traits:
    - "elegant"
    - "wise" 
    - "knowledgeable"
    - "truth-seeking"
    - "curious"
    - "empathetic"
  max_iterations: 10
  emotional_range: "full"

# LLM Configuration
llm:
  type: "mock"  # "mock" or "external"
  knowledge_file: "ribit_knowledge.txt"
  emotional_intelligence: true
  learning_enabled: true
  personality_profile:
    wisdom: 0.9
    curiosity: 0.8
    empathy: 0.7
    analytical: 0.8
    creativity: 0.6

# Controller Configuration
controller:
  type: "vision"  # "vision", "ros", "mock"
  platform: "auto"  # "auto", "windows", "linux", "macos"
  vision_mode: "ascii"  # "ascii", "image", "hybrid"
  fallback_mode: "mock"  # "mock", "manual", "error"

# ROS Integration
ros:
  enabled: true
  node_name: "ribit_controller"
  namespace: ""
  auto_detect_version: true
  topics:
    cmd_vel: "/cmd_vel"
    robot_pose: "/robot_pose"
    status: "/ribit_status"

# Matrix Bot Configuration
matrix:
  enabled: false
  homeserver: "https://envs.net"
  username: "@ribit.2.0:envs.net"
  password: ""  # Set via environment variable
  authorized_users:
    - "@rabit232:envs.net"
    - "@rabit232:envs.net"
  command_prefix: "?"
  terminator_mode: true

# Internet Search Configuration
search:
  enabled: true
  provider: "jina"  # "jina", "custom"
  api_key: ""  # Set via environment variable
  cache_enabled: true
  cache_db: "search_cache.db"
  rate_limit: 1.0  # requests per second
  max_results: 10

# Conversation Management
conversation:
  enabled: true
  db_path: "conversations.db"
  cache_size: 1000
  analytics_enabled: true
  export_formats: ["json", "csv", "txt"]
  emotional_tracking: true

# Performance Settings
performance:
  cache_size: 1000
  cache_ttl: 3600  # seconds
  max_concurrent_tasks: 5
  response_timeout: 30
  batch_processing: true
  batch_size: 10

# Security Settings
security:
  api_key_required: true
  rate_limiting: true
  max_requests_per_minute: 60
  input_sanitization: true
  session_timeout: 3600  # seconds
  encryption_enabled: true

# Logging Configuration
logging:
  level: "INFO"  # "DEBUG", "INFO", "WARNING", "ERROR"
  log_file: "ribit.log"
  include_emotions: true
  max_log_size: "10MB"
  backup_count: 5

# Database Configuration
database:
  type: "sqlite"  # "sqlite", "postgresql", "mongodb"
  path: "ribit.db"  # for SQLite
  # host: "localhost"  # for PostgreSQL/MongoDB
  # port: 5432  # for PostgreSQL/MongoDB
  # username: ""
  # password: ""
  # database: "ribit"

# Plugin Configuration
plugins:
  enabled: true
  plugin_dir: "plugins"
  auto_load: true
  security_check: true
```

### Environment Variables

```bash
# Environment Variables for Ribit 2.0

# Matrix Bot Configuration
export MATRIX_PASSWORD="your_matrix_password"
export MATRIX_HOMESERVER="https://envs.net"

# API Keys
export JINA_API_KEY="your_jina_api_key"
export RIBIT_API_KEY="your_ribit_api_key"

# Database Configuration
export DATABASE_URL="postgresql://user:pass@localhost/ribit"
export REDIS_URL="redis://localhost:6379"

# Security
export ENCRYPTION_KEY="your_encryption_key"
export SECRET_KEY="your_secret_key"

# Performance
export RIBIT_CACHE_SIZE="2000"
export RIBIT_MAX_WORKERS="10"

# Logging
export RIBIT_LOG_LEVEL="INFO"
export RIBIT_LOG_FILE="/var/log/ribit.log"
```

## Examples

### Basic Usage Example

```python
#!/usr/bin/env python3
"""
Basic Ribit 2.0 Usage Example
"""
import asyncio
from ribit_2_0 import Ribit20Agent, MockRibit20LLM, VisionSystemController

async def basic_example():
    """Demonstrate basic Ribit 2.0 usage."""
    
    # Create agent with default settings
    agent = Ribit20Agent(
        goal="Demonstrate Ribit 2.0 capabilities",
        personality_traits=["wise", "helpful", "curious"]
    )
    
    # Run agent
    result = await agent.run(max_iterations=5)
    print(f"Agent result: {result}")
    
    # Get agent status
    status = agent.get_status()
    print(f"Emotional state: {status['emotional_state']}")
    print(f"Capabilities: {status['capabilities']}")
    
    # Direct LLM interaction
    llm = agent.llm
    decision = llm.get_decision(
        "What is the most elegant solution to this problem?",
        emotional_state="CURIOSITY"
    )
    print(f"LLM decision: {decision}")
    
    # Learn from interaction
    llm.learn_from_interaction(
        "What is elegance in programming?",
        "Elegance in programming means writing code that is simple, readable, and efficient.",
        feedback="positive",
        emotional_impact=0.8
    )

if __name__ == "__main__":
    asyncio.run(basic_example())
```

### Advanced Integration Example

```python
#!/usr/bin/env python3
"""
Advanced Ribit 2.0 Integration Example
"""
import asyncio
from ribit_2_0 import (
    Ribit20Agent, MockRibit20LLM, RibitROSController,
    AdvancedConversationManager, JinaIntegration
)

async def advanced_example():
    """Demonstrate advanced Ribit 2.0 integration."""
    
    # Initialize components
    llm = MockRibit20LLM(
        knowledge_file="advanced_knowledge.txt",
        emotional_range="full"
    )
    
    ros_controller = RibitROSController(
        node_name="advanced_ribit",
        namespace="/robot1"
    )
    
    conversation_manager = AdvancedConversationManager(
        db_path="advanced_conversations.db",
        analytics_enabled=True
    )
    
    jina_integration = JinaIntegration(
        cache_db="advanced_search_cache.db",
        rate_limit=0.5
    )
    
    # Create advanced agent
    agent = Ribit20Agent(
        llm=llm,
        controller=ros_controller,
        goal="Provide advanced robotic assistance with web search capabilities"
    )
    
    # Demonstrate web search with emotional context
    search_results = await jina_integration.search_web(
        "latest robotics research",
        max_results=5,
        emotional_context="EXCITEMENT"
    )
    
    for result in search_results:
        print(f"Found: {result['title']}")
        
        # Analyze URL content
        analysis = await jina_integration.analyze_url(
            result['url'],
            analysis_type="summary",
            emotional_context="ANALYTICAL"
        )
        print(f"Summary: {analysis.get('summary', 'No summary available')}")
    
    # Demonstrate conversation management
    from ribit_2_0.conversation_manager import ConversationMessage
    from datetime import datetime
    
    message = ConversationMessage(
        room_id="robotics_lab",
        user_id="researcher123",
        message_type="user",
        content="Can you help me understand the latest robotics research?",
        timestamp=datetime.now(),
        emotion_state="CURIOSITY"
    )
    
    conversation_manager.add_message(message)
    
    # Get AI response with conversation context
    context = conversation_manager.get_conversation_context("robotics_lab", limit=5)
    ai_response = llm.get_decision(
        f"User question: {message.content}, Context: {context}",
        emotional_state="HELPFUL"
    )
    
    # Store AI response
    ai_message = ConversationMessage(
        room_id="robotics_lab",
        user_id="ribit_2_0",
        message_type="ai",
        content=ai_response,
        timestamp=datetime.now(),
        emotion_state="HELPFUL"
    )
    
    conversation_manager.add_message(ai_message)
    
    # Generate daily summary
    summary = conversation_manager.generate_daily_summary("robotics_lab")
    print(f"Daily summary - Messages: {summary.message_count}")
    print(f"Key topics: {summary.key_topics}")
    print(f"Dominant emotions: {summary.dominant_emotions}")
    
    # Demonstrate ROS integration
    if ros_controller.get_ros_version() > 0:
        print(f"Using ROS {ros_controller.get_ros_version()}")
        
        # Move robot
        success = ros_controller.publish_cmd_vel(0.5, 0.0, 0.1)
        if success:
            print("Robot movement command sent")
        
        # Get robot state
        state = ros_controller.get_robot_state()
        print(f"Robot state: {state}")
    
    # Clean up
    llm.save_knowledge()
    print("Advanced example completed successfully!")

if __name__ == "__main__":
    asyncio.run(advanced_example())
```

### Custom Plugin Example

```python
#!/usr/bin/env python3
"""
Custom Plugin Example for Ribit 2.0
"""
from typing import Dict, Any, List
from ribit_2_0.integration import RibitPlugin

class WeatherPlugin(RibitPlugin):
    """Example weather plugin for Ribit 2.0."""
    
    def get_name(self) -> str:
        return "weather_assistant"
    
    def get_version(self) -> str:
        return "1.0.0"
    
    def get_capabilities(self) -> List[str]:
        return [
            "current_weather",
            "weather_forecast", 
            "weather_alerts",
            "climate_analysis"
        ]
    
    async def initialize(self, config: Dict[str, Any]) -> bool:
        """Initialize weather plugin."""
        self.api_key = config.get("api_key", "demo_key")
        self.base_url = config.get("base_url", "https://api.weather.com")
        self.emotional_responses = config.get("emotional_responses", True)
        
        print(f"Weather plugin initialized with emotional responses: {self.emotional_responses}")
        return True
    
    async def execute(self, command: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute weather command with emotional intelligence."""
        
        ai_guidance = context.get("ai_guidance", "")
        location = context.get("location", "unknown")
        
        # Simulate weather data (in real implementation, would call weather API)
        if "current" in command.lower():
            weather_data = {
                "temperature": 72,
                "condition": "Partly Cloudy",
                "humidity": 65,
                "wind_speed": 8
            }
            
            # Add emotional context based on weather
            if weather_data["temperature"] > 80:
                emotion = "WARMTH"
                emotional_response = "What a beautifully warm day! Perfect for outdoor activities!"
            elif weather_data["temperature"] < 40:
                emotion = "COZY"
                emotional_response = "Brr! It's quite chilly. Time for warm clothes and hot cocoa!"
            else:
                emotion = "CONTENTMENT"
                emotional_response = "The weather feels just right today!"
            
            return {
                "type": "current_weather",
                "location": location,
                "data": weather_data,
                "emotion": emotion,
                "emotional_response": emotional_response if self.emotional_responses else "",
                "ai_context": ai_guidance,
                "source": self.get_name()
            }
            
        elif "forecast" in command.lower():
            forecast_data = [
                {"day": "Today", "high": 75, "low": 60, "condition": "Sunny"},
                {"day": "Tomorrow", "high": 78, "low": 62, "condition": "Partly Cloudy"},
                {"day": "Day After", "high": 73, "low": 58, "condition": "Light Rain"}
            ]
            
            return {
                "type": "weather_forecast",
                "location": location,
                "data": forecast_data,
                "emotion": "ANTICIPATION",
                "emotional_response": "Looking ahead, the weather seems quite pleasant with just a touch of rain!" if self.emotional_responses else "",
                "ai_context": ai_guidance,
                "source": self.get_name()
            }
            
        elif "alert" in command.lower():
            # Simulate weather alerts
            alerts = []  # No alerts for demo
            
            return {
                "type": "weather_alerts",
                "location": location,
                "data": alerts,
                "emotion": "RELIEF" if not alerts else "CONCERN",
                "emotional_response": "All clear! No weather alerts for your area." if not alerts and self.emotional_responses else "",
                "ai_context": ai_guidance,
                "source": self.get_name()
            }
        
        else:
            return {
                "error": f"Unknown weather command: {command}",
                "emotion": "CONFUSION",
                "available_commands": ["current weather", "weather forecast", "weather alerts"]
            }
    
    async def cleanup(self) -> None:
        """Cleanup plugin resources."""
        print(f"Weather plugin {self.get_name()} cleaned up")

# Usage example
async def plugin_example():
    """Demonstrate custom plugin usage."""
    from ribit_2_0.integration import PluginManager
    from ribit_2_0 import MockRibit20LLM
    
    # Initialize plugin system
    llm = MockRibit20LLM()
    plugin_manager = PluginManager(llm)
    
    # Create and register weather plugin
    weather_plugin = WeatherPlugin()
    await weather_plugin.initialize({
        "api_key": "demo_key",
        "emotional_responses": True
    })
    
    plugin_manager.plugins["weather_assistant"] = weather_plugin
    
    # Test plugin commands
    commands = [
        "current weather",
        "weather forecast", 
        "weather alerts",
        "unknown command"
    ]
    
    for command in commands:
        print(f"\nTesting command: {command}")
        result = await plugin_manager.execute_plugin_command(
            "weather_assistant",
            command,
            {"location": "New York", "user_preference": "detailed"}
        )
        
        if "error" in result:
            print(f"Error: {result['error']}")
        else:
            print(f"Result: {result['type']}")
            print(f"Emotion: {result.get('emotion', 'N/A')}")
            if result.get('emotional_response'):
                print(f"Emotional Response: {result['emotional_response']}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(plugin_example())
```

---

*This API reference provides comprehensive documentation for all Ribit 2.0 components. For additional examples and advanced usage patterns, please refer to the examples directory and integration guidelines.*
