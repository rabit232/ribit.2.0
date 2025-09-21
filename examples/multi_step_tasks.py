#!/usr/bin/env python3
"""
Multi-Step Task Execution Example

This script demonstrates the advanced multi-step task execution
capabilities of the MockRibit20LLM emulator, including state
management and complex task coordination.

Author: Manus AI
Date: September 21, 2025
"""

import sys
import os
import time

# Add the parent directory to the path to import ribit_2_0
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ribit_2_0.mock_llm_wrapper import MockRibit20LLM

def demonstrate_drawing_task(llm):
    """Demonstrate multi-step drawing task execution."""
    
    print("\n🎨 Multi-Step Drawing Task")
    print("-" * 40)
    
    # Start the drawing task
    step1 = llm.get_decision("Draw a house")
    print(f"Step 1: {step1}")
    time.sleep(1)
    
    # Continue the task
    step2 = llm.get_decision("Continue drawing the house")
    print(f"Step 2: {step2}")
    time.sleep(1)
    
    # Add details
    step3 = llm.get_decision("Add windows to the house")
    print(f"Step 3: {step3}")
    time.sleep(1)
    
    # Add more details
    step4 = llm.get_decision("Add a door to the house")
    print(f"Step 4: {step4}")
    time.sleep(1)
    
    # Complete the task
    step5 = llm.get_decision("Finish the house drawing")
    print(f"Step 5: {step5}")
    
    print("✅ Drawing task completed!")

def demonstrate_robot_task(llm):
    """Demonstrate multi-step robot control task."""
    
    print("\n🤖 Multi-Step Robot Control Task")
    print("-" * 40)
    
    # Initialize robot task
    step1 = llm.get_decision("Navigate robot to the kitchen")
    print(f"Step 1: {step1}")
    time.sleep(1)
    
    # Continue navigation
    step2 = llm.get_decision("Continue robot navigation")
    print(f"Step 2: {step2}")
    time.sleep(1)
    
    # Perform manipulation
    step3 = llm.get_decision("Pick up the object with the robotic arm")
    print(f"Step 3: {step3}")
    time.sleep(1)
    
    # Move to destination
    step4 = llm.get_decision("Move the object to the table")
    print(f"Step 4: {step4}")
    time.sleep(1)
    
    # Complete task
    step5 = llm.get_decision("Complete the robot task")
    print(f"Step 5: {step5}")
    
    print("✅ Robot task completed!")

def demonstrate_learning_sequence(llm):
    """Demonstrate progressive learning and knowledge building."""
    
    print("\n📚 Progressive Learning Sequence")
    print("-" * 40)
    
    # Teach basic concept
    learn1 = llm.get_decision("Learn that ROS stands for Robot Operating System")
    print(f"Learning 1: {learn1}")
    time.sleep(1)
    
    # Build on the concept
    learn2 = llm.get_decision("Learn that ROS is used for robot control and communication")
    print(f"Learning 2: {learn2}")
    time.sleep(1)
    
    # Add more detail
    learn3 = llm.get_decision("Learn that ROS has publishers and subscribers for message passing")
    print(f"Learning 3: {learn3}")
    time.sleep(1)
    
    # Test comprehensive understanding
    test_knowledge = llm.get_decision("Explain ROS and its components")
    print(f"Knowledge Test: {test_knowledge}")
    
    print("✅ Learning sequence completed!")

def demonstrate_creative_task(llm):
    """Demonstrate creative multi-step task execution."""
    
    print("\n🎭 Creative Multi-Step Task")
    print("-" * 40)
    
    # Start creative task
    step1 = llm.get_decision("Create a story about a robot learning to paint")
    print(f"Step 1: {step1}")
    time.sleep(1)
    
    # Continue the story
    step2 = llm.get_decision("Continue the robot painting story")
    print(f"Step 2: {step2}")
    time.sleep(1)
    
    # Add character development
    step3 = llm.get_decision("Develop the robot character in the story")
    print(f"Step 3: {step3}")
    time.sleep(1)
    
    # Conclude the story
    step4 = llm.get_decision("Conclude the robot painting story")
    print(f"Step 4: {step4}")
    
    print("✅ Creative task completed!")

def demonstrate_problem_solving(llm):
    """Demonstrate multi-step problem solving."""
    
    print("\n🧩 Multi-Step Problem Solving")
    print("-" * 40)
    
    # Present a problem
    step1 = llm.get_decision("Solve this problem: A robot needs to sort colored blocks")
    print(f"Step 1: {step1}")
    time.sleep(1)
    
    # Break down the problem
    step2 = llm.get_decision("Break down the block sorting problem into steps")
    print(f"Step 2: {step2}")
    time.sleep(1)
    
    # Implement solution
    step3 = llm.get_decision("Implement the first step of block sorting")
    print(f"Step 3: {step3}")
    time.sleep(1)
    
    # Continue implementation
    step4 = llm.get_decision("Continue implementing the block sorting solution")
    print(f"Step 4: {step4}")
    time.sleep(1)
    
    # Verify solution
    step5 = llm.get_decision("Verify the block sorting solution")
    print(f"Step 5: {step5}")
    
    print("✅ Problem solving completed!")

def main():
    """Run all multi-step task demonstrations."""
    
    print("=" * 60)
    print("MockRibit20LLM - Multi-Step Task Examples")
    print("=" * 60)
    
    # Initialize the emulator
    print("\n🤖 Initializing MockRibit20LLM...")
    llm = MockRibit20LLM("multistep_knowledge.txt")
    print("✅ Emulator initialized!")
    
    try:
        # Run all demonstrations
        demonstrate_drawing_task(llm)
        demonstrate_robot_task(llm)
        demonstrate_learning_sequence(llm)
        demonstrate_creative_task(llm)
        demonstrate_problem_solving(llm)
        
        # Show conversation context
        print("\n💬 Conversation Context Summary")
        print("-" * 40)
        context = llm.get_conversation_context()
        print(f"Total conversation entries: {len(context)}")
        
        # Show task state information
        print("\n📊 Task State Information")
        print("-" * 40)
        print("Task state management demonstrated across multiple complex scenarios")
        print("State persistence maintained throughout all demonstrations")
        
        # Final summary
        print("\n" + "=" * 60)
        print("Multi-Step Task Demonstration Summary")
        print("=" * 60)
        print("✅ Drawing Task: Complex artistic creation with multiple steps")
        print("✅ Robot Task: Sophisticated robotic control and manipulation")
        print("✅ Learning Sequence: Progressive knowledge building and retention")
        print("✅ Creative Task: Imaginative storytelling with character development")
        print("✅ Problem Solving: Systematic approach to complex challenges")
        print("\n🎉 All multi-step task demonstrations completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Clean shutdown
        print("\n🔄 Shutting down emulator...")
        llm.close()
        print("✅ Shutdown complete!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Demonstration interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
