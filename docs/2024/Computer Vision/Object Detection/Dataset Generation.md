# Dataset generation

## Pipeline
A pipeline was developed that produces a dataset with the necessary encoding to be trained with YoloV8. This pipeline utilizes two main technologies. The first is `GroundingDINO`, which enables us to detect objects of our interest and obtain their bounding boxes. The second is `SAM` (Segment Anything Model), which we use to crop images from their original backgrounds and create images containing only the desired objects. To achieve this, SAM requires the bounding boxes of the objects we want to segment, which are provided by GroundingDINO. 

## Dataset transformation
Additionally, a module was developed to transforms any object detection dataset into an object segmentation dataset. This is achieved using SAM, leveraging the YOLO bounding box annotations and re-annotating the labels with a segmentation notation. 

