---
title: Mechanics 2026
---

Mechanical Design — 2026

The 2026 cycle prioritized development of the omnidirectional base while keeping changes to the upper body minimal. Effort focused on mobility, structural improvements, and peripheral integration rather than a full redesign.

!!! info "Scope of this page"
    This page covers mechanical work completed or in progress through May 2026. Software, electrical, and control system details are documented separately.

Headlines

<div class="grid cards" markdown>

- :material-robot:{ .lg .middle } **DashGo Structure**

    ---

    Minimal changes from 2025. Height increase and two additional support points improved reach versatility. Acrylic cover added for aesthetics. New speaker and display integrated. Support-point wheels replaced with quieter alternatives after RoboCup 2025.

- :material-rotate-360:{ .lg .middle } **Omnidirectional base**

    ---

    Structure finalized. Initial URDF ready for testing. Supports 80 kg payload. Targeting functional state for RoboCup 2026.

- :material-hand-back-right:{ .lg .middle } **Gripper**

    ---

    DC motor actuator in development to replace servo. New PCB designed for size reduction. FSR sensor issues under investigation.

</div>

## Breakdown by area

### :material-robot: DashGo Structure

The robot's upper structure retained its 2025 design with targeted refinements:

• Height increase — Extended vertical reach to access elevated surfaces.

• Additional support points — Two extra support points added, improving stability during manipulation tasks across varied workspace heights.

• Acrylic cover — Introduced for aesthetic purposes (paint finish). However, the material proved fragile, difficult to transport, and hard to bend precisely—mirroring the same issues previously encountered with aluminum.

• Peripheral mounting — Speaker and display housings integrated into the body.

• Quieter wheels — Support-point casters replaced with low-noise alternatives, addressing feedback from RoboCup 2025.

Limitations

• Floor-level manipulation — The robot still cannot reach the floor plane for ground-level tasks. This remains a significant constraint for certain manipulation scenarios.

### :material-rotate-360: Omnidirectional base

Development of the omni base reached structural completion by late May 2026:

• Structure finalized — Rigid frame assembled and validated.

• Load capacity — Tested and confirmed to support 80 kg.

• Initial URDF — Created for simulation and control testing.

Pending improvements

• Portability — The structure is less portable than originally intended; redesign needed for easier transport and assembly.

• PLA gears — Current gears break under load. Replacement with Ultracur3D® RG 1100 resin parts is in progress.

• Gearbox mounting — Gearboxes need easier replacement mechanisms and improved support points to reduce maintenance time.

### :material-hand-back-right: Gripper

Active development is underway to improve grasp reliability:

• DC motor actuator — Replacing the current servo motor with a DC motor to provide consistent gripping force, particularly for slippery objects or suboptimal grasp positions.

• New PCB — A redesigned PCB has been developed to reduce overall gripper size. Integration is in progress.

• FSR sensors — Force-sensitive resistors are implemented but produce false negatives. Planned fixes include mechanical adjustments or switching to larger FSR units. Maintaining compact gripper dimensions remains a priority for manipulation tasks.

Pending improvements

• Complete DC motor integration and validate force control.

• Finalize PCB swap and verify size reduction.

• Resolve FSR false-negative issues without increasing gripper footprint.

## Summary of pending work

| Area | Pending improvements |
|---|---|
| DashGo Structure | Enable floor-level manipulation reach; evaluate alternative cover materials (replace acrylic) |
| Omni base | Improve portability; replace PLA gears with Ultracur3D® RG 1100; redesign gearbox mounts for easier maintenance |
| Gripper | Complete DC motor swap; integrate new PCB; fix FSR false negatives without increasing gripper size |

See [Spotlights](../../../development/mechanics/spotlights.md) for the development log of each.
