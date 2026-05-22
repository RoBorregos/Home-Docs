---
title: Packages
---

# Packages

All manipulation code lives in `home2/manipulation/packages/`. This page is a directory of what each package is for, what executables it exposes, and which files you should learn first.

!!! tip "Use this page as a reading map"
    Start with [`pick_and_place`](#pick_and_place) and [`frida_motion_planning`](#frida_motion_planning) — together they cover ~80 % of day-to-day work. Move to [`perception_3d`](#perception_3d) and [`arm_pkg`](#arm_pkg) for low-level integrations.

## Directory layout

```
manipulation/packages/                # contents of main as of the current commit
├── arm_pkg                # MoveIt config + GPD service + grasp markers
├── frida_motion_planning  # Python wrappers over MoveIt 2 (action servers)
├── frida_pymoveit2        # FRIDA's xArm 6 binding for pymoveit2
├── gpd                    # GPD C++ library (submodule → RoBorregos/gpd)
├── manipulation_general   # Per-task launch files (gpsr, hric, ppc, …)
├── mujoco_ros2_control    # ros2_control plugin for MuJoCo (submodule)
├── mujoco_spawn           # Launches FRIDA inside MuJoCo
├── perception_3d          # 3D perception (cluster, plane, primitives)
├── pick_and_place         # Pick / Place / Pour servers and orchestrator
├── place                  # Heatmap-based place pose generator
├── pymoveit2              # Vendored pymoveit2 (submodule). Use frida_pymoveit2.
├── xarm6_ikfast_plugin    # IKFast analytical IK plugin for xArm 6
├── xarm_ros2              # xArm ROS 2 driver (submodule → RoBorregos/xarm_ros2)
└── xarm_utils             # Small utilities and launch helpers for xArm
```

!!! info "About `vamp`, `foam`, `cricket`"
    These packages have been **explored in feature branches** but **are not in `main`** as of this writing. If your local checkout has them as untracked directories, treat them as work-in-progress.

---

## arm_pkg { #arm_pkg }

The **central configuration package** for the arm: MoveIt config builder, GPD service, gripper/IK YAMLs, RViz debug.

=== "Layout"

    ```
    arm_pkg/
    ├── arm_pkg/                    # Python configs (MoveIt builders)
    │   ├── moveit_configs_builder.py
    │   ├── moveit_configs_builder_sim.py
    │   └── utils.py
    ├── launch/
    │   ├── frida_moveit_config.launch.py        ← top-level MoveIt launch
    │   ├── frida_moveit_common.launch.py        ← shared fragment
    │   ├── frida_fake_moveit_config.launch.py   ← fake controller variant
    │   └── frida_driver.launch.py               ← driver only
    ├── config/
    │   ├── frida_eigen_params_custom_gripper.cfg          ← GPD prod config
    │   ├── frida_eigen_params_custom_gripper_testing.cfg
    │   ├── gpd_service.yaml         ← ROS params for gpd_service
    │   ├── sensors_3d.yaml          ← OccupancyMapMonitor (octomap)
    │   ├── joint_limits.yaml
    │   └── xarm_params.yaml
    ├── src/
    │   ├── gpd_service.cpp          ← GraspDetection.srv server
    │   └── gpd_test.cpp             ← CLI tester
    ├── scripts/
    │   ├── grasp_markers.py         ← RViz markers for debugging grasps
    │   └── test_env.py
    └── examples/
        └── grasp_detection_example.py
    ```

=== "Key parameters"

    Inside `frida_eigen_params_custom_gripper.cfg`:

    - **`finger_width`**, **`hand_outer_diameter`**, **`hand_depth`** — match the physical gripper geometry.
    - **`num_samples`**, **`approach_step`** — control GPD's sampling density.
    - **`min_grasp_score`** — reject low-confidence grasps.

    Inside `gpd_service.yaml`:

    ```yaml
    /**:
      ros__parameters:
        target_frame: "base_link"
        pcd_default_frame: "base_link"
        transform_timeout: 1.0
    ```

!!! info "Where GPD comes from"
    The library is built from `manipulation/packages/gpd/` into `/workspace/install/gpd` by `setup_gpd.sh`. `arm_pkg/CMakeLists.txt` reads `GPD_INSTALL_DIR` to link against it.

---

## pick_and_place { #pick_and_place }

The **heart** of the manipulation area. Owns `ManipulationAction` and all high-level managers.

=== "Layout"

    ```
    pick_and_place/
    ├── launch/pick_and_place.launch.py        ← brings up the full stack
    └── pick_and_place/
        ├── manipulation_core.py               ← ManipulationAction server
        ├── manipulation_client.py             ← debug — picks at /clicked_point
        ├── keyboard_input.py                  ← interactive REPL
        ├── pick_server.py                     ← PickMotion + GoToHand
        ├── place_server.py                    ← PlaceMotion
        ├── pour_server.py                     ← PourMotion
        ├── fix_position_to_plane.py
        ├── managers/
        │   ├── PickManager.py
        │   ├── PlaceManager.py
        │   └── PourManager.py
        └── utils/
            ├── grasp_utils.py                 ← filter/score GPD outputs
            └── perception_utils.py            ← get_object_point, etc.
    ```

=== "Key files"

    | File | What it does |
    |---|---|
    | `manipulation_core.py` | Top-level action server. Routes requests to managers. |
    | `managers/PickManager.py` | Detection → cluster → grasp generation → pick motion. Has the cutlery sub-path. |
    | `managers/PlaceManager.py` | Cluster → heatmap → place motion. Handles `forced_pose`, `is_shelf`, special requests. |
    | `managers/PourManager.py` | Optional pick → bowl detection → tilt sequence. |
    | `pick_server.py` | Approach / descend / grasp / lift. Force-guarded descent for cutlery. |
    | `place_server.py` | Approach / descend / open / detach / lift. |
    | `keyboard_input.py` | Interactive shell — see [Running Tasks](tasks.md#interactive-keyboard-tool). |

See [Architecture → Pick sequence](architecture.md#pick-sequence-diagram) for the runtime flow.

---

## frida_motion_planning { #frida_motion_planning }

Python wrappers around MoveIt 2. Speaks neither to vision nor perception — a pure motion layer.

=== "Layout"

    ```
    frida_motion_planning/
    ├── launch/
    │   ├── motion_planning_server.launch.py
    │   └── demo_ds4.launch.py                 ← joystick demo
    ├── examples/
    │   ├── call_pose_goal.py
    │   ├── call_joint_goal.py
    │   ├── add_collision_object.py
    │   ├── remove_collision_object.py
    │   ├── ex_orientation_path_constraint.py
    │   ├── ds4_demo.py
    │   └── look_at_example.py
    └── frida_motion_planning/
        ├── motion_planning_server.py          ← action servers + services
        ├── utils/
        │   ├── MoveItPlanner.py               ← pose / joint plan, IK
        │   ├── MoveItServo.py                 ← servo (continuous)
        │   ├── Planner.py / Servo.py          ← base classes
        │   ├── XArmServices.py                ← xarm_api wrappers
        │   ├── service_utils.py               ← gripper helpers, named joints
        │   ├── tf_utils.py                    ← transform_pose, transform_point
        │   └── ros_utils.py                   ← wait_for_future, QoS helpers
        └── util_nodes/
            └── record_joints_node.py          ← snapshot joint state to a service
    ```

=== "What `MotionPlanningServer` exposes"

    | Endpoint | Type | Purpose |
    |---|---|---|
    | `/manipulation/move_to_pose_action_server` | `MoveToPose` action | Plan + execute to a pose. |
    | `/manipulation/move_joints_action_server` | `MoveJoints` action | Plan + execute to joints (numeric). |
    | `/manipulation/get_joints` | `GetJoints` service | Current joint state. |
    | `/manipulation/add_collision_objects` | `AddCollisionObjects` service | Push `CollisionObject[]` to MoveIt. |
    | `/manipulation/remove_collision_object` | `RemoveCollisionObject` service | Remove by id (optionally including attached). |
    | `/manipulation/attach_collision_object` | `AttachCollisionObject` service | Attach to the gripper. |
    | `/manipulation/get_collision_objects` | `GetCollisionObjects` service | List planning-scene objects. |
    | `/manipulation/toggle_servo` | `ToggleServo` service | Enable/disable MoveIt 2 servo. |

---

## perception_3d { #perception_3d }

PCL-based 3D perception. Mixed C++ / Python.

=== "Layout"

    ```
    perception_3d/
    ├── launch/
    │   ├── perception_3d.launch.py     ← pick_primitives + plane_service + orchestrator
    │   └── downsample_pc.launch.py
    ├── src/
    │   ├── add_primitives.cpp          ← cluster + collision primitives
    │   ├── remove_plane.cpp            ← RANSAC plane segmentation
    │   ├── masive_testin.cpp           ← test_only_orchestrator (top-level)
    │   ├── down_sample_pc.cpp          ← voxel downsample
    │   ├── publish_pcl.cpp             ← publish a PCD file
    │   ├── publish_handle.cpp          ← door handle pose publisher
    │   └── read_cluster.cpp            ← read a saved cluster PCD
    ├── scripts/
    │   ├── flat_grasp_estimator.py     ← cutlery grasp pose
    │   ├── dock_to_handle.py           ← nav2 Dock-based alignment
    │   └── record_relative_pose.py
    ├── config/
    │   └── relative_docking_pose.yaml
    └── include/perception_3d/macros.hpp
    ```

=== "Services owned"

    | Owner node | Services |
    |---|---|
    | `pick_primitives` | `AddPickPrimitives`, `GetPlaneBbox` |
    | `plane_service` | `Test`, `RemovePlane`, `ClusterObjectFromPoint`, `RemoveVerticalPlane` |
    | `test_only_orchestrator` | `PickPerceptionService`, `PlacePerceptionService` (the high-level entry points consumed by the managers) |

=== "Tuning knobs"

    | File | What to tune |
    |---|---|
    | `remove_plane.cpp` | RANSAC `setMaxIterations` (1000), `setDistanceThreshold` (0.03 m), Euclidean cluster `setClusterTolerance` (0.04 m), min/max cluster sizes. |
    | `add_primitives.cpp` | Voxel leaf size for cluster downsampling; primitive shape choice (spheres vs mesh). |
    | `down_sample_pc.cpp` | Per-call `small_size`, `medium_size`, `large_size` voxel leaves. |
    | `flat_grasp_estimator.py` | `GRASP_SURFACE_OFFSET` (3 mm), `MIN_POINTS_FOR_PCA` (10), table-height buffer + outlier rejection. |

---

## place { #place }

Pure-Python heatmap-based place pose finder.

```
place/
├── scripts/heatmapPlace_Server.py         ← HeatmapPlace service
└── place/
    └── heatmap_generators/
        └── close_by_generators.py         ← close_to / front / back / left / right
```

??? abstract "Algorithm (heatmap_place_service)"
    1. Read the incoming `PointCloud2` (must be in `base_link`).
    2. Filter points to a `PLACE_MAX_DISTANCE` (0.8 m) disk.
    3. Rasterize into a 2D occupancy grid with `grid_size = 0.015 m`.
    4. Convolve with a Gaussian **heat** kernel (`length = 0.3 m`, `weight = 1.0`) on free space.
    5. Convolve with a Gaussian **cool** kernel (`length = 0.15 m`, `weight = 10.0`) on occupied space.
    6. `final = heat - cool`, clipped to `[0, ∞)`.
    7. If `prefer_closest`: multiply by an exponential closeness-to-origin map (cubed for sharper decay).
    8. If `special_request` (JSON): apply directional or close-to overlay from `close_by_generators`.
    9. Return the argmax as `PointStamped`.

    Debug topics: `/manipulation/table_place_point_debug` and a saved PNG of the heatmap.

---

## manipulation_general { #manipulation_general }

Per-task launch files. Each composes `arm_pkg/frida_moveit_config.launch.py` with `pick_and_place/pick_and_place.launch.py` plus task-specific extras.

| Launch file | What it brings up |
|---|---|
| `ppc.launch.py` | MoveIt + full pick/place stack. **No extras.** Pick & Place Challenge. |
| `gpsr.launch.py` | MoveIt + full pick/place stack + `follow_face_node`. |
| `restaurant.launch.py` | MoveIt + full pick/place stack + `follow_face_node`. |
| `hric.launch.py` | MoveIt + `motion_planning_server` + `follow_face_node` + `pick_server` (no place/pour). |
| `receptionist.launch.py` | MoveIt + `motion_planning_server` + `follow_face_node`. No pick. |
| `carry.launch.py` | MoveIt + `motion_planning_server` + a low-resolution downsampler for navigation. |

!!! tip "Adding a new task"
    Don't fork `pick_and_place.launch.py`. Compose existing launches in a new file inside `manipulation_general/launch/`.

---

## Simulation packages

### mujoco_spawn { #mujoco_spawn }

Bootstraps MuJoCo with FRIDA. `mujoco_sim_init.launch.py`:

- Writes a `MJCF` scene to `/tmp/mujoco/main.xml`.
- Starts MuJoCo.
- Optionally launches MoveIt and perception inside the sim (`launch_moveit:=true`, `launch_perception:=true`).

### mujoco_ros2_control { #mujoco_ros2_control }

Vendored `ros2_control` plugin that lets MuJoCo expose the same controller interfaces as the real arm. Files of note:

- `mjcf/scene.xml` — the FRIDA scene.
- `scripts/xacro2mjcf.py`, `scripts/urdf2mjcf.py` — URDF → MJCF conversion.
- `scripts/run_coacd.py` — convex decomposition of meshes (required for accurate MuJoCo collisions).

---

## gpd { #gpd }

The Grasp Pose Detection C++ library — submodule pointing to [RoBorregos/gpd](https://github.com/RoBorregos/gpd) (a fork of [atenpas/gpd](https://github.com/atenpas/gpd)). Built into `/workspace/install/gpd` by `setup_gpd.sh`. Exposed to ROS through `arm_pkg`'s `gpd_service`.

---

## xArm packages

### xarm_ros2

Official xArm ROS 2 driver, vendored. Provides `xarm_api`, `xarm_controller`, `xarm_moveit_config`, `xarm_description`, `xarm_msgs`, `xarm_planner`, `xarm_moveit_servo`, `uf_ros_lib`, and the C++ SDK under `xarm_sdk/`.

### xarm6_ikfast_plugin

Generated IKFast analytical IK plugin for the xArm 6. Significantly faster than KDL for pick planning. Selected via the MoveIt kinematics YAML.

### xarm_utils

Small package with helper launches/utilities specific to our integration (mode switching, joint recording).

---

## pymoveit2 / frida_pymoveit2 { #frida_pymoveit2 }

- **`pymoveit2`** — upstream Python MoveIt 2 wrapper, vendored.
- **`frida_pymoveit2`** — our derivative with FRIDA-specific group names, IK frames, and named configurations.

When wiring new motion code, prefer `frida_pymoveit2.robots.xarm6` — it has the right defaults. Touch upstream `pymoveit2` only when fixing a real bug.

---

## Quick rebuild reference

```bash
# In the manipulation container, /workspace
build                                                # the alias — most common
colcon build --symlink-install --packages-select arm_pkg
colcon build --symlink-install --packages-select pick_and_place
colcon build --symlink-install --packages-select frida_motion_planning
colcon build --symlink-install --packages-select perception_3d place
colcon build --symlink-install --packages-select xarm6_ikfast_plugin
```

For a full rebuild use the `build` alias (see [Setup](setup.md#rebuilding)).
