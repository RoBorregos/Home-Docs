# Moondream

[Moondream](https://moondream.ai/) is an open-source visual language model that understands images using simple text prompts.

We integrated Moondream along with YOLOv8 and gRPC to power robot vision capabilities like posture analysis, object detection, and natural language querying.

---

## Contents

- [Architecture](#architecture)
- [Features](#features)
- [ROS Node](#ros-node)
- [gRPC Server](#grpc-server)
- [Protobuf API](#protobuf-api)
- [Project Structure](#project-structure)

---

## Architecture
![image](../../assets/home/Vision/moondream.png)

---

## Features

- Detect person and crop the region with largest area (via YOLOv8)
- Classify person posture (standing, sitting, lying)
- Locate beverages (left, center, right)
- Natural language query over full image or crop
- Serve MoonDream model via gRPC for scalable vision requests

---

## ROS Node

### Node Name: `MoondreamNode`

**Topic Subscribed:**
- `CAMERA_TOPIC` (`sensor_msgs/msg/Image`)

**Services Provided:**

| Service Name              | Description |
|--------------------------|-------------|
| `/beverage_location`     | Locate a beverage (returns LEFT, CENTER, RIGHT, or NOT_FOUND) |
| `/person_posture`        | Detects posture of a person in the frame |
| `/query`                 | Runs a natural language query on the image |
| `/crop_query`            | Describes a cropped region based on bounding box |

### Core Methods

- `image_callback`: Updates internal image on new frame
- `query_callback`: Runs general-purpose query
- `crop_query_callback`: Describes cropped regions
- `beverage_location_callback`: Finds beverage position
- `person_posture_callback`: Uses MoonDream to describe posture
- `detect_and_crop_person`: Extracts largest detected person via YOLOv8

---

## gRPC Server

### Entry Point: `serve()`

**Starts a gRPC server on port 50052**, providing:
- `EncodeImage`
- `FindBeverage`
- `Query`

```python
def serve(**kwargs):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    md_model = MoonDreamModel(**kwargs)
    moondream_proto_pb2_grpc.add_MoonDreamServiceServicer_to_server(
        MoonDreamServicer(md_model), server
    )
    server.add_insecure_port("[::]:50052")
    server.start()
```

**Command-line Arguments:**
- `--model_name`: Model name on Hugging Face
- `--revision`: Revision tag for model version
- `--device_map`: e.g., `"jetson"`, `"cpu"`, `"cuda"`

---

## MoonDreamModel

This is the interface class to the underlying multimodal model (`vikhyatk/moondream2`).

### Methods

```python
encode_image(image_data: bytes) -> bytes
```
Compresses and encodes image to be sent via gRPC.

```python
find_beverage(encoded_image, subject) -> str
```
Returns beverage position: `"left"`, `"center"`, `"right"` or `"not found"`.

```python
query(encoded_image, query: str) -> str
```
Executes natural language query on the visual input.

---

## Protobuf API

Defined in `moondream_proto.proto`

```protobuf
syntax = "proto3";

service MoonDreamService {
  rpc EncodeImage (ImageRequest) returns (EncodedImageResponse);
  rpc FindBeverage (FindBeverageRequest) returns (BeveragePositionResponse);
  rpc Query (QueryRequest) returns (QueryResponse);
}

message ImageRequest {
  bytes image_data = 1;
}

message EncodedImageResponse {
  bytes encoded_image = 1;
}

message FindBeverageRequest {
  bytes encoded_image = 1;
  string subject = 2;
}

message BeveragePositionResponse {
  string position = 1;
}

message QueryRequest {
  bytes encoded_image = 1;
  string query = 2;
}

message QueryResponse {
  string answer = 1;
}
```

---

## Testing Example

Run the gRPC test client:

```bash
python grpc_client_test.py
```

Expected output:

```
Beverage position: left
Description: A purple bottle is on the left shelf.
```

---

## Project Structure
```
moondream_server/
├── client.py             
├── moondream_lib.py         
├── moondream_proto_pb2.py          
├── moondream_proto_pb2_grpc.py     
├── moondream_proto.proto        
└── server.py
scripts/  
├── moondream_node.py         
```
