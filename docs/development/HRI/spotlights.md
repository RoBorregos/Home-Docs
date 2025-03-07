# Weekly Spotlights

This page is a collection of weekly spotlights that highlight the progress of the integration team. Each spotlight is a summary of the work done by the team in a week.

Member status:

- 🔍: Research
- 💻: Development
- 📝: Documentation
- 🔄: Refactoring
- 🔧: Bug fixing
- 🤝: Participation in other subteam

## 2025-3-06

| Name     | Status |
| -------- | ------ |
| Diego    | 💻     |
| Gilberto | 💻     |
| Ivan     |        |
| Jocelyn  | 💻     |
| Leo L.   | 💻     |
| Oscar    | 💻     |

**Development**:

- Integrated keyword detection with timeout in subtask manager
- Added common interests service
- Fine tuned a new model using a base model distilled from Deepseek-R1. Has better accuracy but is heavy.
- Tested a model finetuned using GRPO to verify structured output support.
- Added compose files to run ollama on jetson and other computers
- Created 3 knowledge bases: frida, roborregos, tec de monterrey to answer questions. Manually divided the content to keep semantic meaning
- Created RAG to generate answers using context + llm response
- Scoring to identify between quizz questions (when embedding score is less than 0.4) from direct context questions for the gpsr
- Finished dockerfile for running faster-whisper microservice on l4t with cuda
- Added chroma adapter to recycle methods

## 2025-2-27

| Name     | Status |
| -------- | ------ |
| Diego    |        |
| Gilberto |        |
| Ivan     |        |
| Jocelyn  |        |
| Leo L.   | 💻     |
| Oscar    | 💻     |

**Development**:

- Added the AddItem service into the task manager + the feature to add/query by metadata
- Added scripts for setting the default sink and source in the pulseaudio server (`setup.bash`).

## 2025-2-20

| Name     | Status |
| -------- | ------ |
| Diego    |        |
| Gilberto |        |
| Ivan     |        |
| Jocelyn  |        |
| Leo L.   |        |
| Oscar    |        |

**Planning**:

- Backlog created in Github projects.

## 2025-2-13

| Name     | Status   |
| -------- | -------- |
| Diego    |          |
| Gilberto |          |
| Ivan     |          |
| Jocelyn  | 🔧       |
| Leo L.   |          |
| Oscar    | 🔧 📝 💻 |

**Bug fixing**:

- OpenWakeWord in jetson orin (runtime)
- OpenWakeWord installation

**Development**:

- Docker image for jetson Orin
- Docker compose for jetson orin

**Documentation**:

- Added instructions for pulseaudio setup sink and source setup in the README.
- Running HRI area for the demo.

## 2025-2-05

| Name     | Status   |
| -------- | -------- |
| Diego    |          |
| Gilberto |          |
| Ivan     |          |
| Jocelyn  |          |
| Leo L.   | 💻       |
| Oscar    | 🔧 🔄 📝 |

**Development**:

- Add the embeddings to the DB only when needed (skip if cached).
- Added params to node to control the embeddings to be added to the DB.
- Integration of embeddings to subtask manager.

**Refactoring**:

- Launchfiles for hri.
- Added needed containers to general, hri docker-compose.

**Documentation**:

- Updated HRI README for new docker-compose structure.

## 2025-1-27

| Name     | Status |
| -------- | ------ |
| Diego    |        |
| Gilberto |        |
| Ivan     |        |
| Jocelyn  |        |
| Leo L.   | 💻     |
| Oscar    |        |

**Development**

-ChromaDB for embeddings query set up and working.

## 2025-1-22

| Name     | Status |
| -------- | ------ |
| Diego    |        |
| Gilberto | 🔄     |
| Ivan     |        |
| Jocelyn  |        |
| Leo L.   | 💻     |
| Oscar    |        |

**Development**

-Migrating the item_categorization service to ChromaDB (vector database) for better performance and scalabilty.

**Refactoring**

- Moved Speech To Text service to hear node and integrated callback groups for async calling.

## 2025-1-15

| Name     | Status |
| -------- | ------ |
| Diego    |        |
| Gilberto | 🔄     |
| Ivan     | 🔄     |
| Jocelyn  | 💻     |
| Leo L.   |        |
| Oscar    |        |

**Development**:

- Installed the nvidia container runtime on the Jetson Orin AGX through the SDK manager and tested the ollama container with the fine-tuned model using structured output, which worked.
- Created ROS2 node that interacts with OpenWakeWord library for keyword spotting
- Loaded models to hri project directory

**Refactoring**

- Fixed hear and useful_audio ROS2 nodes.
- Integrated with gRPC speech to text docker microservice.
- Added functional speech launch file.
- Migrated extract_data node
- Migrated stop_listener node

## 2025-1-10

| Name     | Status |
| -------- | ------ |
| Diego    |        |
| Gilberto | 🔄     |
| Ivan     |        |
| Jocelyn  |        |
| Leo L.   |        |
| Oscar    | 🔄     |

**Refactoring**:

- `nlp` package setup in ROS 2.
- Migrated `command_interpreter.py` node to ROS 2.
- Migration of several speech nodes to ROS 2: `hear.py`, `kws.py`, `respeaker.py`, `useful_audio.py`.
- Integration of some speech nodes to the speech launchfile.

## 2025-1-03

| Name     | Status      |
| -------- | ----------- |
| Diego    |             |
| Gilberto |             |
| Ivan     |             |
| Jocelyn  | 💻 🔍       |
| Leo L.   |             |
| Oscar    | 💻 🔄 📝 🤝 |

**Development**:

- Automatically download piper TTS models if not locally present (avoid committing heavy files).
- Trained 3 different KWS models: "Frida", "Yes" and "No". Obtained both .onnx and .tflite files.
- Generated 15GB worth of synthetic audio clips to obtain performance metrics.

**Documentation**:

- Instructions on how to build HRI with docker compose.
- HRI Tree structure.

**Refactoring**:

- Cleaned Dockerfiles for CPU and Cuda images for ROS2.
- Moved docker compose for devices to use CPU image.
- Ros2 package setup for speech.
- Migrated speech utility files.
- Migrated `audio_capturer.py` and `say.py` to ROS 2.

**Research**:

- Active in discussion [channel](https://github.com/dscripka/openWakeWord/discussions/227) on GitHub to find out how to obtain metrics for our KWS models.

## 2024-12-27

(Holiday break)

| Name     | Status |
| -------- | ------ |
| Diego    |        |
| Gilberto |        |
| Ivan     |        |
| Jocelyn  |        |
| Leo L.   |        |
| Oscar    |        |

## 2024-12-20

| Name     | Status |
| -------- | ------ |
| Diego    |        |
| Gilberto | 🤝     |
| Ivan     | 💻     |
| Jocelyn  |        |
| Leo L.   | 💻     |
| Oscar    | 💻     |

**Development**:

- Tests using function calling
- Vector embedding database
- Integration of benchmarked embeddings on several use cases using ROS 2.
- Migrated docker cuda container to ROS 2 .

## 2024-12-13

| Name     | Status |
| -------- | ------ |
| Diego    | 💻     |
| Gilberto |        |
| Ivan     |        |
| Jocelyn  |        |
| Leo L.   |        |
| Oscar    | 💻     |

**Development**:

- Integrated local structured output on main (`extract_data`, `command_interpreter_v2`) while maintaining backwards compatibility.
- Tested new Ollama version, which includes a new feature for structured output that supports our fine tuned model.
- The fine tuned model didn't work as expected with the Orin Nano, likely due to a lack of resources, since it worked on a laptop. We will test it on the Xavier AGX.
