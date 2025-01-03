# Weekly Spotlights

This page is a collection of weekly spotlights that highlight the progress of the integration team. Each spotlight is a summary of the work done by the team in a week.

Member status:

- 🔍: Research
- 💻: Development
- 📝: Documentation
- 🔄: Refactoring
- 🔧: Bug fixing
- 🤝: Participation in other subteam

## 2024-1-3

| Name      | Stauts |
| --------- | ------ |
| Diego     |        |
| Oscar     | 💻 📝  |
| Ale       |        |
| Gilberto  |        |
| Fregoso   |        |
| Ivan      |        |
| Domínguez |        |

**Development**:

- Integrated pre-commit to home2 repository & github action.
- Implemented python linter and formatter (ruff) to home2.
- Base docker images with ROS2 for cuda and cpu.
- Added task manager and frida_interfaces package.
- Added workflow to check ROS2 build.
- Added vision subtask_manager. 

**Documentation**:

- Added README.md for docker naming conventions.
- Added README.md for setting up the project with pre-commit & ruff.

## 2024-12-27

(Holiday break)

| Name      | Stauts |
| --------- | ------ |
| Diego     |        |
| Oscar     |        |
| Ale       |        |
| Gilberto  |        |
| Fregoso   |        |
| Ivan      |        |
| Domínguez |        |

## 2024-12-20

| Name      | Stauts |
| --------- | ------ |
| Diego     |        |
| Oscar     |        |
| Ale       |        |
| Gilberto  | 🔄 🤝  |
| Fregoso   |        |
| Ivan      |        |
| Domínguez |        |

**Development**:

- Setup Orin AGX (Muñoz) for remote access, to make general tests.
- Refactored Speech To Text node from ROS to gRPC integrating faster-whisper in the process.

Planning of new tasks:

- Autogenerated docs for API.
- Linters, precommit, conventional commits.
- Script to check if needed topics, services, and action servers are available.
- Implement network tests (https://docs.ros.org/en/humble/Tutorials/Advanced/ROS2-Tracing-Trace-and-Analyze.html).
- Consider using docker compose for an easier initialization of gRPC client/servers.

## 2024-12-13

| Name      | Stauts |
| --------- | ------ |
| Diego     | 📝     |
| Oscar     | 📝     |
| Ale       | 📝     |
| Gilberto  | 📝     |
| Fregoso   | 📝 🔍  |
| Ivan      | 📝     |
| Domínguez | 🔍     |

**Documentation**:

- Analyzed 7 tasks, considering the main states, transitions, and the specific actions that need to be available for each of the tasks.
- Summarized the [tasks per area](./Task%20Breakdown/AreaTasks.md).

**Research**:

- ROS 2: Research about good practices in ros 2.
- ROS 2: Designed package structure.
- ROS 2: ROSBridge testing.
