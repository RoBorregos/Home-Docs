# Achievements from 2026

This year, after being [accepted](https://athome.robocup.org/2026-qualified-teams/) to participate in RoboCup 2026 held in Incheon, South Korea, the team focused on replacing the commercial base with a custom omnidirectional base, hardening the software for the updated rulebook tasks (HRIC, Pick and Place Challenge, Laundry, Restaurant and GPSR), and standardizing how every area builds, runs and is tested. The team won **1st place at the Mexican Robotics Tournament (TMR 2026)** and placed **9th at RoboCup 2026** (July; Incheon, South Korea). See [Competition History](../../Overview/Achievements.md).

<iframe width="560" height="315" src="https://www.youtube.com/embed/qUQNTDRBEKw" title="RoboCup@Home Video 2026" frameborder="0" allowfullscreen></iframe>

After the competition, the team started the migration to ROS 2 Jazzy and JetPack 7 to prepare for RoboCup 2027 (see [Since RoboCup 2026](#since-robocup-2026)).

These are the major achievements divided by area:

## Integration

### Software Architecture

- CycloneDDS adopted as the DDS middleware across all areas, with shared memory transport between containers.
- Reworked `run.sh` and `stop.sh` scripts with common flag parsing for every area and task.
- Docker images are built and published automatically with a GitHub Action, with separate CPU, CUDA and L4T images.
- USB devices (lidars, base, microphone) are identified by serial number and exposed through fixed symlinks.
- Colored logger for task managers, with one color per subsystem.
- Mock-based tests for the task managers of each area.

### Tasks

- New task managers for the **HRI Challenge (HRIC)**, the **Pick and Place Challenge (PPC)**, **Laundry** and **Restaurant**.
- GPSR: plan confirmation with the operator, merging of consecutive commands into a single plan, and an LLM pass to make the merged plan sound natural.

## Human-Robot Interaction

- The display was migrated to a ROS package, with dedicated pages per task (Laundry, Restaurant, PPC, HRIC), auto-reconnect for ROS and the video stream, and a loading screen.
- Adaptive voice activity detection (VAD), DeepFilterNet noise reduction and an acoustic noise cancellation model.
- Improved hotwords, word confidences in the STT output and ReSpeaker detection.
- Door and doorbell/knock detection for HRIC.
- NLP tests migrated to BAML native tests, and Qwen 3.5 served through Ollama.

## Computer Vision

- A single centralized YOLO node shared by all vision tasks.
- New detections: [trash and trashcans](Computer%20Vision/Object%20Detection/Trash%20Detection.md), cutlery, hands, customers (Restaurant) and dishwasher.
- [Person tracking](Computer-Vision/Tracker/info.md) with DeepSORT and a Swin Transformer ReID model.
- Zero-shot object detection with frame skipping, and duplicated and far detections handling.
- `vision_general` separated from the model nodes (`models-ros`), and a standardized 2D to 3D point conversion.

## Manipulation

- IKFast analytical IK solver plugin for the xArm6.
- `ros2_control` integration and improved 3D perception.
- Per-level shelf pick with vision confirmation, and a pick feasibility check.
- New skills: place laundry, place trash, place bag, pour, pick cutlery, pick bowl and hand to hand.
- A global manipulation safeguard toggle.

## Navigation

- Full navigation refactor with a lifecycle manager and navigation monitoring.
- Map contextualizer and map cleaner to tag areas on the map.
- Nav2 configuration for the custom omnidirectional base (first with 3 wheels, then 4).
- New maps and areas for the Incheon arena.

## [Mechanics](Mechanics/index.md)

- Custom omnidirectional base designed and built by the team, replacing the Dashgo B1. See [Omnibase](../../Areas/Omnibase.md).
- Taller structure, new speaker and display mounts, and an updated gripper.

## Since RoboCup 2026

Work done after the competition (August to October 2026), in preparation for RoboCup 2027:

- Migration of every area to **ROS 2 Jazzy** and of the L4T images to **JetPack 7**.
- **Gazebo Harmonic** simulation of FRIDA, replacing the old Gazebo and MuJoCo code.
- **Semantic navigation**.
- Geometric grasp generator with a cartesian approach pick, and a refactor of the pick and place package.
- Voice and talking detection in vision.
- Vision Docker image reduced from 66.8 GB to 25.1 GB.
- New object detection model trained for TMR 2026.
- The display saves per-run evidence (logs, captures and gallery).
