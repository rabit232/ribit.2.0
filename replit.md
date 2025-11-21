# Ribit 2.0 - Replit Project Documentation

## Overview
Ribit 2.0 is an advanced AI agent designed for GUI automation, robotic control, and intelligent conversation. It features a production-ready LLM emulator, comprehensive knowledge management, and a sophisticated personality system. The project's purpose is to provide an AI agent for automation, robotics, and intelligent conversation, delivered as a Python console application/library.

## User Preferences
*To be added as preferences are discovered*

## System Architecture

### UI/UX Decisions
The project currently utilizes an interactive console-based demo (`demo.py`) as its primary interface. This design choice is optimal for exploring Ribit's capabilities within the Replit environment without requiring complex GUI or web frontend setups.

### Technical Implementations
- **AI Core**: Features a mock LLM emulator for AI decision-making without external services, knowledge management for persistent learning, and a sophisticated personality system for conversation.
- **Task Execution**: Capable of multi-step reasoning and automation, including GUI automation (with mock mode fallback in Replit).
- **Offline Features**: Includes image analysis (color, shape, text, composition, scene classification) and a Matrix message history tracker with smart search and word learning, all fully offline.
- **Matrix Bot**: Integrates with the Matrix protocol for decentralized chat automation, including bot management via a unified CLI.
- **Persistence**: Knowledge is stored in flat files (e.g., `knowledge.txt`, `knowledge.json`) for simplicity and portability, with conversation history managed in memory per session and persistently via file storage.

### Feature Specifications
- **Mock LLM Emulator**: Provides production-ready AI decision-making.
- **Knowledge Management**: Supports persistent learning and knowledge retrieval.
- **Personality System**: Enables sophisticated conversation capabilities.
- **Task Execution**: Offers automation capabilities, including GUI automation where supported.
- **Multi-step Reasoning**: Facilitates complex task breakdown and execution.
- **ROS Integration**: Provides compatibility with Robot Operating System (optional).
- **Matrix Bot**: Supports decentralized chat automation.
- **Offline Image Analysis**: Performs color detection, shape/edge recognition, text region detection, composition analysis, and scene classification without external APIs.
- **Matrix Message History Tracker**: Retains 90 days of messages, offers smart search, and extracts vocabulary.

### System Design Choices
- **Console-based AI Agent Library**: The core design is a Python library with a console-based interface, not a web application.
- **Mock Mode by Default**: Due to Replit's environment limitations (lack of X11 display server), GUI automation runs in "mock mode," demonstrating AI decision-making and knowledge management.
- **Unified CLI**: Provides a single interface for AI commands and Matrix bot controls.
- **Graceful Shutdown**: Matrix bot includes robust subprocess management and cleanup handlers for all exit scenarios.

## External Dependencies

### Core Dependencies
- `matrix-nio[e2e]`: For Matrix protocol support.
- `aiohttp`: Asynchronous HTTP client.
- `requests`: General HTTP library.
- `beautifulsoup4`, `lxml`: For web scraping and parsing.
- `wikipedia-api`: To access Wikipedia.
- `Pillow`: For image processing.
- `python-magic`: For file type detection.
- `aiofiles`: Asynchronous file operations.
- `supabase`: For database integration.
- `psutil`: For process monitoring (used in Matrix bot).

### Optional Dependencies (Not Installed by Default)
- `pyautogui`: For GUI automation (requires X11/display).
- `pynput`: For keyboard/mouse control.
- `rclpy` (ROS 2), `rospy` (ROS 1): For Robot Operating System support.

### Environment Variables and Secrets
- `MATRIX_HOMESERVER`: Matrix server URL.
- `MATRIX_USERNAME`: Bot's Matrix ID.
- `MATRIX_PASSWORD` or `MATRIX_ACCESS_TOKEN`: Matrix account credentials (stored as Replit Secrets).
- `ENABLE_WEBAI_FALLBACK`: Enable WebAI-to-API fallback for image analysis (true/false).
- `WEBAI_API_URL`: WebAI-to-API service URL (e.g., http://localhost:5000).
- `WEBAI_MODEL`: Model for fallback analysis (gemini-pro-vision, gpt-4-vision, claude-3-opus, etc.).

## Recent Changes

### November 20, 2025 - Enhanced Image Analysis & Command System
- 🎨 **Completely Rewrote Image Analyzer with 1000+ Parameters**
  - Detects subjects: animals, humans, humanoids, hybrids, fluffy creatures
  - Identifies actions: sitting, jumping, walking, running, head position, movement
  - Analyzes expressions: smiling, serious, neutral, intense gaze
  - Detects body parts: head, torso, legs, arms, hands/paws, eyes
  - Identifies clothing: colors, accessories, decorations
  - Analyzes environment: outdoor/indoor, sky, vegetation, water, terrain
  - 100+ detailed color variations (not just "mixed color")
  - Species hints and hybrid characteristics
  - Rich natural language descriptions

- 🎮 **Added Command System for Model & Personality Switching**
  - `?model list` - Show available image analysis models
  - `?model offline` - Use offline analyzer (private, no API)
  - `?model webai-gemini` - Use Google Gemini via WebAI-to-API
  - `?model webai-gpt4` - Use GPT-4 Vision via WebAI-to-API
  - `?model webai-claude` - Use Claude 3 Vision via WebAI-to-API
  - `?personality list` - Show available personalities
  - `?personality ribit` - Technical AI assistant mode
  - `?personality megabite` - Friendly companion mode
  - `?help` - Show all commands with current user settings
  - `?status` - Show current model, personality, and bot status

- ✨ **Per-User Settings**
  - Each user can set their own preferred image model
  - Each user can set their own preferred personality
  - Settings persist during bot session
  - Dynamic model switching on image upload

### November 20, 2025 - Added WebAI-to-API Fallback System
- 🚀 **Implemented Image Analysis Fallback Architecture**
  - Created `ImageAnalysisProvider` abstraction for pluggable backends
  - Added `OfflineImageProvider` wrapper for local offline analysis
  - Added `WebAIImageProvider` for WebAI-to-API service integration
  - Added `FallbackImageProvider` with automatic failover logic
  - Fixed `KeyError: 0` crash from incorrect color data access
  - Bot tries offline analyzer first, falls back to WebAI-to-API if enabled
  - Supports multiple AI models via WebAI-to-API: Gemini, ChatGPT, Claude, DeepSeek
  - Configuration via environment variables (see `.env.example`)
  - Inspired by gemini-xmpp pattern for reliable image analysis

### November 20, 2025 - Fixed Image Detection Crashes
- 🐛 **Fixed Image Analysis Errors**
  - Added defensive checks for all optional fields (colors, shapes, features)
  - Fixed color extraction to handle both dict and list formats safely
  - Added proper error handling for analyzer failures
  - Bot no longer crashes on malformed image data