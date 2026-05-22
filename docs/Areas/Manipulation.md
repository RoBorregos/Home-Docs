# Manipulation

Dynamic manipulation is what lets a service robot **interact** with an unstructured world. Instead of executing pre-programmed actions, FRIDA must sense changes in its environment, plan its trajectories, and grasp objects whose shape, size, and material vary from one trial to the next. Robust manipulation opens the door to tasks like meal preparation, item delivery, opening containers, and handing objects to people, all under live human-robot collaboration.

Our pick & place pipeline is built around a **6-DOF UFactory xArm 6** with a custom 2-finger gripper, perceived by a **ZED 2** stereo camera, and planned through **MoveIt 2**.

## Pipeline at a glance

1. **2D Detection**, the Vision area classifies and locates objects in the RGB stream.
2. **3D Perception**, the detection is fused with the ZED point cloud; we segment the supporting plane (RANSAC) and extract the target object cluster (Euclidean clustering on PCL).
3. **Collision Scene**, the plane becomes a collision box and the object becomes a set of spheres or a reconstructed mesh, all pushed to the MoveIt planning scene.
4. **Grasp Generation**, the **GPD** library scores candidate grasps on the object cluster. For thin objects (cutlery), a top-down PCA-aligned pose is computed directly.
5. **Motion Planning**, MoveIt 2 plans a collision-free trajectory using **RRTConnect**, with the **IKFast** analytical IK solver.
6. **Execution**, the trajectory is sent to the xArm driver; the gripper closes; a force-guarded descent variant exists for cutlery to avoid table impact.
7. **Placement**, a Gaussian heatmap on the table cloud chooses the best free spot, with optional directional constraints ("close to", "left of", …).

## Architecture

The Manipulation area exposes a single ROS 2 action, `ManipulationAction`, that every task manager calls. A central `manipulation_core` node orchestrates specialized **Managers** (`PickManager`, `PlaceManager`, `PourManager`) which coordinate detection, perception, grasp generation, and motion in sequence. All motion is funnelled through a `motion_planning_server` that wraps MoveIt 2 and the xArm driver.

## Highlights

- **Dual-heatmap placing**, Gaussian heat kernel over free space combined with a Gaussian cool kernel over obstacles. Supports directional placements (`close_to`, `front`, `back`, `left`, `right`) and a forced-pose mode.
- **Pouring**, orientation-aware path planning above the container centroid; supports an *already-grasped* mode to chain pick → pour → place without re-picking.
- **Cutlery picks**, top-down PCA-aligned grasp pose with a force-guarded descent (xArm mode 5, joint-effort threshold) so the gripper stops on table contact.
- **Custom gripper**, parallel rack-and-pinion mechanism with fractal silicone fingers, payload up to 1 kg. Grasp feedback exposed on `/gripper/grasp_state`.

## Read more

- For day-to-day engineering, see the **[Manipulation development documentation](../development/manipulation/overview.md)**, setup, architecture, packages, running tasks, and interfaces.
