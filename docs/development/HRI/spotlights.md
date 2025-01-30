# Weekly Spotlights

This page is a collection of weekly spotlights that highlight the progress of the integration team. Each spotlight is a summary of the work done by the team in a week.

Member status:

- 🔍: Research
- 💻: Development
- 📝: Documentation
- 🔄: Refactoring
- 🔧: Bug fixing
- 🤝: Participation in other subteam

## 2025-1-27

| Name     | Stauts |
| -------- | ------ |
| Diego    |        |
| Gilberto |        |
| Ivan     |        |
| Jocelyn  |        |
| Leo L.   |        |
| Oscar    |        |

## 2025-1-22

| Name     | Stauts |
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

| Name     | Stauts |
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

| Name     | Stauts |
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

| Name     | Stauts      |
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

| Name     | Stauts |
| -------- | ------ |
| Diego    |        |
| Gilberto |        |
| Ivan     |        |
| Jocelyn  |        |
| Leo L.   |        |
| Oscar    |        |

## 2024-12-20

| Name     | Stauts |
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

| Name     | Stauts |
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
