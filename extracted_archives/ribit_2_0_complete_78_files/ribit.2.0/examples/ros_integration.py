#!/usr/bin/env python3
"""
ROS Integration Example with MockRibit20LLM

This script demonstrates how to integrate the MockRibit20LLM
emulator with ROS-based robotic systems for intelligent
robot control and automation.

Author: Manus AI
Date: September 21, 2025
"""

import sys
import os
import time

# Add the parent directory to the path to import ribit_2_0
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ribit_2_0.mock_llm_wrapper import MockRibit20LLM
from ribit_2_0.ros_controller import RibitROSController

def demonstrate_mobile_robot_control(llm, ros_controller):
    """Demonstrate mobile robot control with AI decision making."""
    
    print("\n🚗 Mobile Robot Control Demonstration")
    print("-" * 50)
    
    # Get AI decision for navigation
    nav_decision = llm.get_decision("Navigate the mobile robot to coordinates (5, 3)")
    print(f"🧠 AI Decision: {nav_decision}")
    
    # Execute through ROS controller
    result = ros_controller.move_mouse(5.0, 3.0)
    print(f"🤖 ROS Execution: {result}")
    
    # Get robot state
    state = ros_controller.get_robot_state()
    print(f"📍 Robot Position: ({state['position']['x']}, {state['position']['y']})")
    
    # AI decision for next action
    next_decision = llm.get_decision("The robot has reached the target. What should it do next?")
    print(f"🧠 Next Decision: {next_decision}")

def demonstrate_manipulator_control(llm, ros_controller):
    """Demonstrate robotic arm control with AI guidance."""
    
    print("\n🦾 Manipulator Control Demonstration")
    print("-" * 50)
    
    # AI decision for manipulation task
    manip_decision = llm.get_decision("Use the robotic arm to pick up an object")
    print(f"🧠 AI Decision: {manip_decision}")
    
    # Execute arm movement
    arm_result = ros_controller.move_mouse(0.5, 0.3)
    print(f"🤖 Arm Movement: {arm_result}")
    
    # AI decision for gripper control
    grip_decision = llm.get_decision("Close the gripper to grasp the object")
    print(f"🧠 Gripper Decision: {grip_decision}")
    
    # Execute gripper action
    grip_result = ros_controller.click()
    print(f"🤖 Gripper Action: {grip_result}")
    
    # Check gripper state
    state = ros_controller.get_robot_state()
    print(f"✋ Gripper State: {state['gripper_state']}")

def demonstrate_sensor_integration(llm, ros_controller):
    """Demonstrate sensor data integration with AI processing."""
    
    print("\n📡 Sensor Integration Demonstration")
    print("-" * 50)
    
    # Simulate sensor data processing
    sensor_decision = llm.get_decision("Process camera data to identify objects in the environment")
    print(f"🧠 Sensor Processing: {sensor_decision}")
    
    # AI decision based on sensor data
    analysis_decision = llm.get_decision("Analyze the detected objects and plan next action")
    print(f"🧠 Analysis Decision: {analysis_decision}")
    
    # Status update
    status_result = ros_controller.type_text("Object detection and analysis completed")
    print(f"📢 Status Update: {status_result}")

def demonstrate_multi_robot_coordination(llm):
    """Demonstrate coordination of multiple robots."""
    
    print("\n🤖🤖 Multi-Robot Coordination Demonstration")
    print("-" * 50)
    
    # Create multiple robot controllers
    robot1 = RibitROSController("ribit_robot_1", namespace="/robot1")
    robot2 = RibitROSController("ribit_robot_2", namespace="/robot2")
    
    # AI decision for coordination
    coord_decision = llm.get_decision("Coordinate two robots to work together on a task")
    print(f"🧠 Coordination Decision: {coord_decision}")
    
    # Execute coordinated movements
    result1 = robot1.move_mouse(2.0, 1.0)
    result2 = robot2.move_mouse(-2.0, 1.0)
    
    print(f"🤖 Robot 1: {result1}")
    print(f"🤖 Robot 2: {result2}")
    
    # AI decision for next coordination step
    next_coord = llm.get_decision("Continue coordinating the robots for optimal task completion")
    print(f"🧠 Next Coordination: {next_coord}")
    
    # Clean up robot controllers
    robot1.shutdown()
    robot2.shutdown()

def demonstrate_emergency_handling(llm, ros_controller):
    """Demonstrate emergency situation handling."""
    
    print("\n🚨 Emergency Handling Demonstration")
    print("-" * 50)
    
    # Simulate emergency situation
    emergency_decision = llm.get_decision("Emergency detected: obstacle in robot path. Take immediate action.")
    print(f"🧠 Emergency Decision: {emergency_decision}")
    
    # Execute emergency stop
    stop_result = ros_controller.press_key("escape")  # Emergency stop
    print(f"🛑 Emergency Stop: {stop_result}")
    
    # AI decision for recovery
    recovery_decision = llm.get_decision("Plan recovery strategy after emergency stop")
    print(f"🧠 Recovery Decision: {recovery_decision}")
    
    # Execute recovery
    recovery_result = ros_controller.run_command("status")
    print(f"🔄 Recovery Status: {recovery_result}")

def demonstrate_learning_from_ros(llm, ros_controller):
    """Demonstrate learning from ROS system interactions."""
    
    print("\n📚 Learning from ROS Interactions")
    print("-" * 50)
    
    # Teach about ROS concepts
    ros_learning = llm.get_decision("Learn that ROS uses topics for communication between nodes")
    print(f"📖 ROS Learning: {ros_learning}")
    
    # Apply learned knowledge
    application = llm.get_decision("Use ROS knowledge to explain robot communication")
    print(f"🎓 Knowledge Application: {application}")
    
    # Learn from robot state
    state = ros_controller.get_robot_state()
    state_learning = llm.get_decision(f"Learn about robot state: position {state['position']}, gripper {state['gripper_state']}")
    print(f"🤖 State Learning: {state_learning}")

def main():
    """Run all ROS integration demonstrations."""
    
    print("=" * 70)
    print("MockRibit20LLM + ROS Integration Examples")
    print("=" * 70)
    
    # Initialize components
    print("\n🤖 Initializing MockRibit20LLM...")
    llm = MockRibit20LLM("ros_knowledge.txt")
    print("✅ LLM Emulator initialized!")
    
    print("\n📡 Initializing ROS Controller...")
    ros_controller = RibitROSController("ribit_demo_robot")
    print(f"✅ ROS Controller initialized! (Version: {ros_controller.get_ros_version()})")
    
    if not ros_controller.is_ros_available():
        print("ℹ️  Running in mock ROS mode (no ROS installation detected)")
    
    try:
        # Run all demonstrations
        demonstrate_mobile_robot_control(llm, ros_controller)
        demonstrate_manipulator_control(llm, ros_controller)
        demonstrate_sensor_integration(llm, ros_controller)
        demonstrate_multi_robot_coordination(llm)
        demonstrate_emergency_handling(llm, ros_controller)
        demonstrate_learning_from_ros(llm, ros_controller)
        
        # Show integration summary
        print("\n" + "=" * 70)
        print("ROS Integration Summary")
        print("=" * 70)
        
        # Check capabilities
        capabilities = llm.get_capabilities()
        print("🔧 AI Capabilities:")
        for cap, status in capabilities.items():
            if status:
                print(f"   ✅ {cap.replace('_', ' ').title()}")
        
        # Check ROS status
        print(f"\n📡 ROS Integration Status:")
        print(f"   • ROS Version: {ros_controller.get_ros_version()}")
        print(f"   • ROS Available: {ros_controller.is_ros_available()}")
        print(f"   • Robot State: {ros_controller.get_robot_state()['status']}")
        
        # Show conversation context
        context = llm.get_conversation_context()
        print(f"\n💬 Conversation Context: {len(context)} entries")
        
        print("\n🎉 All ROS integration demonstrations completed successfully!")
        print("🚀 Ribit 2.0 is ready for robotic deployment!")
        
    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Clean shutdown
        print("\n🔄 Shutting down components...")
        ros_controller.shutdown()
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
