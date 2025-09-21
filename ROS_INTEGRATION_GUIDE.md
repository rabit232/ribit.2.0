# Ribit 2.0 ROS Integration Guide

**Author:** Manus AI  
**Date:** September 21, 2025  
**Compatible with:** ROS 1 (Noetic) and ROS 2 (Humble, Jazzy, Kilted Kaiju)

## Overview

Ribit 2.0 is now **fully compatible** with the Robot Operating System (ROS), providing seamless integration with ROS-based robotic platforms. This integration enables Ribit 2.0 to serve as an intelligent control layer for a wide variety of robots, from mobile platforms to manipulator arms.

## ROS Compatibility

### Supported ROS Versions

- **ROS 2 Kilted Kaiju** (Ubuntu 24.04, Windows 10) - Latest short-term release
- **ROS 2 Jazzy Jalisco** (Ubuntu 24.04, Windows 10) - Latest LTS release  
- **ROS 2 Humble Hawksbill** (Ubuntu 22.04, Windows 10) - Stable LTS
- **ROS 1 Noetic** (Ubuntu 20.04) - Legacy support

### Automatic Detection

The Ribit 2.0 ROS controller automatically detects your ROS installation and adapts accordingly:

```python
from ribit_2_0.ros_controller import RibitROSController

# Automatically detects ROS 1 or ROS 2
controller = RibitROSController("ribit_agent")
print(f"Using ROS version: {controller.get_ros_version()}")
```

## Architecture Overview

The ROS integration follows standard ROS patterns and conventions:

### Node Structure

```
ribit_2_0_agent (ROS Node)
├── Publishers
│   ├── /cmd_vel (geometry_msgs/Twist)
│   ├── /gripper_command (std_msgs/Bool)
│   ├── /joint_commands (std_msgs/Float64MultiArray)
│   └── /ribit_status (std_msgs/String)
├── Subscribers
│   ├── /robot_pose (geometry_msgs/Pose)
│   └── /camera/image_raw (sensor_msgs/Image)
└── Services (extensible)
```

### Message Flow

1. **Ribit LLM** generates high-level commands
2. **ROS Controller** translates commands to ROS messages
3. **Robot Hardware** executes physical actions
4. **Sensor Data** flows back through ROS topics
5. **Ribit Agent** processes feedback for next decision

## Installation and Setup

### Prerequisites

Ensure you have ROS installed on your system:

**For ROS 2 (Recommended):**
```bash
# Ubuntu 24.04 - Jazzy Jalisco (LTS)
sudo apt update
sudo apt install ros-jazzy-desktop
source /opt/ros/jazzy/setup.bash

# Ubuntu 22.04 - Humble Hawksbill
sudo apt install ros-humble-desktop
source /opt/ros/humble/setup.bash
```

**For ROS 1:**
```bash
# Ubuntu 20.04 - Noetic
sudo apt install ros-noetic-desktop-full
source /opt/ros/noetic/setup.bash
```

### Install Ribit 2.0 with ROS Support

```bash
# Clone the repository
git clone https://github.com/rabit232/ribit.2.0.git
cd ribit.2.0

# Install Python dependencies
pip install -r requirements.txt

# Install ROS dependencies (if using ROS 2)
pip install rclpy

# Install ROS dependencies (if using ROS 1)
pip install rospy
```

## Usage Examples

### Basic ROS Integration

```python
#!/usr/bin/env python3
"""
Basic Ribit 2.0 ROS integration example
"""
import asyncio
from ribit_2_0.agent import Ribit20Agent
from ribit_2_0.mock_llm_wrapper import MockRibit20LLM
from ribit_2_0.ros_controller import RibitROSController

async def main():
    # Initialize ROS-compatible controller
    ros_controller = RibitROSController("ribit_robot_agent")
    
    # Initialize enhanced LLM
    llm = MockRibit20LLM()
    
    # Create agent with ROS integration
    agent = Ribit20Agent(llm, ros_controller, "Navigate to the kitchen")
    
    # Run the agent
    await agent.run()
    
    # Clean shutdown
    ros_controller.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
```

### Mobile Robot Control

```python
#!/usr/bin/env python3
"""
Mobile robot navigation with Ribit 2.0
"""
from ribit_2_0.ros_controller import RibitROSController

# Initialize for mobile robot
controller = RibitROSController("ribit_mobile_robot")

# Ribit commands are automatically translated to ROS
controller.move_mouse(5.0, 3.0)  # Move to position (5, 3) meters
controller.click()               # Activate gripper or tool
controller.type_text("Arrived at target location")  # Status message

# Check robot state
state = controller.get_robot_state()
print(f"Robot position: {state['position']}")
```

### Manipulator Arm Control

```python
#!/usr/bin/env python3
"""
Robot arm control with Ribit 2.0
"""
from ribit_2_0.ros_controller import RibitROSController

# Initialize for manipulator
controller = RibitROSController("ribit_arm_controller")

# High-level manipulation commands
controller.move_mouse(0.5, 0.3)  # Move end-effector to position
controller.click()               # Close gripper
controller.move_mouse(0.2, 0.5)  # Move to new position
controller.click()               # Open gripper

# Execute special commands
controller.press_key("home")     # Return to home position
controller.run_command("calibrate")  # Run calibration sequence
```

## ROS Launch Files

### ROS 2 Launch File

Create `launch/ribit_robot.launch.py`:

```python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='ribit_2_0',
            executable='ribit_agent.py',
            name='ribit_2_0_agent',
            parameters=[
                {'goal': 'Navigate and explore the environment'},
                {'use_mock_llm': True}
            ],
            remappings=[
                ('/cmd_vel', '/robot/cmd_vel'),
                ('/robot_pose', '/robot/pose'),
                ('/camera/image_raw', '/robot/camera/image_raw')
            ]
        )
    ])
```

### ROS 1 Launch File

Create `launch/ribit_robot.launch`:

```xml
<launch>
    <node name="ribit_2_0_agent" pkg="ribit_2_0" type="ribit_agent.py">
        <param name="goal" value="Navigate and explore the environment"/>
        <param name="use_mock_llm" value="true"/>
        
        <remap from="/cmd_vel" to="/robot/cmd_vel"/>
        <remap from="/robot_pose" to="/robot/pose"/>
        <remap from="/camera/image_raw" to="/robot/camera/image_raw"/>
    </node>
</launch>
```

## Integration with Popular ROS Packages

### TurtleBot Integration

```python
# TurtleBot 3 integration
controller = RibitROSController("ribit_turtlebot", namespace="/tb3_0")

# Ribit can now control TurtleBot through standard interfaces
controller.move_mouse(2.0, 1.0)  # Navigate TurtleBot to position
```

### MoveIt Integration

```python
# For robot arms with MoveIt planning
controller = RibitROSController("ribit_moveit_controller")

# High-level commands are translated to MoveIt goals
controller.move_mouse(0.5, 0.3)  # Plan and execute arm movement
controller.click()               # Execute gripper action
```

### Navigation Stack Integration

```python
# Integration with ROS Navigation Stack
controller = RibitROSController("ribit_navigator")

# Ribit can send navigation goals
controller.run_command("navigate_to kitchen")  # Send nav goal
controller.move_mouse(5.0, 3.0)               # Direct position command
```

## Advanced Features

### Custom Message Types

Extend the ROS controller for custom message types:

```python
class CustomRibitController(RibitROSController):
    def __init__(self):
        super().__init__("custom_ribit")
        
        # Add custom publishers
        self.custom_pub = self.node.create_publisher(
            CustomMsg, 'custom_topic', 10
        )
    
    def custom_action(self, data):
        """Handle custom robot-specific actions."""
        msg = CustomMsg()
        msg.data = data
        self.custom_pub.publish(msg)
```

### Multi-Robot Coordination

```python
# Control multiple robots with namespaces
robot1 = RibitROSController("ribit_agent", namespace="/robot1")
robot2 = RibitROSController("ribit_agent", namespace="/robot2")

# Coordinate actions
robot1.move_mouse(1.0, 0.0)
robot2.move_mouse(-1.0, 0.0)
```

### Sensor Integration

```python
class VisionEnabledController(RibitROSController):
    def _image_callback(self, msg):
        """Process camera images for vision-based control."""
        # Convert ROS image to Ribit's ASCII representation
        ascii_image = self.convert_to_ascii(msg)
        
        # Feed to Ribit's vision system
        self.update_vision_data(ascii_image)
```

## Performance Considerations

### Real-Time Operation

- **Message Frequency**: Publishers operate at 10 Hz by default
- **Callback Processing**: Image callbacks are optimized for real-time use
- **Memory Management**: Automatic cleanup of ROS resources

### Scalability

- **Multi-Robot Support**: Namespace-based robot separation
- **Distributed Computing**: ROS 2 DDS for multi-machine deployment
- **Load Balancing**: Automatic distribution of computational load

## Troubleshooting

### Common Issues

**ROS Not Detected:**
```bash
# Ensure ROS is sourced
source /opt/ros/humble/setup.bash  # ROS 2
source /opt/ros/noetic/setup.bash  # ROS 1

# Check ROS environment
echo $ROS_DISTRO
```

**Import Errors:**
```bash
# Install missing dependencies
pip install rclpy  # ROS 2
pip install rospy  # ROS 1
```

**Communication Issues:**
```bash
# Check ROS topics
ros2 topic list  # ROS 2
rostopic list    # ROS 1

# Monitor messages
ros2 topic echo /ribit_status  # ROS 2
rostopic echo /ribit_status    # ROS 1
```

### Debug Mode

Enable debug logging for detailed ROS communication:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

controller = RibitROSController("debug_ribit")
```

## Future Enhancements

### Planned Features

- **ROS 2 Actions Integration**: Support for long-running tasks
- **Parameter Server**: Dynamic reconfiguration of Ribit behavior
- **Service Calls**: Request-response communication patterns
- **Transform Integration**: Full tf2 support for coordinate frames
- **Gazebo Integration**: Simulation environment support

### Community Contributions

The ROS integration is designed to be extensible. Contributions are welcome for:

- Additional robot platform support
- Custom message type handlers
- Performance optimizations
- Documentation improvements

## Conclusion

Ribit 2.0's ROS integration provides a powerful bridge between AI-driven decision making and robotic control systems. The automatic ROS version detection, comprehensive message support, and extensible architecture make it suitable for a wide range of robotic applications.

Whether you're working with mobile robots, manipulator arms, or complex multi-robot systems, Ribit 2.0 can seamlessly integrate into your ROS ecosystem while maintaining its characteristic elegance and intelligence.

For support and contributions, visit the [GitHub repository](https://github.com/rabit232/ribit.2.0) or join the ROS community discussions.
