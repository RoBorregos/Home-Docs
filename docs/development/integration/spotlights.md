# Weekly Spotlights

This page is a collection of weekly spotlights that highlight the progress of the integration team. Each spotlight is a summary of the work done by the team in a week.

Member status:

- 🔍: Research
- 💻: Development
- 📝: Documentation
- 🔄: Refactoring
- 🔧: Bug fixing
- 🤝: Participation in other subteam

## 2026-03-10

| Name      | Status |
| --------- | ------ |
| Gilberto  |        |
| Fregoso   | 💻     |
| Domínguez |        |
| Camila    |        |
| Danaé     |        |
| Fernando  |        |
| Benvenuto | 💻     |

**Development**

- Upload images to dockerhub manually run.sh and with github actions.

## 2026-03-03

| Name      | Status |
| --------- | ------ |
| Gilberto  | 💻     |
| Fregoso   |        |
| Domínguez |        |
| Camila    |        |
| Danaé     |        |
| Fernando  |        |
| Benvenuto |        |

**Development**

- Testing of HRIC and integration improvements.
- Fixed follow face node error.

## 2026-02-24

| Name      | Status |
| --------- | ------ |
| Gilberto  | 💻     |
| Fregoso   | 🔧     |
| Domínguez |        |
| Camila    |        |
| Danaé     |        |
| Fernando  |        |
| Benvenuto |        |

**Development**

- Started work on new HRI Challenge task manager.

**Bug fixing**

- Replaced speaker temporarily which stopped working.

## 2026-01-22

| Name      | Status |
| --------- | ------ |
| Gilberto  | 🔄     |
| Fregoso   | 📝     |
| Domínguez | 🤝     |
| Camila    | 🔍     |
| Danaé     | 🤝     |
| Fernando  | 🤝     |
| Benvenuto | 🔍     |

**Refactoring**

- Updating docker images on dockerhub

**Documenting**

- Updating HOME2 Readme

**Research**

- Sound and Visual UI with HRI x Integration

## 2026-01-15

| Name      | Status |
| --------- | ------ |
| Gilberto  | 🔄     |
| Fregoso   |        |
| Domínguez |        |
| Camila    |        |
| Danaé     |        |
| Fernando  |        |
| Benvenuto |        |

**Refactoring**

- Change `run.sh` container running logic to avoid entrypoint commands from rerunning on the background.

## 2025-11-14

| Name      | Status |
| --------- | ------ |
| Gilberto  | 🔄📝   |
| Fregoso   |        |
| Domínguez |        |
| Camila    |        |
| Danaé     |        |
| Fernando  |        |
| Benvenuto |        |

**Refactoring**

- Build images with local user ID to avoid permission errors with all volumes

**Documentation**

- Added docker documentation. Will fix root readme next week explaining new run.sh

## 2025-11-07

| Name      | Status |
| --------- | ------ |
| Gilberto  | 🔄     |
| Fregoso   | 🔄     |
| Domínguez |        |
| Camila    |        |
| Danaé     |        |
| Fernando  |        |
| Benvenuto |        |

**Refactoring**

- Standarized run.sh and docker architecture of every area.

## 2025-7-5

- mock nav
- frida_interfaces cache
- clean the table task manager
- storing and receptionists tests
- Active topics/status checks

## 2025-4-10

**Development**:

- Subtask managers update
- Storing groceries task manager
- GPSR task manager
- Receptionist task manager improvements
- Carry my luggage task manager improvements
- VCN

## 2025-4-10

**Development**:

- Subtask manager update for carry my luggage (vision)
- Network tests

## 2025-3-20

| Name      | Status |
| --------- | ------ |
| Diego     | 💻     |
| Oscar     |        |
| Ale       | 💻     |
| Gilberto  |        |
| Fregoso   | 💻     |
| Ivan      | 💻     |
| Domínguez |        |
| David     | 💻     |
| Emiliano  |        |

**Development**:

- First complete Reception
- Network tests:
  - Test better router -> no major improvements
  - Small test on qos subscriber -> better results
  - pending: testing dds discovery server
- Docker images fixed for permissions and added user to video group, enabled gpu.
- Carry My luggage: On going, defined logic.
- Pushing docker images to dockerhub.
- Starting orchestration efforts.

## 2025-3-6

| Name      | Status |
| --------- | ------ |
| Diego     |        |
| Oscar     | 💻     |
| Ale       | 💻     |
| Gilberto  | 💻     |
| Fregoso   | 💻     |
| Ivan      |        |
| Domínguez |        |
| David     |        |

**Development**:

- Update a receptionist:
  - added person description
  - ⁠added beverage location
  - ⁠fixed action services issue
- GPSR: Break down commands for possible command_interpreter
- Integrated nav docker
- TODO -> actual problems: ros user not added on video group on dockers
- Small updates to demo follow face node

## 2025-2-27

| Name      | Status |
| --------- | ------ |
| Diego     |        |
| Oscar     | 💻🔧   |
| Ale       | 💻     |
| Gilberto  |        |
| Fregoso   | 💻     |
| Ivan      | 💻     |
| Domínguez | 💻     |
| David     | 💻     |

# **Development**:

- Vision's subtask manager: Updated needs and methods for the _Receptionist_ task manager.
- GPSR: Clarified and added visions needs for subtask manager.
- TODO -> Reaserch and investigate why are the HRI services faulty on jetsons containers.
- Manipulation's subtask manager: Added subtask manager and implemented setJointPosition method.
- Follow Face node: change functionality for it to be available as a service.
- Set up Zed2 camera on orin.

## 2025-2-20

| Name      | Status |
| --------- | ------ |
| Diego     |        |
| Oscar     |        |
| Ale       |        |
| Gilberto  |        |
| Fregoso   |        |
| Ivan      |        |
| Domínguez |        |

**Development**:

- Receptionist task manager

## 2025-1-29

| Name      | Status |
| --------- | ------ |
| Diego     |        |
| Oscar     | 💻     |
| Ale       |        |
| Gilberto  |        |
| Fregoso   |        |
| Ivan      |        |
| Domínguez |        |

**Development**:

- Sub task manager for HRI (Command interpreter service, Grammar node, hear, find_closest). Todo: ask function (retrieve from vector store), interpret_keyword (high-level api)
- Update vision subtask manager to support follow face

## 2025-1-29

| Name      | Status |
| --------- | ------ |
| Diego     |        |
| Oscar     |        |
| Ale       |        |
| Gilberto  |        |
| Fregoso   |        |
| Ivan      |        |
| Domínguez |        |

## 2025-1-22

| Name      | Status |
| --------- | ------ |
| Diego     |        |
| Oscar     | 💻     |
| Ale       | 💻     |
| Gilberto  |        |
| Fregoso   |        |
| Ivan      |        |
| Domínguez |        |

**Development**:

- Package for constant management (python support)
- Implementation of mock config for subtask managers
- Implementation of topic checks for subtask managers

## 2025-1-15

| Name      | Status |
| --------- | ------ |
| Diego     |        |
| Oscar     |        |
| Ale       |        |
| Gilberto  |        |
| Fregoso   |        |
| Ivan      |        |
| Domínguez |        |

**Research**:

- Feasibility / how to integrate behavior trees with ROS2 for the task managers.
- Schedule meeting to propose new features for task managers and sub task managers.

## 2025-1-10

| Name      | Status |
| --------- | ------ |
| Diego     |        |
| Oscar     |        |
| Ale       |        |
| Gilberto  |        |
| Fregoso   |        |
| Ivan      |        |
| Domínguez |        |

## 2025-1-3

| Name      | Status |
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

| Name      | Status |
| --------- | ------ |
| Diego     |        |
| Oscar     |        |
| Ale       |        |
| Gilberto  |        |
| Fregoso   |        |
| Ivan      |        |
| Domínguez |        |

## 2024-12-20

| Name      | Status |
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

| Name      | Status |
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
