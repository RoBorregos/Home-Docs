# Navigation

The navigation system for Frida is built on a comprehensive architecture that enables autonomous movement, obstacle avoidance, and efficient path planning. The system integrates advanced mapping and localization with sophisticated path planning and motion control, all implemented on ROS2 with Nav2.

## Overview

The navigation stack is divided into two main components:

1. **Mapping & Localization** - RTABMap with ORB-SLAM3 for visual-inertial mapping and localization
2. **Path Planning & Control** - MPPI Controller integrated with Nav2 behavior tree for autonomous navigation

---

## Mapping & Localization

### RTABMap with ORB-SLAM3 Implementation

The mapping and localization system combines visual and laser-based approaches to create a robust, dense 3D map while maintaining accurate robot localization.

**Visual Localization & Mapping:**
- **ORB-SLAM3**: Provides visual-inertial simultaneous localization and mapping using camera and IMU data
- Enables accurate pose estimation and visual feature tracking in the environment
- Supports loop closure detection for drift correction and map consistency

**Sensor Fusion Approach:**
- **Hybrid Mapping**: Combines RGB-D/Stereo camera data (ORB-SLAM3) with 2D LiDAR data (RTABMap)
- **Visual Features**: Used for accurate pose estimation and fine-grained environment understanding
- **LiDAR Scans**: Provides additional depth information, obstacle detection, and 2D navigation compatibility
- **RTABMap Integration**: Fuses visual features from ORB-SLAM3 with LiDAR data to generate a comprehensive map
- **Loop Closure**: Detects when the robot revisits known areas, allowing for map optimization and drift correction

**Resulting Capabilities:**
- 3D occupancy mapping for navigation planning
- Accurate global localization within the mapped environment
- Robust loop closure and map consistency
- Support for both visual and metric mapping

---

## Path Planning & Control

### MPPI Controller with Nav2

The navigation execution layer uses a sophisticated control architecture built on ROS2 and Nav2 framework.

**Architecture Components:**

**1. Behavior Tree Navigation**
- Implements hierarchical planning using a behavior tree structure
- Manages complex navigation sequences and fallback strategies
- Coordinates between different navigation states and responses

**2. Nav2 Framework (ROS2)**
- **Planner Server**: Generates global paths from start to goal positions
- **Controller Server**: Executes motion commands and follows planned trajectories
- **Behavior Server**: Manages high-level navigation behaviors and recovery actions
- **Costmap**: Maintains dynamic cost maps for obstacle avoidance and path safety

**3. MPPI Controller**
- **Model Predictive Path Integral Control**: Advanced motion controller for trajectory following
- Optimizes motion paths considering:
  - Robot dynamics and kinematics
  - Collision avoidance with dynamic obstacles
  - Smooth acceleration and deceleration profiles
  - Energy efficiency in path execution
- Provides smooth, natural robot motion while respecting physical constraints

**4. 2D LiDAR Navigation**
- Uses 2D laser scans for real-time obstacle detection
- Integrates with costmaps for dynamic environment response
- Enables safe navigation in unstructured environments

**System Flow:**
1. Goal specification from high-level planning
2. Behavior tree coordination of navigation sequence
3. Nav2 global path planning to goal
4. MPPI controller generates smooth, safe trajectories
5. Real-time execution with LiDAR-based obstacle avoidance
6. Continuous feedback and adaptation using localization from RTABMap/ORB-SLAM3

