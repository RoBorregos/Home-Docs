---
title: "Proto Interfaces"
---

# Proto Interfaces Package

!!! info "Synced from home2"
    Generated from [`home2/hri/proto_interfaces/README.md`](https://github.com/RoBorregos/home2/blob/7288a442c4a6b3b487947e5f57e107c504856b23/hri/proto_interfaces/README.md) @ `7288a44` by `scripts/sync_home2_readmes.py`. Edit the README in home2 instead of this page.

This package contains Protocol Buffer definitions and gRPC service interfaces for the HRI microservices.

## Contents

- **speech_pb2.py / speech_pb2_grpc.py**: Speech-to-Text service definitions
- **tts_pb2.py / tts_pb2_grpc.py**: Text-to-Speech service definitions

## Usage

### ROS2 Nodes

```python
from proto_interfaces import speech_pb2_grpc, speech_pb2

# Create gRPC channel and stub
channel = grpc.insecure_channel("localhost:50051")
stub = speech_pb2_grpc.SpeechStreamStub(channel)
```

### Microservices

```python
from proto_interfaces import speech_pb2_grpc, speech_pb2

class WhisperServicer(speech_pb2_grpc.SpeechStreamServicer):
    def Transcribe(self, request_iterator, context):
        # Implementation
        pass
```

## Regenerating Proto Files

Run `run.sh hri --build-proto` to automatically generate the python scripts.
