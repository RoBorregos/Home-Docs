# Architecture

TMR 2025 had the best implementation of both pick and place tasks from recent years on RoBorregos. It also saw a big shift in the structure of nodes and their communication, considering both ROS2 capabilities and escalability for further tasks on the area.

The core of the system is designed around robust communication and specialized management. The Manipulation Core serves as the central logic handler, connecting most nodes and orchestrating task achievement. It minimizes system overhead by reducing the need for redundant client connections across multiple nodes (e.g., accessing perception for both picking and placing). Internally, it uses specialized "Managers" for each task, which handle the unique logic of their respective operations using the core's assets. All movements to specified goals are planned by the Motion Servers. These servers interface with MoveIt! to generate and execute collision-free trajectories.


## Node Architecture

![image](../../assets/home/Manipulation/architecture_tmr2025.png)

## Task Pipeline

The developed pipeline enables precise interaction with a 6-DOF robotic arm and its custom gripper for picking, placing, and pouring, integrating perception and motion planning components.
The system employs a Hybrid Motion Planning strategy. It utilizes Sampling-based Planning (RRTConnect) for generating collision-free trajectories during complex manipulation (like pouring), enforcing strict orientation constraints, while employing Direct Joint Interpolation for high-speed, and auxiliary tasks (homing, scanning) in free space.

The Picking Strategy achieved an 80% reliability rate, enabling precise target isolation by fusing 2D detection data with 3D point clouds. To minimize latency, parallel filtering and variable-resolution downsampling are employed. The planning scene is optimized by modeling the table as a box and obstacles as spheres using RANSAC. GPD interprets object clusters, allowing MoveIt! to efficiently plan trajectories within the simplified environment.

The Placing Strategy demonstrated a high 95% reliability rate. The optimal placement pose is determined by combining two costmaps: a Gaussian Base Heatmap (favoring free space) and a Special Request Heatmap (encoding relative constraints like "in front of").

For the Pouring Strategy, the container's 3D cluster is analyzed (PCL) to determine the centroid and rim height. The PourMotion server uses MoveIt! with dynamic orientation path constraints to define a pour_pose above the center and prevent spillage.

Finally, the Custom Gripper is a parallel mechanism powered by a rack-and-pinion system. Its innovation lies in its fingers, which incorporate fractal-structured silicone covers and soft inner materials, enhancing deformation and adaptability for objects up to 1 kg.


![image](../../assets/home/Manipulation/pipeline_tmr2025.png)