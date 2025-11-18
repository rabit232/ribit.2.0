#!/usr/bin/env python3
"""
Ribit 2.0 Demo - Interactive Console Application
Demonstrates the core functionality of Ribit 2.0 AI agent
"""

import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ribit_2_0.mock_llm_wrapper import MockRibit20LLM

def print_header():
    """Print the Ribit 2.0 welcome header."""
    print("\n" + "=" * 70)
    print("🤖 Ribit 2.0: Enhanced AI Agent Demo")
    print("=" * 70)
    print("An elegant, wise AI agent for GUI automation and robotic control")
    print("=" * 70 + "\n")

def print_menu():
    """Print the interactive menu."""
    print("\n" + "-" * 70)
    print("Available Commands:")
    print("-" * 70)
    print("  1. Introduction - Meet Ribit 2.0")
    print("  2. Capabilities - View available features")
    print("  3. Personality - Learn about Ribit's character")
    print("  4. Ask Question - Have a conversation with Ribit")
    print("  5. Learn Knowledge - Teach Ribit something new")
    print("  6. Recall Knowledge - Ask Ribit to recall information")
    print("  7. Task Execution - Demonstrate automation capabilities")
    print("  8. Conversation History - View recent context")
    print("  9. Exit")
    print("-" * 70)

def main():
    """Main demo application."""
    print_header()
    
    print("🔧 Initializing Ribit 2.0 LLM Emulator...")
    try:
        llm = MockRibit20LLM()
        print("✅ Ribit 2.0 initialized successfully!\n")
    except Exception as e:
        print(f"❌ Error initializing Ribit 2.0: {e}")
        return
    
    running = True
    
    while running:
        print_menu()
        choice = input("\n👉 Enter your choice (1-9): ").strip()
        
        print("\n" + "=" * 70)
        
        if choice == "1":
            # Introduction
            print("🎭 INTRODUCTION")
            print("-" * 70)
            response = llm.get_decision("Introduce yourself and tell me about your purpose")
            print(f"\n{response}\n")
            
        elif choice == "2":
            # Capabilities
            print("🔧 CAPABILITIES")
            print("-" * 70)
            capabilities = llm.get_capabilities()
            print("\nRibit 2.0 Features:")
            for capability, status in capabilities.items():
                status_icon = "✅" if status else "❌"
                print(f"  {status_icon} {capability.replace('_', ' ').title()}")
            print()
            
        elif choice == "3":
            # Personality
            print("🎨 PERSONALITY")
            print("-" * 70)
            personality = llm.get_personality_info()
            print("\nPersonality Profile:")
            for key, value in personality.items():
                print(f"  • {key.replace('_', ' ').title()}: {value}")
            print()
            
        elif choice == "4":
            # Ask Question
            print("💬 ASK A QUESTION")
            print("-" * 70)
            question = input("\n👉 Your question: ").strip()
            if question:
                response = llm.get_decision(question)
                print(f"\n🤖 Ribit: {response}\n")
            else:
                print("⚠️  No question entered.\n")
                
        elif choice == "5":
            # Learn Knowledge
            print("📚 TEACH RIBIT")
            print("-" * 70)
            knowledge = input("\n👉 What would you like to teach? (e.g., 'Learn that Python is a programming language'): ").strip()
            if knowledge:
                response = llm.get_decision(knowledge)
                print(f"\n🤖 Ribit: {response}\n")
            else:
                print("⚠️  No knowledge entered.\n")
                
        elif choice == "6":
            # Recall Knowledge
            print("🧠 RECALL KNOWLEDGE")
            print("-" * 70)
            query = input("\n👉 What should Ribit recall? (e.g., 'What is Python?'): ").strip()
            if query:
                response = llm.get_decision(query)
                print(f"\n🤖 Ribit: {response}\n")
            else:
                print("⚠️  No query entered.\n")
                
        elif choice == "7":
            # Task Execution
            print("🎯 TASK EXECUTION DEMO")
            print("-" * 70)
            print("\nDemonstrating automation capabilities...")
            tasks = [
                "Move to coordinates (100, 200)",
                "Click on the target",
                "Type 'Hello, World!'",
                "Explain what you just did"
            ]
            for i, task in enumerate(tasks, 1):
                print(f"\n{i}. Task: {task}")
                response = llm.get_decision(task)
                print(f"   Response: {response}")
            print()
            
        elif choice == "8":
            # Conversation History
            print("📜 CONVERSATION HISTORY")
            print("-" * 70)
            context = llm.get_conversation_context()
            print(f"\nTotal conversation entries: {len(context)}")
            if context:
                print("\nRecent context (last 5 entries):")
                for i, entry in enumerate(context[-5:], 1):
                    print(f"  {i}. {entry[:60]}...")
            else:
                print("\n⚠️  No conversation history yet.")
            print()
            
        elif choice == "9":
            # Exit
            print("👋 GOODBYE")
            print("-" * 70)
            print("\nThank you for exploring Ribit 2.0!")
            print("🤖 Shutting down gracefully...\n")
            llm.close()
            running = False
            
        else:
            print("⚠️  Invalid choice. Please enter a number between 1 and 9.\n")
    
    print("=" * 70)
    print("✅ Demo completed successfully!")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user. Exiting gracefully...\n")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
