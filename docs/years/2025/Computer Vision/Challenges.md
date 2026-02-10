# Vision Exercises

To get familiar with the computer vision module, here are two exercises that involve the most used tools and libraries:

## 1. Count people
Make a node that counts the number of people in the current frame. This should be called through a ros2 service that returns only the number of people detected. 

<details>
<summary>Hint</summary>

You can use yolo to detect people with classes=[0] and then count the number of detections.

</details>

<details><summary>Hint 2</summary>

Checkout the following example that gets the detections from an image and draws bounding boxes:

```python
results = self.yolo_model(image, verbose=False, classes=0)

for out in results:
    for box in out.boxes:
        x, y, w, h = [round(i) for i in box.xywh[0].tolist()]
        confidence = box.conf.item()

        if (
            confidence > CONF_THRESHOLD
            and x >= int(width * PERCENTAGE)
            and x <= int(width * (1 - PERCENTAGE))
        ):
            cv2.rectangle(
                self.output_image,
                (int(x - w / 2), int(y - h / 2)),
                (int(x + w / 2), int(y + h / 2)),
                (0, 255, 0),
                2,
            )
            break
```

</details>

<details><summary>Hint 3</summary>

Check the following code that creates a service:

```python
self.count_people_service = self.create_service(
            YourSRV, "your_topic", self.your_function_callback
        )
```

</details>

## 2. Count object requested
Make a node that counts the number of objects requested in the current frame. This should be called through a ros2 service, where the request is a valid object class (e.g. "person", "bottle", "chair") and the response is the number of objects detected.

[Checkout valid classes](https://gist.github.com/rcland12/dc48e1963268ff98c8b2c4543e7a9be8)

<details>
<summary>Hint 1</summary>

You can use yolo to detect objects with all available classes and then check if the class label matches.

</details>


<details>
<summary>Hint 2</summary>

You can get the class using the following code:

```python
# Here the model would use the path you specify
model = YOLO("yolo_model.pt")

# ... 

for out in results:
    for box in out.boxes:
        x1, y1, x2, y2 = [round(x) for x in box.xyxy[0].tolist()]

        # Get class name
        class_id = box.cls[0].item()
        label = model.names[class_id]
```

</details>

<details><summary>Hint 3</summary>
You would need to add a srv to frida_interfaces that expects a string and returns an int. You can check the following example:

``` python
# This would be in home2/frida_interfaces/vision/srv/YourSRVName.srv

string object_name 
---
int32 count
```

and use it in your node like this:

```python
from frida_interfaces.srv import YourSRVName
```
