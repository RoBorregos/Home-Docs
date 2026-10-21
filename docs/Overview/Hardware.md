# Hardware overview

<div class="timeline-compare">
  <div class="timeline-item">
    <div class="label">2023</div>
    <div class="timeline-image-wrap">
      <img class="timeline-image" src="/assets/overview/robot.jpg" alt="Robot 2023" />
    </div>
  </div>

  <div class="timeline-arrow" aria-hidden="true">&rarr;</div>

  <div class="timeline-item">
    <div class="label">2024</div>
    <div class="timeline-image-wrap">
      <img class="timeline-image" src="/assets/overview/FRIDA.jpg" alt="Robot 2024" />
    </div>
  </div>

  <div class="timeline-arrow" aria-hidden="true">&rarr;</div>

  <div class="timeline-item">
    <div class="label">2025</div>
    <div class="timeline-image-wrap">
      <img class="timeline-image" src="/assets/overview/frida.png" alt="Robot 2025" />
    </div>
  </div>
</div>

### Mobility and Manipulation
FRIDA moves on a **custom omnidirectional base** designed and built by the team (it replaced the EAI Dashgo B1), and a **uFactory xArm 6** is used for manipulation tasks and to mount the depth camera. See the [Omnibase Overview](../development/omnibase/overview.md) for the base design.

### Components

#### Base
- **Drive**: Four mecanum wheels, each driven by an EaglePower LA8308 90KV brushless motor through a 9:1 gearbox.
- **Motor drivers**: Four ODrive S1 controllers on a CAN bus.
- **Base controller**: STM32H755 running FreeRTOS for the mecanum kinematics and an on-board EKF that fuses wheel odometry with a BNO085 IMU. An ESP32 provides Bluetooth gamepad teleoperation.

#### Computers
- **2× NVIDIA Jetson AGX Orin 64GB**

#### Batteries
- **LiFePO4 pack**: Eight 3.2 V 25 Ah cells in series (25.6 V, 640 Wh) with a Daly BMS, powering the whole robot.

#### Arm
- **Manipulator**: uFactory xArm 6.
- **Gripper**: 2 finger parallel custom 3D printed gripper with force resistive
sensors on each finger and an IR sensor for detecting objects in front of it. It uses an ESP32 as the microcontroller.

#### Vision
- **Camera**: Stereolabs ZED2 attached to the xArm's end effector (EOF), transmits vision data via USB to the Jetson Orin.

#### Human-Robot Interaction (HRI)
- **Microphone**: Seed Studio ReSpeaker Microphone Array.
- **Speaker**: Logitech X100 Wireless Portable Speaker.
- **Display**: HDMI LCD touchscreen display.

#### Navigation
- **Lidar**: Two RPLIDAR C1 at opposite corners of the base, merged into a single 360° scan.

#### Base Cover
- Aluminum profile frame with MDF covers for securing every component and hiding the internal electronics.

#### Physical Specifications
- **Height**: 170 cm (fully extended).
- **Base footprint**: 64 x 50 cm.
- **Weight**: 46 kg.

### Additional Devices
- **Power Indicators**: For the xArm 6 and Jetson Orin batteries.
- **5V Ethernet Switch**: Enables local data transmission.

---



