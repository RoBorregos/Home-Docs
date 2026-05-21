---
title: Manipulation 2026
---

# Manipulation — 2026

The 2026 cycle focused on **closing the loop** on the pick-&-place pipeline that landed at TMR 2025 and extending it toward the new RoboCup tasks: HRIC handovers, restaurant service, cutlery handling, and full simulation parity. Most of the work happened on top of the existing `pick_and_place` stack and the new MuJoCo simulation environment, with the introduction of **IKFast** as the default analytical IK solver.

This year also marked the first appearance of a dedicated **Pick-&-Place Task Manager**, decoupling the manipulation pipeline from the per-task state machines.

!!! info "Scope of this page"
    Everything listed below has been **merged into `main` of `home2`**. VAMP / `foam` / `cricket` work was explored on a feature branch during the cycle but is **not** part of the merged code, so it is not documented here.

!!! tip "Where to go next"
    - **Engineering reference** (how to run things, packages, APIs) → [Manipulation development docs](../../../development/manipulation/overview.md).
    - **Week-by-week development log** → [Spotlights](../../../development/manipulation/spotlights.md).

## Headlines

<div class="grid cards" markdown>

-   :material-routes:{ .lg .middle } **Motion planning**

    ---

    IKFast plugin shipped as the default kinematics solver
    ([#856](https://github.com/RoBorregos/home2/pull/856)). `xarm_ros2`
    submodule pinned to `roborregos_custom` with services enabled
    ([#729](https://github.com/RoBorregos/home2/pull/729)).

-   :material-hand-back-right:{ .lg .middle } **Pick & Place pipeline**

    ---

    Cutlery picks via force-guarded descent. Gripper grasp-feedback
    integration. Distance filter on detections. Place-on-top, place-on-floor,
    dishwasher placement, directional places.

-   :material-account-multiple:{ .lg .middle } **HRI support**

    ---

    `GoToHand` action server for handovers. Move-to-point integrated into
    HRIC. Bag-pose search while navigating.

-   :material-cube-outline:{ .lg .middle } **3D perception**

    ---

    Plane-rotation fix. Variable-resolution voxelization + parallel
    filtering. Research on transparent-object grasping (ClearGrasp / ASGrasp).

-   :material-robot-industrial:{ .lg .middle } **Simulation**

    ---

    MuJoCo + `ros2_control` parity end-to-end. Gripper fix. Receptionist
    scene. Point-cloud round-trip validated.

-   :material-book-open-page-variant:{ .lg .middle } **Documentation**

    ---

    TDP 2026 reviewed. New development docs (this site) authored. Repo
    cleanup on Orin; CI green on CPU, CUDA, and L4T.

</div>

## Breakdown by area

### :material-routes: Motion planning

- **Analytical IK for xArm 6 (IKFast)** — added the `xarm6_ikfast_plugin` package and made it the kinematics solver for MoveIt. Significantly reduces IK time inside the pick planner. ([#856](https://github.com/RoBorregos/home2/pull/856))
- **`xarm_ros2` submodule fix** — pinned to the `roborregos_custom` branch with the services we depend on enabled. ([#729](https://github.com/RoBorregos/home2/pull/729))

### :material-hand-back-right: Pick & Place pipeline

- **Pick cutlery (force-guarded descent)** — new code path for forks, knives, and spoons. The arm enters xArm mode 5 and descends at ~20 mm/s; `flat_grasp_estimator.py` provides a top-down PCA-aligned grasp pose, and the pick aborts on a joint-effort threshold so the gripper doesn't slam the table. ([#797](https://github.com/RoBorregos/home2/pull/797))
- **Improved picks** — pre-grasp logic and approach-axis offsets, addressing the long-standing "picks too low / collides with table" issue. ([#832](https://github.com/RoBorregos/home2/pull/832))
- **`EEF_CONTACT_LINKS` update** — extended the allowed contact-link list to cover the gripper and finger geometry so MoveIt's collision check stops false-positiving on grasp contact. ([#833](https://github.com/RoBorregos/home2/pull/833))
- **Grasp feedback from the custom gripper** — renamed `ir_gripper` → `grasp_detector` and exposed the on-board grasp-detection signal via TGPIO so the pipeline can read whether the gripper actually holds something. ([#850](https://github.com/RoBorregos/home2/pull/850))
- **Distance mask for picks** — vision detections are filtered by `min_distance` / `max_distance` (`pick_params`) before being considered, so the robot never tries to pick objects clearly out of reach. ([#659](https://github.com/RoBorregos/home2/pull/659))
- **Place bag on the floor** — dedicated place pipeline for the carry task. ([#696](https://github.com/RoBorregos/home2/pull/696))
- **Pour refactor — object already grasped** — `PourMotion` no longer re-picks when the source object is already in the gripper, enabling chained pick → pour → place sequences. ([#828](https://github.com/RoBorregos/home2/pull/828))
- **Pick plane removal** — refined how the supporting plane interacts with the pick collision model; padding-scale adjustments. ([#974](https://github.com/RoBorregos/home2/pull/974))

### :material-account-multiple: Task-manager layer (new)

- **Pick-&-Place Challenge node** — initial cut of the standalone PPC task manager. ([#851](https://github.com/RoBorregos/home2/pull/851))
- **PPC TMR 2026** — challenge-specific updates and integration. ([#918](https://github.com/RoBorregos/home2/pull/918))

### :material-hand-okay: Human-Robot Interaction support

- **`GoToHand` action for HRIC handover** — vision publishes a `PointStamped` for the user's hand; `pick_server` exposes `go_to_hand_action_server` and brings the EE within `hand_offset` (default 10 cm) of the point along the approach axis. ([#724](https://github.com/RoBorregos/home2/pull/724))
- **HRIC integration touching the manipulation side** — motion planning server, `MoveItPlanner`, `pick_server`, and `hric.launch.py` updates. ([#778](https://github.com/RoBorregos/home2/pull/778), [#680](https://github.com/RoBorregos/home2/pull/680))
- **Hand-detection debug fixes**. ([#879](https://github.com/RoBorregos/home2/pull/879))
- **Named configurations for carry** — `FRONT_STARE_CARRY_BAG` ([#866](https://github.com/RoBorregos/home2/pull/866)) and `NAV_CARRY_BAG_POSE` ([#864](https://github.com/RoBorregos/home2/pull/864)) joint configurations.

### :material-cube-outline: 3D perception

The 3D-perception nodes in main (`perception_3d/`) were tuned during the cycle (RANSAC distance threshold 0.03 m, Euclidean cluster tolerance 0.04 m, voxel leaves 0.01/0.10 m). Larger restructuring of the perception stack (transparent-object handling, ClearGrasp/ASGrasp research, etc.) was discussed in the spotlights but not merged to `main` during the documented cycle.

### :material-robot-industrial: Simulation

- **MuJoCo integration** — `mujoco_ros2_control` plugin pinned, base-link mesh decimated, camera and joint actuators wired, `mujoco_spawn` package introduced. ([#739](https://github.com/RoBorregos/home2/pull/739))
- **Simulation scene** — load house, decompose its collision geometry, replace fixtures with an object pool. ([#922](https://github.com/RoBorregos/home2/pull/922))
- **`mujoco_spawn` cleanup** — drop vision nodes from the sim launch so the pick stack runs against a clean perception input. ([#923](https://github.com/RoBorregos/home2/pull/923))
- **Simulation container** — dedicated MuJoCo image and entrypoints. ([#928](https://github.com/RoBorregos/home2/pull/928))
- **Simulation fixes** + **regression hotfix** — final stabilisation passes. ([#966](https://github.com/RoBorregos/home2/pull/966), [#973](https://github.com/RoBorregos/home2/pull/973))

### :material-book-open-page-variant: Documentation & infrastructure

- **Build alias updated** to keep `colcon build` working as the workspace grew. ([#795](https://github.com/RoBorregos/home2/pull/795))
- **Manipulation development docs** (this site) — the [overview](../../../development/manipulation/overview.md), [setup](../../../development/manipulation/setup.md), [architecture](../../../development/manipulation/architecture.md), [packages](../../../development/manipulation/packages.md), [tasks](../../../development/manipulation/tasks.md), and [interfaces](../../../development/manipulation/interfaces.md) pages were authored this cycle (this repo, not `home2`).

## Tasks covered

| Competition task | Launch | Manipulation features used |
|---|---|---|
| **PPC** (Pick & Place Challenge) | `manipulation_general/launch/ppc.launch.py` | Full pick+place stack, no extras |
| **GPSR** | `gpsr.launch.py` | Full pick+place stack + `follow_face_node` |
| **Restaurant** | `restaurant.launch.py` | Pick+place + face follow + cutlery support |
| **HRIC** | `hric.launch.py` | `GoToHand`, move-to-point, face follow |
| **Carry My Luggage** | `carry.launch.py` | MoveIt + motion planning + nav-friendly downsampler. The Carry TM brings up pick/place nodes separately when needed. |
| **Receptionist** | `receptionist.launch.py` | MoveIt + motion planning + face follow. **No pick stack.** |
| **Storing Groceries / Dishwasher** | (per-task TMs) | Shelf scanning + dishwasher placement |
| **Trash throwing** | (subtask) | Place-on-top + heatmap centroid mode |

## Contributions on `main`

The table below reflects only the work **merged into `main` of `home2`** during the 2026 cycle (Jan–May 2026). Each entry links to the originating PR.

| Member | Merged contributions |
|---|---|
| **José Luis Domínguez Morales** | [#696 Place bag](https://github.com/RoBorregos/home2/pull/696) · [#729 Pin `xarm_ros2` to `roborregos_custom`](https://github.com/RoBorregos/home2/pull/729) · [#795 Update build command](https://github.com/RoBorregos/home2/pull/795) · [#797 Pick cutlery](https://github.com/RoBorregos/home2/pull/797) · [#828 Pour refactor](https://github.com/RoBorregos/home2/pull/828) · [#832 Improve pick](https://github.com/RoBorregos/home2/pull/832) · [#833 Update `EEF_CONTACT_LINKS`](https://github.com/RoBorregos/home2/pull/833) · [#850 Rename `ir_gripper` → `grasp_detector` (TGPIO grasp feedback)](https://github.com/RoBorregos/home2/pull/850) · [#851 Pick & Place Challenge](https://github.com/RoBorregos/home2/pull/851) · [#856 IKFast analytical IK plugin for xArm 6](https://github.com/RoBorregos/home2/pull/856) · [#864 `NAV_CARRY_BAG_POSE`](https://github.com/RoBorregos/home2/pull/864) · [#866 `FRONT_STARE_CARRY_BAG`](https://github.com/RoBorregos/home2/pull/866) · [#918 PPC TMR 2026](https://github.com/RoBorregos/home2/pull/918) · [#922 Sim scene: load house + object pool](https://github.com/RoBorregos/home2/pull/922) · [#923 `mujoco_spawn`: drop vision nodes](https://github.com/RoBorregos/home2/pull/923) · [#928 Simulation container](https://github.com/RoBorregos/home2/pull/928) · [#966 Simulation fixes](https://github.com/RoBorregos/home2/pull/966) · [#973 Restore real-robot pick after MuJoCo regression](https://github.com/RoBorregos/home2/pull/973) |
| **Fernando Hernandez Cantu** | [#659 Distance mask on `PickParams`](https://github.com/RoBorregos/home2/pull/659) · [#724 `GoToHand` action for HRIC handover](https://github.com/RoBorregos/home2/pull/724) · [#879 Hand-detection debug fixes](https://github.com/RoBorregos/home2/pull/879) · [#974 Remove pick plane (padding scale)](https://github.com/RoBorregos/home2/pull/974) |
| **Efrain Vázquez** | [#739 MuJoCo simulation: `mujoco_ros2_control` integration, `mujoco_spawn`, base-link decimation, camera + actuators](https://github.com/RoBorregos/home2/pull/739) |
| **Oscar Arreola** | [#778 HRIC March 17: motion planning, `MoveItPlanner`, `pick_server`, and `hric.launch.py` updates](https://github.com/RoBorregos/home2/pull/778) |
| **Gilberto Malagamba Montejo** | [#680 Preliminary HRI Challenge (touches `hric.launch.py`)](https://github.com/RoBorregos/home2/pull/680) · [#810 HRIC testing — updates to `xarm_configurations.py`](https://github.com/RoBorregos/home2/pull/810) |
| **Angela Camila Tite Haro** | [#880 Restaurant launch entry + radial sampling adaptive goal](https://github.com/RoBorregos/home2/pull/880) |

!!! info "How this table was compiled"
    From the output of:

    ```bash
    git log --since="2026-01-01" --pretty=format:"%h %an %s" -- \
        manipulation/ \
        frida_interfaces/manipulation/ \
        frida_constants/frida_constants/manipulation_constants.py \
        frida_constants/frida_constants/xarm_configurations.py
    ```

    Only commits that land manipulation-side code in `main` are listed. Documentation work, research, paper writing, and in-progress branches are intentionally **not** included — they live in the [Spotlights](../../../development/manipulation/spotlights.md) log instead.

## Work explored but not in `main`

The following appeared in the spotlights as in-progress or "Done" entries but **did not land in `main`** during the documented cycle:

- **VAMP integration** (`vamp` / `foam` / `cricket` packages, planning fallback). Lives on a feature branch.
- **Transparent-object grasping** research (ClearGrasp / ASGrasp / VPG).
- Broader perception refactors and dense-cloud database for the grasp detector.

See [Spotlights](../../../development/manipulation/spotlights.md) for the development log of each.
