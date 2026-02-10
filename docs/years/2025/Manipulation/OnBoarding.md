# Manipulation Onboarding Guide

## Cloning

Be aware manipulation uses several submodules to work properly. You can clone the repository with the following command:
```bash
git clone --recurse-submodules
```

Or initiate the submodules after cloning with:
```bash
git submodule update --init --recursive --remote
```

## Docker

Installation of every requirement used for this area can be both slow and difficult, particularly when using GPUs. Follow the guide from [this repo](https://github.com/EmilianoHFlores/ros-docker) to install docker with GPU support. GPU is NOT required, but it is highly recommended to use it for faster simulation and inference when using neural networks.

Once you have docker installed, you can use the following command to run the manipulation docker image:
```bash
./run.sh manipulation
```

You may need to run this more than once when building the image or every time you boot your PC to turn on the container. You will notice you are inisde the container when you see yourself inside the container's terminal, which will look like this:

```bash
ros@host:/workspace$
```

## Running

If you use docker, assume all this is running within the container.

### Simulation
Launch the robot with our simulation environment on gazebo and loading gripper and 3D camera:
```bash
ros2 launch frida_description moveit.launch.py load_zed:=true
```

### Real Robot
#### Robot interface
On the real robot, run the following commands. Remember to ssh to the robot first:
```bash
ssh orin@<robot_ip>
cd home2
./run.sh manipulation
ros2 launch arm_pkg frida_moveit_config.launch.py
```

#### 3D Camera
To run the 3D camera, while on the device connected to it, run the following command:
```bash
ssh orin@<robot_ip>
ros2 launch zed_wrapper zed_camera.launch.py camera_model:=zed2 publish_tf:=false
```

## Pick and Place

Whether you are on simulation or on the real robot, you can run the pick and place nodes with the following command:
```bash
ros2 launch pick_and_place pick_and_place.launch.py
```

### Vision

To get object detections going, you have two options:

#### Using vision container

Launch the vision docker container with the following command, this one launches the object detector and the zero-shot object detector:
```bash
./run.sh vision --storing-groceries
```

#### Using manipulation container

```bash
./run.sh manipulation
ros2 launch object_detector_2d object_detector_node.launch.py
ros2 launch object_detector_2d zero_shot_object_detector_node.launch.py
```
Either of them will work, second one will allow you to use zero-shot detection, which classes you can edit in the vision_constants.py file within frida_constants package.

#### Visualizing

Use rqt's image plugin to visualize what your camera is seeing. You will also be able to change topics and the object detectors will pop up in the list of topics. Use this to visualize if it is working correctly:
```bash
rqt
```
Add the image plugin by clicking on Plugins -> Visualization -> Image View. Then select the topic you want to visualize, such as `/zed2/zed_node/left/image_rect_color`.

### Trying up pick & place
Launch the keyboard node to try picking objects up:
```bash
ros2 run pick_and_place keyboard_input.py
```
When running this node, you will see printed if the robot is seeing a detected object. Change the zero shot classes or use a trained model to detect different objects. When the robot sees something, trigger tasks by following the instructions printed on the terminal.

## Troubleshooting

Should anything go wrong, you can always call your fellow manipulation team members for help. This year, we have people working on these areas:

- **Pipeline and Motion Planning**: Emiliano Flores, José Luis Domínguez, Ricardo Guerrero
- **3D Perception**: Iván Romero
- **2D Perception**: Emiliano Flores
- **Simulation and Real Robot**: Emiliano Flores, Gerardo Fregoso, David Vázquez