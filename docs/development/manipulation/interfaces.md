---
title: Interfaces
---

# Interfaces

Reference for every `.action`, `.srv`, and `.msg` under `frida_interfaces/manipulation/`. Endpoint names live in [`frida_constants/manipulation_constants.py`](https://github.com/RoBorregos/home2/blob/main/frida_constants/frida_constants/manipulation_constants.py) — always import them, never hard-code.

!!! abstract "Conventions used below"
    - Each block reproduces the **exact** content of the corresponding `.action`/`.srv`/`.msg` file.
    - Action sections are separated into Goal / Result / Feedback by the `---` lines.
    - All distances are in meters, angles in radians (unless noted), velocities in m/s.

## Top-level action

### `ManipulationAction.action`

The **only** action a task manager should call for picking / placing / pouring.

```
# Goal
int8 task_type                # ManipulationTask.{PICK, PICK_CLOSEST, PLACE, POUR}
PickParams pick_params
PlaceParams place_params
PourParams pour_params
bool scan_environment         # if true, sweep + keep the octomap (used for shelves)
---
# Result
int32 success                 # 1 on success, 0 on failure
---
# Feedback
string execution_state        # human-readable progress
```

Server: `/manipulation/manipulation_action_server` (constant `MANIPULATION_ACTION_SERVER`).

### `ManipulationTask.msg`

```
int8 PICK         = 0
int8 PICK_CLOSEST = 1
int8 PLACE        = 2
int8 POUR         = 3
```

### `PickParams.msg`

```
geometry_msgs/PointStamped object_point   # optional explicit 3D point; ignored if object_name resolves via vision
string object_name                        # label (must match a vision class or zero-shot input)
float32 max_distance                      # detection filter bounds (m)
float32 min_distance
bool closest                              # prefer closest detection
bool largest                              # prefer largest cluster
bool in_configuration                     # if false, the arm will move to a stare pose first
```

### `PlaceParams.msg`

```
float32 table_height                      # override detected plane (m)
float32 table_height_tolerance
bool is_shelf                             # keep octomap, stay in current pose
string close_to                           # name of a known object to bias toward
string special_request                    # JSON, see below
geometry_msgs/PoseStamped forced_pose     # if non-empty, skip heatmap and use this
```

??? example "`special_request` JSON examples"

    ```json
    {"request":"close_by","object":"sugar","position":"left"}
    {"request":"close_by","object":"box","position":"front"}
    ```

    Valid `position` values: `close`, `front`, `back`, `left`, `right`.

### `PourParams.msg`

```
string object_name              # what to pour (must be in POUR_OBJECT_NAMES if upright)
string bowl_name                # what to pour into
bool object_already_grasped     # if true, skip the pick stage
```

### `PickResult.msg`

```
geometry_msgs/PoseStamped pick_pose
float32 grasp_score
string object_name
float32 object_pick_height      # detected object height (m)
float32 object_height
```

## Internal motion actions

### `PickMotion.action`

```
# Goal
geometry_msgs/PoseStamped[] grasping_poses
float64[]                   grasping_scores
string                      object_name
---
# Result
int32      success
PickResult pick_result
---
# Feedback
string execution_state
```

Server: `/manipulation/pick_motion_action_server`. Picks the best of `grasping_poses` (scored by `grasping_scores`) and executes approach / descend / grasp / lift.

### `PlaceMotion.action`

```
# Goal
geometry_msgs/PoseStamped place_pose
string                    object_name
PlaceParams               place_params
---
# Result
int32 success
---
# Feedback
string execution_state
```

Server: `/manipulation/place_motion_action_server`.

### `PourMotion.action`

```
# Goal
geometry_msgs/PoseStamped pour_pose
frida_interfaces/PickResult pick_result
bool                      object_already_grasped
---
# Result
int32      success
PickResult pour_result
---
# Feedback
string execution_state
```

Server: `/manipulation/pour_motion_action_server`. The `PourParams` from the top-level action are unpacked by `manipulation_core`; the internal action receives the computed pour pose and the prior pick result.

### `MoveToPose.action`

```
# Goal
geometry_msgs/PoseStamped pose
float32 velocity
float32 acceleration
float32 planning_time
int32   planning_attempts
float32 tolerance_position
float32 tolerance_orientation
string  planner_id
string  target_link            # default: link_eef
bool    apply_constraint
frida_interfaces/Constraint constraint
---
# Result
int32 success
---
# Feedback
string execution_state
```

Server: `/manipulation/move_to_pose_action_server`.

### `MoveJoints.action`

```
# Goal
float64[] joint_positions
string[]  joint_names           # if empty, joints in chain order
float32   velocity
float32   acceleration
float32   planning_time
int32     planning_attempts
string    planner_id
bool      apply_constraint
frida_interfaces/Constraint constraint
---
# Result
int32 success
---
# Feedback
string execution_state
```

Server: `/manipulation/move_joints_action_server`.

!!! warning "No `named_position` field on the action"
    The Python helper `frida_motion_planning.utils.service_utils.move_joint_positions(named_position=...)` resolves the name from `frida_constants.xarm_configurations` and fills `joint_positions` before sending the goal.

### `GoToHand.action`

```
# Goal
geometry_msgs/PointStamped point
float32 hand_offset 0.1
---
# Result
int32 success
---
# Feedback
string execution_state
```

Server: `/manipulation/go_to_hand_action_server`. Used by HRIC: vision publishes a hand point, the EE stops `hand_offset` short of it along the approach axis.

## Services

### Perception

#### `PickPerceptionService.srv` *(test_only_orchestrator)*

```
geometry_msgs/PointStamped point
bool                       add_collision_objects
---
sensor_msgs/PointCloud2 cluster_result
```

#### `PlacePerceptionService.srv` *(test_only_orchestrator)*

```
PlaceParams place_params
---
sensor_msgs/PointCloud2 cluster_result
```

#### `GraspDetection.srv` *(gpd_service)*

```
# Request
string                  cfg_path
string                  pcd_path
sensor_msgs/PointCloud2 input_cloud
---
# Response
bool                          success
string                        message
geometry_msgs/PoseStamped[]   grasp_poses
float64[]                     grasp_scores
```

#### `HeatmapPlace.srv` *(heatmap_place_service)*

```
sensor_msgs/PointCloud2    pointcloud
bool                       prefer_closest
geometry_msgs/PointStamped close_point
string                     special_request
---
geometry_msgs/PointStamped place_point
bool                       success
```

#### `RemovePlane.srv` *(plane_service)*

```
bool                       extract_or_remove   # true → return the plane, false → return cloud minus plane
geometry_msgs/PointStamped close_point         # optional
float32                    min_height
float32                    max_height
---
sensor_msgs/PointCloud2 cloud
int32                   health_response
```

#### `RemoveVerticalPlane.srv` *(plane_service)*

Same shape as `RemovePlane.srv` but targets vertical planes (walls, shelf backs).

#### `ClusterObjectFromPoint.srv` *(plane_service)*

```
geometry_msgs/PointStamped point
bool                       is_get_all_other_surrounding_objects
---
sensor_msgs/PointCloud2 cluster
int32                   status
```

#### `AddPickPrimitives.srv` *(pick_primitives)*

```
sensor_msgs/PointCloud2 cloud
bool                    is_plane
bool                    is_object
bool                    is_other_objects
---
uint32 status
```

#### `GetPlaneBbox.srv` *(pick_primitives)*

```
float32 min_height
float32 max_height
---
geometry_msgs/PointStamped pt1
geometry_msgs/PointStamped pt2
geometry_msgs/PointStamped pt3
geometry_msgs/PointStamped pt4
geometry_msgs/PointStamped center
geometry_msgs/PointStamped highest
geometry_msgs/PointStamped lowest
int32                      health_response
bool                       state
```

### Motion planning scene *(motion_planning_server)*

#### `AddCollisionObjects.srv`

```
frida_interfaces/CollisionObject[] collision_objects
---
bool success
```

#### `RemoveCollisionObject.srv`

```
string id
bool   include_attached
---
bool success
```

#### `AttachCollisionObject.srv`

```
string   id
string   attached_link
string[] touch_links
bool     detach
---
bool success
```

#### `GetCollisionObjects.srv`

```
---
frida_interfaces/CollisionObject[] collision_objects
bool                               success
```

### Arm state and motion

#### `GetJoints.srv` *(motion_planning_server)*

```
---
float32[] joint_positions
string[]  joint_names
```

#### `ToggleServo.srv` *(motion_planning_server)*

```
bool enable
---
bool success
```

### Other

#### `PlayTrayectory.srv` *(motion_planning_server)*

Replays a recorded joint trajectory by name.

#### `DockToHandle.srv` *(dock_to_handle.py)*

Wraps the nav2 `Dock` action to align with a previously-published door handle pose.

#### `Test.srv` *(plane_service)*

```
string base_name
---
int32 success
```

Internal smoke test.

## Messages

### `CollisionObject.msg`

```
string                    id
string                    type
geometry_msgs/PoseStamped pose
geometry_msgs/Point       dimensions  # length, width, height
shape_msgs/Mesh           mesh
string                    path_to_mesh
```

### `Constraint.msg`

```
geometry_msgs/Quaternion orientation
string                   frame_id
string                   target_link
float64[]                tolerance_orientation
float64                  weight
int32                    parameterization
```

### `GripperGraspState.msg`

```
bool object_detected
```

Published on `/gripper/grasp_state`.

## Topic reference

| Topic | Direction | Purpose |
|---|---|---|
| `/manipulation/flat_grasp_pose` | pub: `flat_grasp_estimator` | Live top-down cutlery grasp candidate. |
| `/gripper/grasp_state` | pub: gripper driver | `GripperGraspState` — has-contact flag. |
| `/manipulation/table_place_point_debug` | pub: `heatmap_place_service` | Last place point chosen. |
| `/manipulation/debug_pose_goal` | pub: `motion_planning_server` | Last pose goal received. |
| `/manipulator/place_ee_link_pose` | pub: `place_server` | Last EE pose used in a place. |
| `/manipulation/debug_object_point` | pub: `PourManager` | Pour: object 3D point. |
| `/manipulation/debug_bowl_point` | pub: `PourManager` | Pour: bowl 3D point. |
| `/manipulation/debug_bowl_centroid` | pub: `PourManager` | Pour: bowl cluster centroid. |
| `/clicked_point` | sub: `manipulation_client` | RViz click → trigger pick. |
| `/clear_octomap` | service `std_srvs/Empty` | MoveIt octomap reset. |
| `/zed/zed_node/point_cloud/cloud_registered` | sensor | Raw ZED point cloud (real robot). |
| `/filtered_cloud` | filter | MoveIt self-filtered cloud (sim default input). |
| `/point_cloud` | downsampled | Default input to perception. |

For any name not in this table, grep `frida_constants/manipulation_constants.py` — it is the source of truth.
