# Zero-Shot Object Detector

[YOLOE](https://docs.ultralytics.com/models/yoloe/) (Real-Time Seeing Anything) is a new advancement in zero-shot, promptable YOLO models, designed for open-vocabulary detection and segmentation. Unlike previous YOLO models limited to fixed categories, YOLOE uses text, image, or internal vocabulary prompts, enabling real-time detection of any object class. 

This document describes the functionality, parameters, and usage of the `zero_shot_object_detector_node`, a ROS 2 node designed to detect objects using a YOLO-based zero-shot detector.

## Overview

The `zero_shot_object_detector_node` performs real-time 2D object detection from RGB and depth images, using a YOLO-based model. It also supports:

- Output of detection poses and 3D visualizations
- Publishing detection images
- Dynamic class configuration via a ROS service
- Use of ZED transform for spatial alignment

## Node Name

```yaml
zero_shot_object_detector_2D_node
```

## Subscribed Topics

- `CAMERA_TOPIC` (sensor\_msgs/Image): RGB camera stream
- `DEPTH_IMAGE_TOPIC` (sensor\_msgs/Image): Depth image
- `CAMERA_INFO_TOPIC` (sensor\_msgs/CameraInfo): Intrinsics

## Published Topics

- `ZERO_SHOT_DETECTIONS_TOPIC` (frida\_interfaces/ObjectDetectionArray): 2D object detections
- `ZERO_SHOT_DETECTIONS_POSES_TOPIC` (geometry\_msgs/PoseArray): Detected object poses
- `ZERO_SHOT_DETECTIONS_3D_TOPIC` (visualization\_msgs/MarkerArray): RViz-compatible markers
- `ZERO_SHOT_DETECTIONS_IMAGE_TOPIC` (sensor\_msgs/Image): Debug image with bounding boxes

## Services

- `SET_DETECTOR_CLASSES_SERVICE`
  - **Request:**
    ```yaml
    string[] classes
    ```
  - **Response:**
    ```yaml
    bool success
    ```

## Parameters

These are defined in the `ARGS` dictionary and loaded using ROS 2 `declare_parameter()`:

| Parameter Name      | Type       | Default Value                  | Description                          |
| ------------------- | ---------- | ------------------------------ | ------------------------------------ |
| `YOLO_MODEL_PATH`   | `string`   | `yoloe-11l-seg.pt`             | YOLOv5/YOLOe model to load           |
| `CLASSES`           | `string[]` | List of default object classes | Object categories to detect          |
| `USE_ACTIVE_FLAG`   | `bool`     | `False`                        | Enables active detection gating      |
| `DEPTH_ACTIVE`      | `bool`     | `True`                         | Use depth image for 3D info          |
| `MIN_SCORE_THRESH`  | `float`    | `0.25`                         | Minimum confidence score             |
| `USE_ZED_TRANSFORM` | `bool`     | `True`                         | Enables ZED-specific frame alignment |
| `FLIP_IMAGE`        | `bool`     | `False`                        | Flip input image if required         |
| `VERBOSE`           | `bool`     | `False`                        | Enables debug logs                   |

## Default Classes

```python
ZERO_SHOT_DEFAULT_CLASSES = [
    "bowl", "whiteBaseball", "apple", "cup", "plate",
    "yellow_mustard_container", "blue_tuna_can", "soup_can",
    "neon_ball", "squash", "banana", "soap", "rubikCube",
    "coke_bottle", "yellow_bowl", "fanta_can", "orange"
]
```

## Example Detection Output

```text
Detected: 'apple' at (x=0.45, y=0.63), confidence=0.81
Detected: 'rubikCube' at (x=0.27, y=0.42), confidence=0.74
```

## Message Example: SetDetectorClasses

**Request**

```yaml
string[] classes:
  - "apple"
  - "cup"
  - "banana"
```

**Response**

```yaml
bool success: true
```

## Visualization

The 2D detections and 3D markers can be visualized in RViz:



## Launching the Node

Run the node as a standalone executable:

```bash
ros2 run your_package zero_shot_object_detector_node
```

Make sure your topic remappings and camera inputs are correct.

## Extending the Detector

This node is built atop the `object_detector_node` class and leverages `YoloEObjectDetector`. You can:

- Replace the detection backend
- Update the class list dynamically
- Customize frame transforms and camera parameters


