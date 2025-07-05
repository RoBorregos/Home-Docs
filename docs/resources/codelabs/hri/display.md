# HRI Display Guide

This guide explains how to build, run, and test the HRI display interface.

### When to use CPU vs. GPU (CUDA)

| Version    | When to use                                                                  |
|------------|------------------------------------------------------------------------------|
| CPU        | When using a machine without an NVIDIA GPU or for general development.       |
| GPU (CUDA) | When using an NVIDIA GPU and running performance-heavy models (e.g. STT, NLP)|


###  Files and Requirements

Make sure the following files exist and are correctly configured:

- `docker/hri/display.yaml`: Docker Compose file for the display service.
- `docker/hri/.env`: Environment variables (can be copied from `.env.example`).
- `docker/hri/setup.bash`: Script to set up the Docker environment.

---
### CPU Setup Instructions

#### 1. Set up the environment

```bash
cd home2/docker/hri
source setup.bash
```

#### 2. Build the CPU base image

```bash
cd home2/docker
docker compose -f cpu.yaml build
```

#### 3. Run HRI containers 

```bash
cd home2/docker/hri
docker compose -f docker-compose-cpu.yml up
```
#### 4. Access the container

```bash
docker exec -it home2-hri-cpu-devices bash
```
---
### GPU Setup Instructions

#### 1. Set up the environment

```bash
cd home2/docker/hri
source setup.bash
```

#### 2. Build the GPU base image

```bash
cd home2/docker
docker compose -f cuda.yaml build
```

#### 3. Run HRI containers 

```bash
cd home2/docker/hri
docker compose up
```
#### 4. Access the container

```bash
docker exec -it home2-hri-cuda-devices bash
```
---
### Running the Display

To start the display container:

```bash
cd home2/docker/hri
docker compose -f display.yaml up
```

This uses the configuration defined in display.yaml, which launches the container home2-hri-display.

---
### Viewing the Display

Open the browser and go to:

```bash
http://localhost:3000
```
This will show the robot display interface.

---
### Testing the System 

From inside the HRI container (CPU or GPU), you can test the system using the following commands.

#### Launch HRI nodes

```bash
ros2 launch speech hri_launch.py
```
#### Speech and NLP Services
```bash
# Say something
ros2 service call /hri/speech/speak frida_interfaces/srv/Speak "{text: \"Go to the kitchen and grab cookies\"}"

# Extract data from a sentence
ros2 service call /hri/nlp/data_extractor frida_interfaces/srv/ExtractInfo "{full_text: 'Hello, my name is Oscar', data: 'name'}"

# Is positive
ros2 service call /hri/nlp/is_positive frida_interfaces/srv/IsPositive "{text: 'I confirm'}"

# Is negative
ros2 service call /hri/nlp/is_negative frida_interfaces/srv/IsNegative "{text: 'Incorrect'}"

# Rag question
ros2 service call /hri/rag/answer_question frida_interfaces/srv/AnswerQuestion "
question: 'What time is it'
topk: 10
threshold: 0.0
knowledge_type: []
"
```
#### Interact with robot's display
```bash
## Simulate hear text
ros2 topic pub /speech/raw_command std_msgs/msg/String '{data: "hello"}' -1

## Simulate the robot saying something
ros2 topic pub /speech/text_spoken std_msgs/msg/String '{data: "My name is Frida"}' -1

## Simulate keyword detection
ros2 topic pub /hri/speech/oww std_msgs/msg/String '{data: "Frida"}' -1

## Simulate voice activity
ros2 topic pub /AudioState std_msgs/msg/String '{data: "listening"}' -1

ros2 topic pub /hri/speech/vad std_msgs/msg/Float32 '{data: 0.8}' -1

## Stop voice simulation
ros2 topic pub /AudioState std_msgs/msg/String '{data: "idle"}' -1
```
#### Troubleshooting
- Use `docker ps` to verify containers are running.

- Use `docker logs home2-hri-display` to check display logs.

- Ensure the `.env `file is properly set up with environment variables.
- Confirm your system meets GPU requirements if using CUDA.