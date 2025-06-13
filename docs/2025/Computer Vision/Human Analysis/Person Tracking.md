# Person Tracking

Person tracking requires the robot to identify a person and be able to follow them as they move around the environment. This process is required in several tasks, such as Carry My Luggage and GPSR (General Purpose Service Robot). Therefore, computational vision is required to detect, identify and track a person.

## Person detection

In order to detect people, the `YOLO v8` model was used, obtaining the bounding boxes of each person in each frame. Additionally the `ByteTracker` algorithm was implemented to automatically assign a track_id to each person that is still visible from the previous frame. However, using the default tracker from YOLO was not consistent enough, since people who go behind large objects or even other people are assigned new ids, since this tracker does not keep track of people who leave and re-enter the frame. This introduced the necessity of a re-identification model that could recognize people who have appeared in previous frames, specially because the tracked person could exit the frame at any moment and it is necessary to identify them again to continue following.

```python
# Get the results from the YOLOv8 model
results = self.model.track(frame, persist=True, tracker='bytetrack.yaml', classes=0, verbose=False)
```

## Person re-identification

To re-identify people, the repository [Person_reID_baseline_pytorch]("https://github.com/layumi/Person_reID_baseline_pytorch") was used as a base to train different models using the `Market1501` dataset. More specifically, the models `ResNet50`, `Swin`, `PCB` and `DenseNet` were trained and tested, eventually opting for the `DenseNet` model as it was the lightest last year. However, in order to improve re-identification, this year we used the larger `Swin` model, which obtained more accurate feature vectors from an image with a person.

```python
# Crop the image using the bbox coordinates
cropped_image = frame[y1:y2, x1:x2]

# Convert the image array to a PIL image
pil_image = PILImage.fromarray(cropped_image)

# Get feature
with torch.no_grad():
    new_feature = extract_feature_from_img(pil_image, self.model_reid)
```

## Implementation

With the tracker and re-id modules, the general flow is the following:

1. When triggered, the person with the largest bounding box area is assigned as the tracked person and their embeddings are extracted and stored. (The tracked person can also be set by the pose, gesture or color-clothes combination)

2. If the person is in frame, the re-id is not triggered. However, the angle to which the person is facing is calculated. This way, we save 4 different embeddings for the same person according to the angle they are facing. This allows to compare embeddings by angle, which is more precise because for example a person facing to the camera will look different than when facing sideways.

3. If the person is not in frame, the embeddings of the tracked person are compared to the embeddings of all the people detected in the current frame. This helps to ensure that the person is detected again if they re-enter the frame or change their position significantly.


## Areas of improvement

- It should be modular: Use an abstract class to define the interface for person tracker, which would allow to use different models or algorithms if needed.
- It should also be a lot faster. Currently comparing all people to the tracked person takes a lot of time, but is the best approach to re-idenify the person.
- It should be added to its own package. 
- This uses the same model from a year ago, however it is likely that new models are now available or we could even explore making our own model.