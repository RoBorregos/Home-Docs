# Hardware overview

<p align="center">
  <img src="/assets/overview/FRIDA.jpg" alt="Robot Image">
</p>

### Mobility and Manipulation
A modified **EAI Dashgo B1** robot was used for mobility purposes, and a **uFactory xArm 6** was added for manipulation tasks and to mount the depth camera.

### Components

#### Base
- Chassis with a differential wheel configuration.
- Motors with encoders for odometry purposes.

#### Computers
- **Jetson Xavier AGX**: Handles manipulation and vision tasks.
- **Jetson Nano**: Manages movement and sensor processing via a local Ethernet network.

#### Batteries
- **24V Batteries**: Powers the xArm 6, Dashgo, and Jetson Nano.
- **14.8V Battery**: Powers the Jetson Xavier.

#### Arm
- **Manipulator**: uFactory xArm 6.
- **Gripper**: Universal custom gripper, interchangeable with:
  - Parallel gripper.
  - High-precision gripper for small objects.
  - High-strength gripper using a stepper motor.

#### Vision
- **Camera**: Stereolabs ZED2 attached to the xArm's end effector (EOF), transmits vision data via USB to the Jetson Xavier.

#### Human-Robot Interaction (HRI)
- **Microphone**: Seed Studio ReSpeaker Microphone Array.
- **Speaker**: Logitech X100 Wireless Portable Speaker.
- **Display**: HDMI LCD touchscreen display.

#### Navigation
- **Lidar**: RP Lidar A1.

#### Base Cover
- Custom sheet metal structure for passive heat dissipation.

#### Physical Specifications
- **Height**: 186 cm (fully extended).
- **Width**: 42 cm.
- **Weight**: 37 kg.

### Additional Devices
- **Power Indicators**: For the xArm 6 and Jetson Xavier batteries.
- **5V Ethernet Switch**: Enables local data transmission.
- **Emergency Stop Devices**: Independent for Jetson Xavier, xArm controller, and Dashgo.
- **Customized Gripper Controller**.

---



