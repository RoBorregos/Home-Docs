# Weekly Spotlights

This page is a collection of weekly spotlights that highlight the progress of the vision team. Each spotlight is a summary of the work done by the team in a week.

## 2025-11-28

**In Progress:**

| Owners   | Task   |
|-------|---------|
| Daniela | Trash detection |
| Héctor & Brisma | Tracker |
| Danaé | Address comments in TDP |
| Joce | Migrate to Moondream3 | 

## 2025-11-21

**In Progress:**

| Owners   | Task   |
|-------|---------|
| Héctor, Daniela & Brisma | Pose detection, face detection and ReID |
| Danaé | Address comments in TDP |
| Joce | Migrate to Moondream3 | 

## 2025-11-14

**In Progress:**

| Owners   | Task   |
|-------|---------|
| Héctor, Daniela & Brisma | Improve face detection |
| Fernando | Integrating logic into pipeline interface (backend) |
| Danaé, Joce | Working in TDP |
| Danaé | Clean and standarize docker | 

## 2025-11-07

**In Progress:**

| Owners   | Task   |
|-------|---------|
| Héctor & Daniela | Pose detection |
| Brisma  | Research about face detection |
| Fernando | Integrating logic into pipeline interface (backend) |
| Danaé | Working in TDP 

## 2025-10-16

**In Progress:**

| Owners   | Task   |
|-------|---------|
| Fernando & Brisma  |  Testing object/person detection filter by distance |
| Brisma  | Research about face detection |
| Fernando | Improving dataset pipeline |
| Fernando | Integrating logic into pipeline interface (backend) |
| Danaé | Research of new models / VLMs / repositories |

**Done:**

| Owners   | Task   |
|-------|---------|
| Brisma  | Frontend for dataset pipeline interface |


## 2025-10-09

**In progress:**

| Owners              | Task                                                                 |
|---------------------|----------------------------------------------------------------------|
| Brisma |  Proposal of interface for dataset creation |
| Danaé & Fernando 💻 | Clean dataset pipeline and test new models |
| Fernando & Brisma  |  Testing object/person detection filter by distance |


## 2025-10-02

**Done:**

| Owners              | Task                                                                 |
|---------------------|----------------------------------------------------------------------|
| Héctor & Daniela  📄 |  Research about pose detection, reID and tracker |
| Danaé 💻 | Developed YOLO central node |

**In Progress:**

| Owners              | Task                                                                 |
|---------------------|----------------------------------------------------------------------|
| Fernando & Brisma  |  Testing object/person detection filter by distance |
| Danaé  | Testing YOLO node |

**To-do:**

| Owners              | Task                                                                 |
|---------------------|----------------------------------------------------------------------|
| Fernando and Jocelyn 💻  | Improve DINO for more accurate segmentation |

## 2025-09-25

**In Progress:**

| Owners              | Task                                                                 |
|---------------------|----------------------------------------------------------------------|
| Danaé & Brisma 💻   | Centralizing YOLO            |
| Brisma 💻   | Test object detection filtering based on distance             |
| Fernando and Jocelyn 💻  | Improving DINO for more accurate segmentation                    |
| Daniela & Hector 📄 | Research: Alternatives/improvements for tracker, reID and pose detection       |

## 2025-09-18

**In Progress:**

| Owners              | Task                                                                 |
|---------------------|----------------------------------------------------------------------|
| Danaé & Brisma 💻   | Simplifying YOLO usage by creating a single shared instance           |
| Danaé & Brisma 💻   | Implementing object detection filtering based on distance             |
| Fernando 💻         | Improving DINO for more accurate segmentation                        |
| Jocelyn             | Supporting "Candidatos Avanzados" through mentoring                   |
| Jocelyn & Danaé 📄  | Planning the @Home vision research paper                              |



## 2025-06-25

**Done:**

- OnBoarding pt2
- Task definition and prioritization
- Documentation for Moondream and Zero Shot model YOLOe

**In progress:**

- Mask detected people to avoid those who are outside of the arena
- ReId download model and requirements without internet
- ReID modifications:
    - Now extracts multiple embeddings for each person based on similarity with own tracklet over past frames
    - Will integrate batch feature extraction and batch feature comparison for increased speed and allow for more comparisons -> multiple embeddings for each person

**To do:**

- Pipeline segmentation
- Pipeline dataset augmentation
- Pipeline tutorial
- Single camera depth inference


## 2025-06-18

**Done:**

- OnBoarding pt1

**In progress:**

- Documentation
- Mask detected people to avoid those who are outside of the arena
- ReId download model and requirements without internet

**To do:**

- Define and assign new tasks for stage 2 and stage 1 fixes/improvements
- Pipeline segmentation
- Pipeline dataset augmentation

## 2025-04-24

**Done:**

- Fixes for receptionist (find seat)
- Zero-shot + yolo models
- Subtasks for GPSR
- Carry launch

**In progress:**

- Testing subtask functions
- Pipeline

**To do:**

- 

## 2025-04-10

**Done:**

- Moondream general service
- Detector 2d
- Subtask manager update for carry
- GPSR Node

**In progress:**

- New yolo testing
- Shelf detector node

**To do:**

- Test model training pipeline

## 2025-04-03

<div style="display: flex; justify-content: space-between;">
    <!-- Add any images here -->
    <img src="/assets/development/vision/spotlights/moondream.png" alt="image" width="300"/>
    <img src="/assets/development/vision/spotlights/detic.jpeg" alt="image" width="300"/>
    <img src="/assets/development/vision/spotlights/spotlight_2025_04_03.gif" alt="image" width="300"/>
</div>

**Done:**

- Tracker in orin with reid and angle detection
- Detic script
- Shelf detection function
- Moondream fast for orin

**In progress:**

- GPSR Commands
- Storing groceries commands 
- Dataset generation pipeline testing

**To do:**

- Test

## 2025-03-27

**Done:**

- Fix docker
- Moondream running in jetson

**In progress:**

- Shelve Detection
- Optimizing moondream
- Testing tracker in orin
- Testing and improving dataset generator pipeline

**To do:**

- Test model training pipeline

## 2025-03-20

**Done:**

- Poses and gestures detection
- GPSR commands first version
- Moondream dependency fix and new package
- Object detector 2d

**In progress:**

- Test in orin

**To do:**

- Test model training pipeline

## 2025-03-13

**Done:**

-
-

**In progress:**

- Fix docker

**To do:**

- Test tracker node

## 2025-03-06

**Done:**

- Tracker node with person angle
- Divided tasks
- Moondream integration to detect: laying down, standing or sitting down
- Beverage location in relation to image detection: center, left or right

**In progress:**

- Checking docker

**To do:**

-

## 2025-02-27

**Done:**

-

**In progress:**

- Waiting for task manager requirements

**To do:**

- Define tasks
- Created moondream method for detecting beverage from an image fram
- Created moondream method for describing person's clothes from an image frame using yolo person detection and image cropping
- Implemented both methods on receptionist commands

## 2025-02-20

**Done:**

-

**In progress:**

- Updating receptionist task manager

**To do:**

- Backlog

## 2025-02-13

**Done:**

- Update subtask_manager for follow_face demo

**In progress:**

- Restaurant commands
- Storing groceries commands
- Object detector

**To do:**

- GPSR Commands

## 2025-02-05

**Done:**

- Single person tracker

**In progress:**

- Restaurant commands
- Storing groceries commands
- Object detector

**To do:**

- GPSR Commands

## 2025-01-29

**Done:**

-

**In progress:**

- Restaurant commands
- Storing groceries commands
- Object detector

**To do:**

- GPSR Commands

## 2025-01-22

**Done:**

-

**In progress:**

- Tracker node tests
- Investigation for pose estimation classification. Considering training a Tensorflow Lite model with MediaPipe.

**To do:**

- Storing groceries commands
- Restaurant commands

## 2025-01-15

**Done:**

- Moondream2 wrapper

**In progress:**

- Tracker node:
  - REID module
- Pose/gesture/clothes detector:
  - Implemented S2T ratio with MediaPipe to determine person's general angle

**To do:**

- Object detector v1

## 2025-01-03

**Done:**

- Face recognition node in ROS2
- Receptionist commands in ROS2

**In progress:**

- Tracker node:
  - Research on different approaches
- Pose/gesture/clothes detector
  - Person's center detection and tracking methods added
  - Investigation started on angle detection
- Moondream2 wrapper

**To do:**

- Object detector v1

## 2024-12-20

**Done:**

- General vision package structure.

**In progress:**

- Pose/gesture/clothes detector.
- Moondream2 wrapper.

**To do:**

- Migration to ROS2
- Tracker
