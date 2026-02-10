# OpenWakeWord

## Overview

`OpenWakeWordNode` is a ROS 2 node that performs keyword spotting (wake word detection) using models trained with [OpenWakeWord](https://github.com/dscripka/openWakeWord). It supports inference using ONNX or TensorFlow Lite (TFLite) frameworks. The node subscribes to raw audio data, detects wake words in real time, and publishes detection events.

---

## What is OpenWakeWord?

OpenWakeWord is an open-source wake word detection toolkit that enables training custom wake word models (e.g., "frida", "no", "stop", "yes") and running inference efficiently. It supports exporting models to ONNX and TFLite formats for deployment on various platforms.

---

## Use Case

This node is intended to detect wake words during the @Home competition to trigger specific functions

---

## Architecture and Implementation

### ROS Parameters
| Parameter                | Type     | Default Path / Value                                     | Description                                                              |
|--------------------------|----------|----------------------------------------------------------|--------------------------------------------------------------------------|
| `model_path`             | string   | `/workspace/src/hri/packages/speech/assets/oww`          | Directory containing ONNX wake word models (`.onnx` files)               |
| `inference_framework`    | string   | `onnx`                                                   | Framework used for inference (`onnx` or `tflite`)                        |
| `audio_topic`            | string   | `/rawAudioChunk`                                         | Topic where raw audio chunks are received                                |
| `WAKEWORD_TOPIC`         | string   | `/speech/oww`                                            | Topic to publish detected wake words                                     |
| `chunk_size`             | int      | `1280`                                                   | Number of samples processed per inference                                |
| `detection_cooldown`     | float    | `1.0`                                                    | Minimum time (in seconds) between detections to avoid repeated triggers  |
| `SENSITIVITY_THRESHOLD`  | float    | `0.5`                                                    | Confidence threshold required for detection                              |

### Model Init
| Feature                    | Description                                                                 |
|----------------------------|-----------------------------------------------------------------------------|
| Load Wakeword Models       | Loads all `.onnx` models from `model_path`. Logs number of models loaded.  |
| Default Model Fallback     | Loads default wake word model if no directory or models are found.         |
| Feature Extractor Download | Downloads `melspectrogram.onnx` and `embedding_model.onnx` if missing.     |
| Path Setup                 | Copies models to the correct execution path if not already present.        |
| ROS Publisher/Subscriber   | Creates publisher (`WAKEWORD_TOPIC`) and subscriber (`audio_topic`).       |
| Cooldown Timer             | Initializes internal timer to prevent repeated wake word detections.       |

### Audio Inference Flow
| Step                        | Description                                                                                   |
|-----------------------------|-----------------------------------------------------------------------------------------------|
| Receive Audio               | Listens to `AudioData` messages from `audio_topic`.                                           |
| Convert to NumPy            | Converts audio byte stream to `np.int16` NumPy array.                                        |
| Run Inference               | Feeds the audio to OpenWakeWord model for prediction.                                        |
| Monitor Prediction Buffer   | Checks latest confidence score for each keyword.                                             |
| Detection Condition         | If `score > SENSITIVITY_THRESHOLD` and cooldown has passed, a detection is triggered.       |
| Publish Detection           | Sends a `std_msgs/String` message like `{"keyword": "frida", "score": 0.87}`.                |

---

## Parameters

| Parameter             | Type    | Default                                           | Description                                                    |
|-----------------------|---------|--------------------------------------------------|----------------------------------------------------------------|
| `model_path`          | string  | `/workspace/src/hri/packages/speech/assets/oww` | Directory containing wake word `.onnx` model files             |
| `inference_framework` | string  | `onnx`                                           | Framework used for model inference (`onnx` or `tflite`)         |
| `audio_topic`         | string  | `/rawAudioChunk`                                 | ROS topic subscribing to raw microphone audio data              |
| `WAKEWORD_TOPIC`      | string  | `/speech/oww`                                   | ROS topic publishing detected wake word messages                |
| `chunk_size`          | int     | `1280`                                          | Size of audio chunks processed per prediction                   |
| `detection_cooldown`  | float   | `1.0`                                           | Minimum seconds between repeated detections                     |
| `SENSITIVITY_THRESHOLD`| float  | `0.5`                                           | Confidence score threshold to confirm wake word detection       |

---

## Message Types

- **Input:** `frida_interfaces/msg/AudioData` — raw audio buffer (16-bit PCM)
- **Output:** `std_msgs/msg/String` — JSON string with detected keyword and confidence score, e.g. `{"keyword": "frida", "score": 0.87}`

