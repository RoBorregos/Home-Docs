---
title: "FRIDA Description"
---

# FRIDA Description

!!! info "Synced from home2"
    Generated from [`home2/robot_description/frida_description/README.md`](https://github.com/RoBorregos/home2/blob/f0c8ff3c9c6d1c0cdd0fe4ccf516eefa026d8966/robot_description/frida_description/README.md) @ `f0c8ff3` by `scripts/sync_home2_readmes.py`. Edit the README in home2 instead of this page.

Command to run FRIDA simulation in Gazebo:

```python
ros2 launch frida_description moveit.launch.py add_gripper:=true add_realsense_d435i:=true
```

> [!WARNING]
> If the arm spawns incorrectly, please run again the simulation and check through the arm transform in the Rviz window
