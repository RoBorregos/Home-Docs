# Weekly Spotlights

This page is a collection of weekly spotlights that highlight the progress of the integration team. Each spotlight is a summary of the work done by the team in a week.

Member status:

- 🔍: Research
- 💻: Development
- 📝: Documentation
- 🔄: Refactoring
- 🔧: Bug fixing
- 🤝: Participation in other subteam

## 2026-03-24

 Name     | Status |
| -------- | ------ |
| Camila   |   💻   |
| Fregoso  |   💻   |
| Alberto  |   💻   |
| Bahena   |   🔍   |
| Rodro    |   💻   |
| Daniel   |   🤝   |
| Dana     |   🔍   |

- **Development**

  - Major navigation refactor: cleaned up old behavior trees, removed unused maps, restructured launch composition, and deleted legacy config files. Added new map area tagger tool (771 lines) and custom Nav UI (777 lines) for map context management.
  - Implemented ROS 2 node resource monitor that tracks CPU, memory, and GPU usage of specified nodes. Added custom `NodeStatus` and `MonitorReport` message definitions to `frida_interfaces`. Includes dedicated launch file and Docker Compose configurations for GPU, L4T, and general navigation environments.
  - Added CycloneDDS as the DDS middleware across all areas including navigation, with setup scripts and Docker integration.
  - Nav2 parameter tuning: MPPI controller tuning, voxel layer improvements, updated inflation permissions, and improved obstacle handling. Updated behavior tree for replanning and recovery. Refactored `rtabnav2.launch.py` and improved `move_to_location.py` with better replanning logic.
  - Nav UI improvements and final parameter tuning for nav2_standard and nav2_following configurations.
  - Created a lifecycle manager node (`nav_lifecycle_manager.py`) for dependency handling between navigation nodes. Converted `map_service` to a lifecycle node managed by the lifecycle manager using timer-based dependency monitoring.
  - Created a controller node for DualShock with deadzone support, adjustable rotation and linear speed features.
  - Updated EKF launch configuration for `dashgo_driver`.

- **Bug fixing**

  - Fixed `ignore_laser.cpp` filter logic.
  - Fixed Python3 environment recognition errors in navigation packages.

## 2026-02-03

 Name     | Status |
| -------- | ------ |
| Camila   |   💻   |
| Bahena   |   🔍   |
| Fregoso  |   💻   |
| Rodro    |   💻   |
| Daniel   |   💻   |
| Alberto  |   💻  |
| Dana     |   🔍   |

- **Research**

  - New members still learning i guess.

- **Development**
   - Finish updating repository
   - Finish rplidar fix and urdf change
   - Started Nav custom UI with QT development
  ![image](../../assets/development/navigation/spotlights/navUI.jpeg)
  
## 2026-01-29

 Name     | Status |
| -------- | ------ |
| Camila   |   💻   |
| Bahena   |   🔍   |
| Fregoso  |   💻   |
| Rodro    |   💻   |
| Daniel   |   💻   |
| Alberto  |   🔍   |
| Dana     |   🔍   |

- **Research**

  - New members are learning about nav2 repo and behaivor trees.

- **Development**

  - Webots first status simulation.
  ![image](../../assets/development/navigation/spotlights/Webotsfirstversion.jpeg)
  - Webots zed2 digital twin.
  - Cleanup repository
  ![image](../../assets/development/navigation/spotlights/RepoUpdate.png)
  - Updating Performance for Nodes migrating to cpp.
  - Tauri app development in progress
  

## 2026-01-22

 Name     | Status |
| -------- | ------ |
| Camila   |   📝   |
| Bahena   |   🔍   |
| Fregoso  |    🔄  |
| Rodro    |   📝   |
| Daniel   |   🤝   |
| Alberto  |   🔍   |
| Dana     |   🔍   |

- **Research**

  - New members are learning about nav2 introduction with Articulated Robotics videos.

- **Refactor**

  - Removing old stuff and updating packages.

 **Documentation**

  - Creating first tauri app documentation.
  - Documenting first takes with webots simulation.
