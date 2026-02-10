# OnBoarding

For the computer vision area, here are some reccommendations to get started:

## Python3
Python is the main language used in vision, so it would be a good idea to get familiar with it if you are new to python. You can check the following resources:

- [Python3 Documentation](https://docs.python.org/3/)

## Vision tools
Here are some of the libraries and tools used in the vision area:

- [Vision tools](https://github.com/Ale-Coeto/vision-algorithms)

A recommended exercise is to use openCV and YOLO to detect a person and draw the bounding box.

## Terminal
You will probably be using the terminal a lot, so it is recommended to get familiar with the most used commands. Here are some resources:

- [Linux Command Line Basics](https://ubuntu.com/tutorials/command-line-for-beginners#1-overview)

## ROS2
We currently use the ROS2 (humble) framework. This is a very useful tool in robotics, used mostly for communication between different modules and devices. It allows us to create nodes that can publish and subscribe to topics, making it easier to integrate different components of the robot.

It is recommended to install ubuntu to use ROS2, however it is also possible to use it with Docker, but not recommended when starting out. Make sure to check the official documentation for installation and tutorials:

- [ROS2 Installation](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html)

- [ROS2 Tutorials](https://docs.ros.org/en/humble/Tutorials.html)

Also, make sure to check out how we use ROS2 in the home2 repo. If possible, try to run some of the examples:

- [Home2 ROS2](../../codelabs/ros2.md)

## Docker
Docker is a tool that we use to run the modules in containers. This allows us to have a consistent environment across different machines and it gets everything setup and ready to use. It is not necessary to understand it at fist because we already have bash scripts that run everything automatically, but it is a powerful tool worth learning.

You can check the official documentation for installation and tutorials:

- [Docker Installation](https://docs.docker.com/get-docker/)
- [Docker Tutorials](https://docs.docker.com/get-started/)

Finally, check out how to run the vision module using Docker in the home2 repo:

- [Run Vision with Docker](https://github.com/RoBorregos/home2/blob/main/docs/Run/Areas/vision.md)

To ensure everything runs properly, try to run the zed-simulator (this will simulate the zed using your own webcam) and the face recognition node. 

## Check out the docs
Finally, check out our documentation to see the different subareas, current implementations and areas of improvement.

- [Docs 2025](../../../years/2025/Computer%20Vision/index.md)
- [Architecture](Architecture.md)
