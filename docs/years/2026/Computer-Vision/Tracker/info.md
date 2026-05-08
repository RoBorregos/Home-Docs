# Tracker Node — Person Tracking with DeepSORT + ReID

**Contributors:** Hector Tovar, Juan Pablo Gutierrez
**Source file:** `vision/packages/vision_general/scripts/tracker_node.py`
**Base algorithm:** [Deep SORT](https://github.com/nwojke/deep_sort) — Simple Online and Realtime Tracking with a Deep Association Metric

---

## Overview

`tracker_node.py` is a ROS2 node that tracks a **single target person** across frames using a combination of:

1. **YOLOv8n** — person detection (class 0)
2. **DeepSORT** — multi-person tracking with persistent IDs via Kalman filtering + cosine-distance association
3. **ReID model (Swin Transformer)** — appearance-based re-identification when the tracked person's ID is lost

The node publishes the tracked person's **3D world coordinates** and a **normalized 2D centroid** for downstream use (e.g., robot navigation/following).

---

## Architecture

```
Camera (RGB + Depth)
        │
        ▼
   YOLOv8n (TRT)          ← detects all people (class 0)
        │
        ▼
   DeepSORT Tracker        ← assigns consistent track IDs across frames
   (Kalman + cosine dist)
        │
        ▼
   ReID Feature Extractor  ← Swin Transformer, FP16 on Orin AGX
   (per-person embeddings)
        │
        ├─ [Track ID matches] → publish 3D point + centroid
        │
        └─ [Track ID lost]   → Re-ID: compare new detections against
                                stored embeddings (angle-aware)
```

---

## How It Works

### 1. Target Selection (`set_target`)

When a tracking service is called, the node runs YOLO + DeepSORT for `N_INIT + 1` frames to let tracks confirm, then selects a target by one of four modes:

| Mode | Service | Description |
|---|---|---|
| `largest_person` | `set_tracking_target` (SetBool) | Picks the person with the largest bounding box area |
| `gestures` | `set_tracking_target_by` (TrackBy) | Uses `PoseDetection.detectGesture()` (e.g., `waving`) |
| `poses` | `set_tracking_target_by` (TrackBy) | Queries Moondream VLM: standing / sitting / lying down |
| `color` | `set_tracking_target_by` (TrackBy) | Queries Moondream VLM: clothing color match |

Moondream queries are sent as crop-bounded prompts via the `CropQuery` service.

### 2. Tracking Loop (`run`, 10 Hz)

Each tick:
- Runs YOLO + DeepSORT on the latest frame
- Looks for the target's `track_id` among confirmed tracks
- If found: updates coordinates, extracts a new embedding at `REID_EXTRACT_FREQ = 0.3 Hz`, stores angle-specific embeddings (forward/backward/left/right)
- Publishes 3D position and normalized 2D centroid

### 3. Re-Identification

When the target's `track_id` is no longer in any confirmed track:
- Extracts ReID embeddings for **all** currently visible people (batch)
- Determines each person's viewing angle via `PoseDetection.personAngle()`
- If angle is known: compares against the angle-specific stored embedding (`cosine threshold = 0.7`)
- If angle is unknown: compares against the full embedding bank (up to `MAX_EMBEDDINGS = 128`)
- On match: resets `person_data` and assigns the new `track_id` as the target

---

## Utility Modules Used

### `vision_general.utils.deep_sort` (from [nwojke/deep_sort](https://github.com/nwojke/deep_sort))

| Module | Used for |
|---|---|
| `deep_sort.tracker.Tracker` | Multi-target tracker (Kalman filter + Hungarian assignment) |
| `deep_sort.detection.Detection` | Wraps a bounding box + confidence + appearance feature |
| `deep_sort.nn_matching.NearestNeighborDistanceMetric` | Cosine-distance metric for track-to-detection association |
| `deep_sort.kalman_filter` | (internal) State estimation for track positions |
| `deep_sort.linear_assignment` | (internal) Hungarian algorithm for assignment |
| `deep_sort.iou_matching` | (internal) IoU-based gating |
| `deep_sort.track` | (internal) Track state machine (Tentative → Confirmed → Deleted) |

### `vision_general.utils.reid_model`

| Function | Used for |
|---|---|
| `get_structure()` | Returns the ReID model architecture (Swin Transformer by default) |
| `load_network(structure)` | Loads pretrained weights from `models/swin/` |
| `extract_feature_from_img(pil_img, model)` | Extracts a single appearance embedding |
| `extract_feature_from_img_batch(img_list, model)` | Batch embedding extraction (used during re-ID) |
| `compare_images(emb1, emb2, threshold)` | Cosine similarity check between two embeddings |
| `compare_images_batch(emb, bank, threshold)` | Checks if an embedding exists in the stored bank |

The ReID model is a **Swin Transformer** (`ft_net_swin`) trained on Market-1501 (751 person IDs). It runs in **FP16** on NVIDIA Orin AGX (capability ≥ 7.0) and falls back to FP32 elsewhere. The classifier head is removed (`nn.Sequential()`) so the output is the raw 512-dim feature vector.

### `vision_general.utils.calculations`

| Function | Used for |
|---|---|
| `get2DCentroid(bbox, depth_img)` | Gets the 2D centroid pixel of the tracked person |
| `get_depth(depth_img, point2D)` | Reads the depth value at a pixel |
| `deproject_pixel_to_point(camera_info, point2D, depth)` | Back-projects pixel + depth → 3D camera-frame point |

### `vision_general.utils.trt_utils`

| Function | Used for |
|---|---|
| `load_yolo_trt(model_name)` | Loads YOLOv8n with optional TensorRT acceleration (Orin AGX) |

### `pose_detection.PoseDetection`

| Method | Used for |
|---|---|
| `detectGesture(img)` | Returns gesture enum (e.g., waving) |
| `personAngle(img)` | Returns viewing angle: `"forward"`, `"backward"`, `"left"`, `"right"`, or `None` |
| `_get_keypoints(img)` | Raw keypoint extraction |
| `is_waving_from_keypoints(pts, kpc)` | Special-case waving detection for `wavingCustomer` |

---

## ROS2 Interface

### Subscriptions

| Topic (constant) | Type | Purpose |
|---|---|---|
| `CAMERA_TOPIC` | `sensor_msgs/Image` | RGB camera feed |
| `DEPTH_IMAGE_TOPIC` | `sensor_msgs/Image` | Depth image (32FC1) |
| `CAMERA_INFO_TOPIC` | `sensor_msgs/CameraInfo` | Camera intrinsics for deprojection |

### Publishers

| Topic (constant) | Type | Purpose |
|---|---|---|
| `RESULTS_TOPIC` | `geometry_msgs/PointStamped` | 3D world coordinates of tracked person |
| `TRACKER_IMAGE_TOPIC` | `sensor_msgs/Image` | Annotated debug image |
| `CENTROID_TOIC` | `geometry_msgs/Point` | Normalized x-centroid (range −1 to +1) |

### Services (server)

| Topic (constant) | Type | Purpose |
|---|---|---|
| `SET_TARGET_TOPIC` | `std_srvs/SetBool` | Enable/disable tracking (largest person default) |
| `SET_TARGET_BY_TOPIC` | `frida_interfaces/TrackBy` | Enable tracking by gesture, pose, or color |
| `IS_TRACKING_TOPIC` | `std_srvs/Trigger` | Query current tracking status |

### Service Clients

| Topic (constant) | Type | Purpose |
|---|---|---|
| `CROP_QUERY_TOPIC` | `frida_interfaces/CropQuery` | VLM crop query via Moondream node |

---

## Key Configuration Parameters

| Parameter | Value | Description |
|---|---|---|
| `CONF_THRESHOLD` | `0.6` | Minimum YOLO confidence to create a detection |
| `DEEPSORT_MAX_COSINE_DISTANCE` | `0.3` | Max cosine distance for DeepSORT association |
| `DEEPSORT_NN_BUDGET` | `100` | Max stored appearance samples per track |
| `DEEPSORT_MAX_AGE` | `100` | Frames before an unmatched track is deleted |
| `DEEPSORT_N_INIT` | `3` | Frames of consecutive detections to confirm a track |
| `REID_EXTRACT_FREQ` | `0.3` Hz | How often to extract and store new embeddings |
| `MAX_EMBEDDINGS` | `128` | Max unique embeddings stored per target |
| `DEPTH_THRESHOLD` | `100` ns | Timestamp tolerance to sync depth + RGB frames |

---

## Running the Node

```bash
# Terminal 1 — tracker
ros2 run vision_general tracker_node

# Terminal 2 — set target (largest person)
ros2 service call /vision/set_tracking_target std_srvs/srv/SetBool "{data: true}"

# Terminal 2 — set target by gesture
ros2 service call /vision/set_tracking_target_by frida_interfaces/srv/TrackBy \
    "{track_enabled: true, track_by: 'gestures', value: 'waving'}"

# Terminal 2 — set target by clothing color (requires Moondream)
ros2 service call /vision/set_tracking_target_by frida_interfaces/srv/TrackBy \
    "{track_enabled: true, track_by: 'color', value: 'red shirt'}"

# Terminal 3 (optional, required for poses/color) — Moondream VLM
ros2 run vision_general moondream_node

# Terminal 3 (Orin only) — ZED camera
./run.sh zed
```

---

## Notes

- The node uses a `MultiThreadedExecutor` with 4 threads; image subscription and moondream calls run in separate `ReentrantCallbackGroup`s to avoid blocking.
- Depth synchronization uses nanosecond timestamps; if depth and RGB are more than `DEPTH_THRESHOLD` ns apart, the 3D publish is skipped with a warning.
- The frame reference is hardcoded to `"zed_left_camera_optical_frame"`.
- During re-ID, **all visible people** are processed in a single batch inference pass for efficiency.
