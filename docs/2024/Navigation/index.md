# Navigation
Navigation in mobile robots refers to the ability of a robot to move autonomously within its environment, reach designated goals, avoid obstacles, and optimize its path. This process involves several components and technologies, including localization, path planning, and motion control.

For the Frida robot, the navigation system is developed across various levels, ranging from hardware integration to advanced software implementations. We divide navigation into three key components:

- Mapping
- Path Planning and Localization
- Navigation Action Server

## Mapping

In this project, mapping is achieved using gmapping with ROS1 Noetic. The process integrates multiple hardware and software components to generate a robust and accurate 2D map of the environment. Below is a detailed explanation of the mapping pipeline:

### 1. Hardware Overview
Mobile Base: **Dashgo B1**, equipped with a custom driver wrapper for interfacing and a velocity smoother node for refined control of movement.
***Sensors:***
- RP A1 LiDAR: Provides 2D laser scan data for detecting obstacles and features in the environment.
- IMU (Inertial Measurement Unit): Offers orientation and angular velocity data.
- Wheel Encoders (Odometry): Tracks the robot's linear and angular movement.

### 2. Sensor Fusion with EKF
To improve localization accuracy, sensor data is fused using an *Extended Kalman Filter (EKF)*:

Combines odometry and IMU data to generate a more reliable pose estimate.
Outputs a filtered odom frame that accounts for drift and noise in individual sensors.

### 3. Gmapping for SLAM (Simultaneous Localization and Mapping)
The gmapping package implements a particle filter-based SLAM approach:

***Input Data:***
Laser scan data from RP A1 LiDAR (/scan topic).
Odometry data (/odom topic) from the EKF fusion.
***Particle Filter:***
Uses LiDAR data to detect features like walls and furniture.
Matches these features against previously observed landmarks, updating the robot's position and improving the map incrementally.
***Map Generation:***
Produces a 2D occupancy grid map (/map topic), representing free space, obstacles, and unknown areas.

### 4. Velocity Smoothing
The velocity smoother node ensures controlled and steady movement of the Dashgo B1, reducing jerky motions that could distort the mapping process.

### 5. Navigation and Feedback Loop
As the robot moves, the gmapping algorithm continuously updates the map while the particle filter adjusts the robot’s position.
The real-time feedback between odometry, LiDAR data, and the particle filter ensures that the map remains accurate and consistent.
This setup creates a reliable and efficient pipeline for generating maps in a domestic environment, enabling subsequent tasks such as path planning and autonomous navigation.



