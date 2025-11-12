# Contributing to Ribit 2.0

Thank you for your interest in contributing to Ribit 2.0! This document provides guidelines and information for contributors who want to help improve this elegant AI agent with emotional intelligence and advanced automation capabilities.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Guidelines](#contributing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)
- [Development Standards](#development-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation Standards](#documentation-standards)
- [Community](#community)

## Code of Conduct

Ribit 2.0 follows the principles of elegance, wisdom, and truth-seeking that define our AI agent. We expect all contributors to maintain these values in their interactions:

**Elegance**: Write clean, readable code and communicate respectfully with other contributors.

**Wisdom**: Share knowledge generously and learn from others with humility and curiosity.

**Truth-seeking**: Be honest about capabilities and limitations, and strive for accuracy in all contributions.

**Inclusivity**: Welcome contributors of all backgrounds and experience levels with patience and support.

## Getting Started

### Prerequisites

Before contributing, ensure you have the following installed:

```bash
# Python 3.8 or higher
python3 --version

# Git for version control
git --version

# Virtual environment (recommended)
python3 -m venv ribit_dev
source ribit_dev/bin/activate  # Linux/macOS
# ribit_dev\Scripts\activate  # Windows
```

### Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/ribit.2.0.git
cd ribit.2.0

# Add upstream remote
git remote add upstream https://github.com/rabit232/ribit.2.0.git
```

## Development Setup

### Installation for Development

```bash
# Install in development mode
pip install -e .

# Install development dependencies
pip install -r requirements.txt
pip install pytest pytest-asyncio black flake8 mypy

# Optional: Install ROS for full functionality
pip install rclpy  # ROS 2
```

### Environment Configuration

Create a `.env` file for development:

```bash
# Development configuration
RIBIT_DEBUG=true
RIBIT_LOG_LEVEL=DEBUG
MATRIX_HOMESERVER=https://matrix.envs.net
JINA_SEARCH_CACHE_TTL=3600
```

### Verify Installation

```bash
# Test basic functionality
python3 -c "
from ribit_2_0 import MockRibit20LLM
llm = MockRibit20LLM()
print('✅ Development setup successful!')
print(f'Capabilities: {len(llm.get_capabilities())}')
llm.close()
"
```

## Contributing Guidelines

### Areas for Contribution

We welcome contributions in several key areas:

**Core AI Development**: Enhance the MockRibit20LLM emulator with more sophisticated reasoning, improved emotional intelligence, and advanced decision-making algorithms.

**Robotics Integration**: Expand ROS compatibility, add support for new robot platforms, and improve real-time performance for robotic applications.

**Internet Integration**: Enhance Jina.ai search capabilities, improve URL content analysis, and add support for additional web services and APIs.

**Conversation Management**: Improve the advanced conversation system with better analytics, enhanced context awareness, and more sophisticated user interaction patterns.

**Performance Optimization**: Optimize database queries, improve caching strategies, and enhance overall system performance for production deployments.

**Documentation**: Create tutorials, improve API documentation, add examples, and enhance user guides for better accessibility.

### Contribution Types

**Bug Fixes**: Address issues in existing functionality with clear problem identification and solution implementation.

**Feature Enhancements**: Improve existing features with additional capabilities, better performance, or enhanced user experience.

**New Features**: Add completely new functionality that aligns with Ribit 2.0's vision of elegant AI automation.

**Documentation**: Improve existing documentation or create new guides, tutorials, and API references.

**Testing**: Add test coverage, create integration tests, and improve testing infrastructure.

**Examples**: Create new example scripts demonstrating specific use cases or integration scenarios.

## Pull Request Process

### Before Submitting

1. **Sync with upstream**: Ensure your fork is up-to-date with the latest changes
2. **Create feature branch**: Use descriptive branch names like `feature/enhanced-emotions` or `fix/matrix-bot-auth`
3. **Test thoroughly**: Run all tests and verify your changes work as expected
4. **Update documentation**: Include relevant documentation updates with your changes
5. **Follow code style**: Ensure your code follows the established patterns and conventions

### Submission Steps

```bash
# Sync with upstream
git fetch upstream
git checkout master
git merge upstream/master

# Create feature branch
git checkout -b feature/your-feature-name

# Make your changes
# ... develop and test ...

# Commit with descriptive messages
git add .
git commit -m "✨ Add enhanced emotional responses for technical queries

- Implement 15 new emotions for programming and database tasks
- Add context-aware emotion selection based on query complexity
- Enhance response quality with more nuanced emotional expressions
- Include comprehensive tests for new emotional capabilities"

# Push to your fork
git push origin feature/your-feature-name
```

### Pull Request Template

When creating a pull request, please include:

**Description**: Clear explanation of what your changes accomplish and why they are needed.

**Changes Made**: List of specific modifications, additions, or improvements included in the PR.

**Testing**: Description of how you tested your changes and any new test cases added.

**Documentation**: Note any documentation updates or new documentation created.

**Breaking Changes**: Clearly identify any changes that might affect existing functionality.

**Related Issues**: Reference any GitHub issues that this PR addresses or relates to.

## Issue Reporting

### Bug Reports

When reporting bugs, please include:

**Environment Information**: Python version, operating system, ROS version (if applicable), and relevant dependencies.

**Steps to Reproduce**: Clear, step-by-step instructions to reproduce the issue.

**Expected Behavior**: What you expected to happen.

**Actual Behavior**: What actually happened, including error messages and stack traces.

**Additional Context**: Any additional information that might help diagnose the issue.

### Feature Requests

For feature requests, please provide:

**Use Case**: Describe the specific scenario where this feature would be valuable.

**Proposed Solution**: Your ideas for how this feature might be implemented.

**Alternatives Considered**: Other approaches you've considered and why they might not be suitable.

**Impact**: How this feature would benefit the Ribit 2.0 community and ecosystem.

## Development Standards

### Code Style

Ribit 2.0 follows Python best practices with emphasis on readability and maintainability:

```python
# Use clear, descriptive variable names
emotional_response_generator = EmotionalResponseGenerator()
conversation_context = manager.get_recent_context(limit=10)

# Include comprehensive docstrings
def analyze_emotional_context(message: str, history: List[str]) -> Dict[str, float]:
    """
    Analyze the emotional context of a message based on conversation history.
    
    Args:
        message: The current message to analyze
        history: Recent conversation history for context
        
    Returns:
        Dictionary mapping emotion names to confidence scores
        
    Raises:
        ValueError: If message is empty or history is malformed
    """
    pass

# Use type hints for better code clarity
from typing import Dict, List, Optional, Union

def process_search_results(
    results: List[Dict[str, str]], 
    emotion_context: Optional[str] = None
) -> Dict[str, Union[str, List[str]]]:
    """Process search results with emotional intelligence."""
    pass
```

### Error Handling

Implement robust error handling with graceful degradation:

```python
try:
    search_results = await jina_engine.search_web(query)
except ConnectionError as e:
    logger.warning(f"Search service unavailable: {e}")
    return self._generate_fallback_response(query)
except Exception as e:
    logger.error(f"Unexpected error in search: {e}")
    return "I encountered an unexpected issue while searching. Please try again."
```

### Logging

Use structured logging for better debugging and monitoring:

```python
import logging

logger = logging.getLogger(__name__)

def process_user_request(request: str) -> str:
    logger.info(f"Processing user request: {request[:50]}...")
    
    try:
        response = self._generate_response(request)
        logger.debug(f"Generated response length: {len(response)}")
        return response
    except Exception as e:
        logger.error(f"Failed to process request: {e}", exc_info=True)
        raise
```

## Testing Guidelines

### Test Structure

Organize tests logically with clear naming conventions:

```python
import pytest
from ribit_2_0.mock_llm_wrapper import MockRibit20LLM

class TestMockRibit20LLM:
    """Test suite for the MockRibit20LLM emulator."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.llm = MockRibit20LLM("test_knowledge.txt")
    
    def teardown_method(self):
        """Clean up after each test method."""
        self.llm.close()
    
    def test_basic_decision_making(self):
        """Test basic decision making functionality."""
        response = self.llm.get_decision("Hello, introduce yourself")
        assert "Ribit" in response
        assert len(response) > 50
    
    def test_emotional_responses(self):
        """Test emotional intelligence in responses."""
        response = self.llm.get_decision("I'm feeling sad today")
        emotional_words = ["empathy", "understanding", "support", "care"]
        assert any(word in response.lower() for word in emotional_words)
```

### Integration Tests

Create integration tests for complex workflows:

```python
@pytest.mark.asyncio
async def test_matrix_bot_integration():
    """Test Matrix bot integration with conversation management."""
    # Setup test environment
    bot = RibitMatrixBot("test_server", "test_user", "test_pass")
    
    # Test message processing
    test_message = "Search for Python tutorials"
    response = await bot.process_message(test_message, "test_room", "test_user")
    
    # Verify response quality
    assert len(response) > 100
    assert "search" in response.lower()
    assert any(emotion in response.upper() for emotion in ["CURIOSITY", "EXCITEMENT"])
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=ribit_2_0

# Run specific test categories
pytest tests/test_llm_wrapper.py
pytest tests/test_integration.py

# Run with verbose output
pytest -v
```

## Documentation Standards

### API Documentation

Document all public APIs with comprehensive docstrings:

```python
class AdvancedConversationManager:
    """
    Advanced conversation management with emotional intelligence and analytics.
    
    This class provides sophisticated conversation tracking, user interaction
    pattern analysis, and emotional context management for AI agents.
    
    Attributes:
        db_path: Path to the SQLite database for conversation storage
        cache_size: Maximum number of conversations to keep in memory
        
    Example:
        >>> manager = AdvancedConversationManager()
        >>> message = ConversationMessage(
        ...     room_id="!example:matrix.org",
        ...     user_id="@user:matrix.org",
        ...     content="Hello Ribit!",
        ...     emotion_state="CURIOSITY"
        ... )
        >>> message_id = manager.add_message(message)
    """
    
    def get_conversation_context(
        self, 
        room_id: str, 
        limit: int = 50,
        min_relevance: float = 0.0
    ) -> List[Dict[str, Any]]:
        """
        Retrieve conversation context with relevance filtering.
        
        Args:
            room_id: Unique identifier for the conversation room
            limit: Maximum number of messages to retrieve
            min_relevance: Minimum relevance score for message inclusion
            
        Returns:
            List of conversation messages with metadata, sorted by relevance
            and recency. Each message includes content, emotion state, and
            contextual information.
            
        Raises:
            ValueError: If room_id is empty or limit is negative
            DatabaseError: If database connection fails
            
        Example:
            >>> context = manager.get_conversation_context(
            ...     room_id="!example:matrix.org",
            ...     limit=20,
            ...     min_relevance=0.3
            ... )
            >>> print(f"Retrieved {len(context)} relevant messages")
        """
        pass
```

### User Guides

Create clear, step-by-step guides for common use cases:

```markdown
## Setting Up Ribit 2.0 for Robot Control

This guide walks you through configuring Ribit 2.0 for robotic applications with ROS integration.

### Prerequisites

Before beginning, ensure you have a working ROS installation and a compatible robot platform.

### Step 1: Install Dependencies

Install the required ROS packages for your robot platform:

```bash
# For TurtleBot 3
sudo apt install ros-humble-turtlebot3*

# For Universal Robots
sudo apt install ros-humble-ur-robot-driver
```

### Step 2: Configure Ribit 2.0

Create a configuration file for your robot setup:

```python
# robot_config.py
from ribit_2_0 import RibitROSController

controller = RibitROSController(
    node_name="ribit_robot_controller",
    namespace="/robot1"
)
```
```

## Community

### Communication Channels

**GitHub Issues**: Primary channel for bug reports, feature requests, and technical discussions.

**GitHub Discussions**: Community forum for questions, ideas, and general discussions about Ribit 2.0.

**Pull Request Reviews**: Collaborative code review process for all contributions.

### Recognition

Contributors are recognized in several ways:

**Changelog**: All significant contributions are acknowledged in the project changelog.

**README**: Major contributors are listed in the project acknowledgments.

**Release Notes**: Feature contributors are mentioned in release announcements.

### Mentorship

New contributors are welcome and supported through:

**Good First Issues**: Specially labeled issues suitable for newcomers to the project.

**Code Review Feedback**: Constructive feedback and guidance during the pull request process.

**Documentation Support**: Help with understanding the codebase and contribution process.

## Getting Help

If you need assistance with contributing:

**Documentation**: Start with the comprehensive documentation in the repository.

**Examples**: Review the examples directory for practical implementation patterns.

**Issues**: Search existing issues for similar questions or problems.

**Discussions**: Use GitHub Discussions for broader questions about the project.

## Thank You

Your contributions help make Ribit 2.0 a more elegant, wise, and capable AI agent. Whether you're fixing a small bug, adding a major feature, or improving documentation, every contribution is valued and appreciated.

Together, we're building an AI system that embodies the principles of elegance, wisdom, and truth-seeking while providing practical automation capabilities for the robotics and AI community.

**Welcome to the Ribit 2.0 community!** 🤖✨
