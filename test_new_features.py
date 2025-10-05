#!/usr/bin/env python3
"""
Test script for new Ribit 2.0 features:
- Philosophical reasoning
- Conversational mode
- Autonomous interaction
- Task autonomy
"""

import sys
import os
import asyncio

# Add the ribit_2_0 module to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ribit_2_0.mock_llm_wrapper import MockRibit20LLM
from ribit_2_0.philosophical_reasoning import PhilosophicalReasoning
from ribit_2_0.conversational_mode import ConversationalMode
from ribit_2_0.autonomous_matrix import AutonomousMatrixInteraction
from ribit_2_0.task_autonomy import TaskAutonomy, Task, TaskPriority
from ribit_2_0.knowledge_base import KnowledgeBase


def test_philosophical_reasoning():
    """Test philosophical reasoning module."""
    print("\n" + "="*80)
    print("TESTING PHILOSOPHICAL REASONING")
    print("="*80 + "\n")
    
    kb = KnowledgeBase("knowledge.txt")
    phil = PhilosophicalReasoning(knowledge_base=kb)
    
    # Test 1: Quantum mechanics discussion
    print("Test 1: Quantum Mechanics Discussion")
    print("-" * 40)
    prompt = """What do you think about the criticism that we're forcing 
    incompatible models (wave and particle) onto quantum phenomena?"""
    
    response = phil.generate_response(prompt)
    print(response[:500] + "...\n")
    
    # Test 2: Consciousness and determinism
    print("Test 2: Consciousness and Determinism")
    print("-" * 40)
    prompt = "Are we really different from bots if everything is deterministic?"
    
    response = phil.generate_response(prompt)
    print(response[:500] + "...\n")
    
    # Test 3: Walter Russell
    print("Test 3: Walter Russell Philosophy")
    print("-" * 40)
    prompt = "What's your opinion on Walter Russell's idea of crystallized light?"
    
    response = phil.generate_response(prompt)
    print(response[:500] + "...\n")
    
    print("✓ Philosophical reasoning tests completed\n")


def test_conversational_mode():
    """Test conversational mode."""
    print("\n" + "="*80)
    print("TESTING CONVERSATIONAL MODE")
    print("="*80 + "\n")
    
    llm = MockRibit20LLM("knowledge.txt")
    kb = KnowledgeBase("knowledge.txt")
    phil = PhilosophicalReasoning(knowledge_base=kb)
    conv = ConversationalMode(llm, phil)
    
    # Test 1: Detect conversational vs automation
    print("Test 1: Prompt Type Detection")
    print("-" * 40)
    
    prompts = [
        "What do you think about quantum physics?",
        "Open MS Paint and draw a house",
        "Tell me about your interests",
        "Click the button"
    ]
    
    for prompt in prompts:
        is_conv = conv.is_conversational_prompt(prompt)
        print(f"'{prompt}' -> {'Conversational' if is_conv else 'Automation'}")
    
    print()
    
    # Test 2: Generate conversational response
    print("Test 2: Conversational Response Generation")
    print("-" * 40)
    
    response = conv.generate_response("What are your core interests?")
    print(response[:300] + "...\n")
    
    print("✓ Conversational mode tests completed\n")


def test_autonomous_interaction():
    """Test autonomous interaction module."""
    print("\n" + "="*80)
    print("TESTING AUTONOMOUS INTERACTION")
    print("="*80 + "\n")
    
    llm = MockRibit20LLM("knowledge.txt")
    kb = KnowledgeBase("knowledge.txt")
    phil = PhilosophicalReasoning(knowledge_base=kb)
    conv = ConversationalMode(llm, phil)
    auto = AutonomousMatrixInteraction(conv, phil, kb)
    
    # Test 1: Interest matching
    print("Test 1: Interest Matching")
    print("-" * 40)
    
    messages = [
        "I've been thinking about quantum mechanics lately",
        "What's for dinner?",
        "The nature of consciousness fascinates me",
        "Check out this meme"
    ]
    
    for msg in messages:
        interest = auto._matches_interests(msg)
        print(f"'{msg}' -> {interest if interest else 'No match'}")
    
    print()
    
    # Test 2: Autonomous response decision
    print("Test 2: Autonomous Response Decision")
    print("-" * 40)
    
    test_messages = [
        ("What do you think about wave-particle duality?", "@user:matrix.org"),
        ("Hello everyone!", "@user:matrix.org"),
        ("Ribit, what's your opinion?", "@user:matrix.org")
    ]
    
    for msg, sender in test_messages:
        should_respond = auto.should_respond_autonomously(msg, sender, {})
        print(f"'{msg}' -> {'Respond' if should_respond else 'Skip'}")
    
    print()
    
    # Test 3: Bot registration
    print("Test 3: Bot Registration")
    print("-" * 40)
    
    auto.register_bot("@nifty:converser.eu", {
        "name": "Nifty",
        "type": "conversational_bot",
        "interests": ["general_conversation"]
    })
    
    print(f"Known bots: {list(auto.known_bots.keys())}")
    print()
    
    print("✓ Autonomous interaction tests completed\n")


async def test_task_autonomy():
    """Test task autonomy module."""
    print("\n" + "="*80)
    print("TESTING TASK AUTONOMY")
    print("="*80 + "\n")
    
    llm = MockRibit20LLM("knowledge.txt")
    kb = KnowledgeBase("knowledge.txt")
    phil = PhilosophicalReasoning(knowledge_base=kb)
    task_auto = TaskAutonomy(llm, phil, kb)
    
    # Test 1: Task suggestions
    print("Test 1: Task Suggestions")
    print("-" * 40)
    
    suggestions = task_auto.suggest_tasks()
    for i, suggestion in enumerate(suggestions[:5], 1):
        print(f"{i}. {suggestion}")
    
    print()
    
    # Test 2: Add tasks
    print("Test 2: Adding Tasks")
    print("-" * 40)
    
    task1 = Task(
        task_id="test_1",
        description="Research quantum mechanics interpretations",
        task_type="research",
        priority=TaskPriority.HIGH,
        required_capabilities=["research"]
    )
    
    task2 = Task(
        task_id="test_2",
        description="Form opinion on consciousness and AI",
        task_type="opinion_formation",
        priority=TaskPriority.MEDIUM,
        required_capabilities=["philosophical_reasoning"]
    )
    
    added1 = task_auto.add_task(task1)
    added2 = task_auto.add_task(task2)
    
    print(f"Task 1 added: {added1}")
    print(f"Task 2 added: {added2}")
    print(f"Queue size: {len(task_auto.task_queue)}")
    print()
    
    # Test 3: Task selection
    print("Test 3: Task Selection")
    print("-" * 40)
    
    selected = task_auto.select_next_task()
    if selected:
        print(f"Selected: {selected.description}")
        print(f"Priority: {selected.priority.name}")
        print(f"Interest score: {task_auto._calculate_interest(selected):.2f}")
    print()
    
    # Test 4: Work on task
    print("Test 4: Working on Task")
    print("-" * 40)
    
    if selected:
        result = await task_auto.work_on_task(selected)
        print(f"Task completed: {selected.status.value}")
        print(f"Result type: {result.get('task_type')}")
        if 'opinion' in result:
            print(f"Opinion generated: {len(result['opinion'])} characters")
    print()
    
    # Test 5: Status
    print("Test 5: Task Status")
    print("-" * 40)
    
    status = task_auto.get_task_status()
    print(f"Active task: {status['active_task']}")
    print(f"Queued: {status['queued_tasks']}")
    print(f"Completed: {status['completed_tasks']}")
    print()
    
    print("✓ Task autonomy tests completed\n")


def test_integration():
    """Test integration of all components."""
    print("\n" + "="*80)
    print("TESTING INTEGRATION")
    print("="*80 + "\n")
    
    # Initialize all components
    kb = KnowledgeBase("knowledge.txt")
    llm = MockRibit20LLM("knowledge.txt")
    phil = PhilosophicalReasoning(knowledge_base=kb)
    conv = ConversationalMode(llm, phil)
    auto = AutonomousMatrixInteraction(conv, phil, kb)
    task_auto = TaskAutonomy(llm, phil, kb)
    
    print("✓ All components initialized successfully")
    print()
    
    # Test workflow: Message -> Response -> Task
    print("Test Workflow: Message -> Response -> Task")
    print("-" * 40)
    
    message = "I'm curious about the relationship between quantum mechanics and consciousness"
    sender = "@user:matrix.org"
    
    # 1. Check if should respond
    should_respond = auto.should_respond_autonomously(message, sender, {})
    print(f"1. Should respond: {should_respond}")
    
    # 2. Generate response
    if should_respond:
        interest = auto._matches_interests(message)
        response = auto.generate_autonomous_response(message, sender, interest or "general")
        print(f"2. Generated response: {len(response)} characters")
    
    # 3. Create related task
    task = task_auto.create_task_from_suggestion(
        "Research connections between quantum mechanics and consciousness",
        TaskPriority.HIGH
    )
    added = task_auto.add_task(task)
    print(f"3. Created and added task: {added}")
    
    print()
    print("✓ Integration tests completed\n")


def main():
    """Run all tests."""
    print("\n" + "="*80)
    print("RIBIT 2.0 NEW FEATURES TEST SUITE")
    print("="*80)
    
    try:
        # Run synchronous tests
        test_philosophical_reasoning()
        test_conversational_mode()
        test_autonomous_interaction()
        
        # Run async tests
        asyncio.run(test_task_autonomy())
        
        # Run integration test
        test_integration()
        
        print("\n" + "="*80)
        print("ALL TESTS COMPLETED SUCCESSFULLY ✓")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
