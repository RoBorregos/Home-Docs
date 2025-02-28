# Area Overview
RoBorregos @Home's Object Manipulation area handles the robot's physical interaction with the environment, including objects and people. This area is crucial for tasks such as picking and placing objects, handling specific items (such as a watter bottle or a bag) and even interacting with people (receiving or giving objects). As such, this area leads 3 core technical areas of the robot:

- **2D Vision**: Collaborating with the Vision area, it is used to identify and extract information from 2D images, such as object detection and segmentation.
- **3D Perception**: Revolves around extracting environment and object information from 3D data.
- **Motion Planning**: Integrates and develops motion planning algorithms to ensure the robot can move safely and efficiently in its environment.

Given its requirements, this area also develops general tasks useful for other areas, providing methods for moving the arm, keeping the URDF and motion planning updated and collaborating in developing simulation environments.

# Node Overview

## General Nodes

### Manipulation Server
- Manages requests made for pick, place and other object interactions through the robot arm
- Connects to every manipulation node, such as object detectors, 3D perception, motion planning and more. 

### Object Detector 2D
- Uses Computer Vision models to detect and segment objects in 2D images
- Returns both 2D and 3D object locations  

### Perception 3D
Several nodes spawning capabilities such as:
- Extracting surfaces and objects
- Detecting and extracting object of interest' pointclouds and reconstructed meshes

### Place Server
- Incorporates algorithms to determine the best position for placing objects

### Pick and Place Server
- Calls and manages motion planning algorithms to pick and place objects

---