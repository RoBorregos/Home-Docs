# Clothing Detection

Clothing-based identification is a key capability in **GPSR** (General Purpose Service Robot) and **EGPSR** (Enhanced General Purpose Service Robot) tasks, where the robot may be asked to "find the person wearing a red jacket" or "count how many people are in white shirts." These instructions rely on natural human language and require a system that can understand both visual content and semantic queries.

To address this, the clothing detection module uses a combination of:

* **YOLOv8**: For person detection and bounding box generation.
* **Moondream**: A vision-language model to interpret clothing from cropped images and respond to prompts.
* **ROS 2 services**: To expose the functionality in a modular and scalable manner.



## Overview

1. **Detect all people in the camera frame** using YOLOv8.
2. **Crop the image** around each detected person using their bounding box.
3. **Formulate a language prompt** describing the target clothing, e.g., *“Is the person wearing a red shirt?”*
4. **Query Moondream** with the cropped image and prompt.
5. **Interpret the result** (binary: `1` = match, `0` = no match).
6. **Return the total count** of people matching the description.


## Service Callback: `count_by_color_callback`

This is the entry point when a client wants to count people based on clothing color/type.

```python
def count_by_color_callback(self, request, response):
    """Callback to count people wearing a specific color and clothing."""
    self.get_logger().info("Executing service Count By Color")

    if self.image is None:
        response.success = False
        response.count = 0
        return response

    frame = self.image
    self.output_image = frame.copy()

    clothing = request.clothing
    color = request.color

    self.get_detections(frame, 0)

    count = 0

    for person in self.people:
        x1, y1, x2, y2 = person["bbox"]

        prompt = f"Reply only with 1 if the person is wearing a {color} {clothing}. Otherwise, reply only with 0."
        status, response_q = self.moondream_crop_query(
            prompt, [float(y1), float(x1), float(y2), float(x2)]
        )

        if status:
            response_clean = response_q.strip()
            if response_clean == "1":
                count += 1
                self.get_logger().info(f"Person {count} is wearing a {color} {clothing}.")
            elif response_clean != "0":
                self.get_logger().warn(f"Unexpected response: {response_clean}")

    response.success = True
    response.count = count
    self.get_logger().info(f"People wearing a {color} {clothing}: {count}")
    return response
```

* The prompt is **generated dynamically** based on user input (`color`, `clothing`), allowing any combination without hardcoding.
* The decision threshold is **binary (1 or 0)** to simplify interpretation and reduce ambiguity.
* Only results with exact match (`"1"`) are counted.


## Bounding Box Normalization & Moondream Query

Since Moondream expects input in normalized coordinates, we extract and normalize the bounding box for each person before sending the request:

```python
def moondream_crop_query(self, prompt: str, bbox: list[float]) -> tuple[int, str]:
    """Makes a query of the current image using Moondream."""
    self.get_logger().info(f"Querying image with prompt: {prompt}")

    height, width = self.image.shape[:2]

    ymin = bbox[0] / height
    xmin = bbox[1] / width
    ymax = bbox[2] / height
    xmax = bbox[3] / width

    request = CropQuery.Request()
    request.query = prompt
    request.ymin = ymin
    request.xmin = xmin
    request.ymax = ymax
    request.xmax = xmax

    future = self.moondream_client.call_async(request)
    future = self.wait_for_future(future, 15)
    result = future.result()

    if result is None:
        self.get_logger().error("Moondream service returned None.")
        return 0, "0"

    if result.success:
        self.get_logger().info(f"Moondream result: {result.result}")
        return 1, result.result
```

* `call_async()` allows **non-blocking queries**, necessary when multiple services are used in parallel.
* A custom utility (`wait_for_future`) ensures that the query completes before proceeding.



## Asynchronous Handling with `wait_for_future`

This helper function waits for the result of an asynchronous Moondream call:

```python
def wait_for_future(self, future, timeout=5):
    start_time = time.time()
    while future is None and (time.time() - start_time) < timeout:
        pass
    if future is None:
        return False
    while not future.done() and (time.time() - start_time) < timeout:
        pass
    return future
```

### Why it's needed:

* ROS 2 service clients operate asynchronously by default.
* Without this, you would either:

  * Proceed without a result.
  * Block indefinitely.
* This keeps the node responsive while ensuring results are actually used.



## Multithreading & Reentrant Callback Group

Clothing queries might be long-running due to model latency. To prevent blocking other services or the image stream, the node uses:

```python
self.callback_group = rclpy.callback_groups.ReentrantCallbackGroup()
```

And in the service:

```python
self.count_by_color_service = self.create_service(
    CountByColor,
    COUNT_BY_COLOR_TOPIC,
    self.count_by_color_callback,
    callback_group=self.callback_group,
)
```

In `main()`:

```python
executor = rclpy.executors.MultiThreadedExecutor(8)
```

### Key Benefits:

* Multiple requests can be processed **concurrently**.
* Other parts of the node (e.g., image acquisition, pose queries) remain functional.
* Reentrant group allows the **same callback** to run in parallel if triggered twice.