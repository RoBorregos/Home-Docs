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
A modified **EAI Dashgo B1** robot was used for mobility purposes, and a **uFactory xArm 6** was added for manipulation tasks and to mount the depth camera.

### Components

#### Base
- Chassis with a differential wheel configuration.
- Motors with encoders for odometry purposes.

#### Computers
- **NVIDIA Jetson AGX Orin 64GB**

#### Batteries
- **24V Batteries**: A total of three 24v li-ion batteries are used, one for the xArm,
Jetson Orin and Dashgo.

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
- **Lidar**: RP Lidar A1.

#### Base Cover
- Custom acrylic cover and aluminum profile structure for securing every component and hide the internal electronics.

#### Physical Specifications
- **Height**: 180 cm (fully extended).
- **Base footprint**: 50 x 42 cm.
- **Weight**: 40 kg.

### Additional Devices
- **Power Indicators**: For the xArm 6 and Jetson Orin batteries.
- **5V Ethernet Switch**: Enables local data transmission.

---



