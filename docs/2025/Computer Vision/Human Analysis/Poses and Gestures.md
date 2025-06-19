# Poses and Gestures

Pose and gesture recognition are essential in tasks such as **GPSR** (General Purpose Service Robot) and **EGPSR** (Enhanced General Purpose Service Robot). The main approach consists of using MediaPipe’s pose tracking solution combined with OpenCV for visualization and gesture detection, while Moondream is used as a query service to complement pose recognition.


## Gestures

The `PoseDetection` class uses MediaPipe to detect and analyze human body landmarks from video frames captured by a camera. 

* Applies heuristic rules based on joint angles and landmark positions to classify gestures.
* Visualizes pose landmarks and joint angles on the video frames.
* Captures video from a webcam and processes it frame by frame.
* Supports the following gestures:

  * Raising left/right arm
  * Pointing left/right
  * Waving
  * Unknown (default when no gesture detected)


### Class `PoseDetection`

This class encapsulates all logic related to detecting body landmarks, drawing on images, and recognizing gestures.



### Initialization: 

```python
def __init__(self):
    print("Pose Detection Ready")
    self.mp_pose = mp.solutions.pose
    self.pose = self.mp_pose.Pose()
    self.mp_drawing = mp.solutions.drawing_utils
```

* Sets up MediaPipe’s Pose model.
* `self.pose` is the core object used for processing images to find pose landmarks.
* Prints a readiness message for confirmation.



### Drawing Landmarks: 

```python
def draw_landmarks(self, image, results, mp_pose):
    image_height, image_width, _ = image.shape
    landmarks_to_draw = [
        self.mp_pose.PoseLandmark.LEFT_SHOULDER,
        self.mp_pose.PoseLandmark.LEFT_ELBOW,
        self.mp_pose.PoseLandmark.LEFT_WRIST,
        self.mp_pose.PoseLandmark.RIGHT_SHOULDER,
        self.mp_pose.PoseLandmark.RIGHT_ELBOW,
        self.mp_pose.PoseLandmark.RIGHT_WRIST,
        self.mp_pose.PoseLandmark.LEFT_HIP,
        self.mp_pose.PoseLandmark.RIGHT_HIP,
    ]

    for landmark in landmarks_to_draw:
        if results.pose_landmarks is not None:
            landmark_data = results.pose_landmarks.landmark[landmark]
            if landmark_data.visibility > 0.5:
                x, y = (
                    int(landmark_data.x * image_width),
                    int(landmark_data.y * image_height),
                )
                cv2.circle(image, (x, y), 5, (0, 255, 0), -1)
    self.draw_connections(image, results, mp_pose)
```

* Receives the current video frame (`image`) and the pose detection results.
* Selects key landmarks relevant for upper body gestures.
* Draws a green circle on the image at each landmark’s pixel coordinates if the landmark is confidently visible (visibility > 0.5).
* Calls `draw_connections` to add lines and angle annotations between joints.



### Drawing Connections and Angles

```python
def draw_connections(self, image, results, mp_pose):
    connections = [
        (
            mp_pose.PoseLandmark.LEFT_SHOULDER,
            mp_pose.PoseLandmark.LEFT_ELBOW,
            mp_pose.PoseLandmark.LEFT_WRIST,
        ),
        (
            mp_pose.PoseLandmark.RIGHT_SHOULDER,
            mp_pose.PoseLandmark.RIGHT_ELBOW,
            mp_pose.PoseLandmark.RIGHT_WRIST,
        ),
    ]
    for start_idx, mid_idx, end_idx in connections:
        self.draw_line_and_angle(image, results, start_idx, mid_idx, end_idx)
```

* Defines joint triplets (shoulder → elbow → wrist) for both arms.
* For each triplet, calls `draw_line_and_angle` to visualize the arm segments and annotate the joint angle.

```python
def draw_line_and_angle(self, image, results, start_idx, mid_idx, end_idx):
    if results.pose_landmarks:
        start, mid, end = (
            results.pose_landmarks.landmark[start_idx],
            results.pose_landmarks.landmark[mid_idx],
            results.pose_landmarks.landmark[end_idx],
        )
        if start.visibility > 0.5 and mid.visibility > 0.5 and end.visibility > 0.5:
            start_point = (
                int(start.x * image.shape[1]),
                int(start.y * image.shape[0]),
            )
            mid_point = (int(mid.x * image.shape[1]), int(mid.y * image.shape[0]))
            end_point = (int(end.x * image.shape[1]), int(end.y * image.shape[0]))
            cv2.line(image, start_point, mid_point, (0, 0, 255), 2)
            cv2.line(image, mid_point, end_point, (0, 0, 255), 2)
            angle = self.get_angle(start, mid, end)
            cv2.putText(
                image,
                f"{int(angle)} - {start_idx} {end_idx}",
                (mid_point[0] - 20, mid_point[1] - 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 0),
                2,
            )
```

* Checks if all three landmarks are confidently visible.
* Converts normalized landmark coordinates into pixel coordinates.
* Draws red lines connecting shoulder to elbow and elbow to wrist.
* Calculates the angle at the elbow joint using `get_angle`.
* Overlays the angle value as text near the elbow for visualization.



### Calculating Angles: 

```python
def get_angle(self, p1, p2, p3):
    p1, p2, p3 = (
        np.array([p1.x, p1.y]),
        np.array([p2.x, p2.y]),
        np.array([p3.x, p3.y]),
    )
    l1, l2, l3 = (
        np.linalg.norm(p2 - p3),
        np.linalg.norm(p1 - p3),
        np.linalg.norm(p1 - p2),
    )
    return abs(degrees(acos((l1**2 + l2**2 - l3**2) / (2 * l1 * l2))))
```

* Converts the landmarks into 2D numpy arrays (x, y).
* Uses the cosine rule to calculate the angle formed at `p2`.
* Returns the angle in degrees, representing the bend at the joint.



### Gesture Detection Logic

```python
def detectGesture(self, image):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results_p = self.pose.process(image_rgb)

    gestures = Gestures.UNKNOWN

    if results_p.pose_landmarks:
        mid_x = self.get_midpoint_x(results_p)

        if not self.is_chest_visible(image) or self.are_arms_down(results_p.pose_landmarks):
            print(f"Detected gesture: {gestures}")
            return gestures

        # Left hand gestures
        elif self.is_raising_left_arm(mid_x, results_p):
            gestures = Gestures.RAISING_LEFT_ARM
        elif self.is_pointing_left(mid_x, results_p):
            gestures = Gestures.POINTING_LEFT

        # Right hand gestures
        elif self.is_raising_right_arm(mid_x, results_p):
            gestures = Gestures.RAISING_RIGHT_ARM
        elif self.is_pointing_right(mid_x, results_p):
            gestures = Gestures.POINTING_RIGHT
        elif self.is_waving(results_p):
            gestures = Gestures.WAVING

    print(f"Detected gesture: {gestures}")
    return gestures
```

* Converts the frame to RGB (required by MediaPipe).
* Runs pose detection to get landmarks.
* Initializes gesture as UNKNOWN.
* Checks if the chest (both shoulders) is visible and arms are not down; otherwise, no gesture is detected.
* Uses helper methods to detect specific gestures in a priority order.
* Returns the detected gesture enum.



### Specific Gesture Helper Functions

These methods analyze landmark positions and joint angles for each gesture type.

* **Raising Arm:** Checks if the arm is bent less than 35°, with wrist and elbow above the shoulder.
* **Pointing:** Compares finger positions relative to the shoulders and the chest midline.
* **Waving:** Uses elbow-wrist angle thresholds to identify waving movement.

Example:

```python
def is_raising_left_arm(self, mid_x, results):
    landmarks = results.pose_landmarks.landmark
    left_shoulder = landmarks[11]
    left_elbow = landmarks[13]
    left_wrist = landmarks[15]

    angle = self.get_angle(left_shoulder, left_elbow, left_wrist)

    if (
        angle < 35
        and left_wrist.y < left_shoulder.y
        and left_elbow.y < left_shoulder.y
    ):
        return True

    return False
```



### Main Loop: 

* Opens the default webcam.
* Reads frames continuously.
* For each frame:

  * Detects gesture.
  * Draws landmarks, connections, and angles.
  * Displays the detected gesture name on the frame.
  * Shows the annotated frame in a window.

### Areas of Improvement

* *Gesture transition and robustness* can be improved by analyzing multiple consecutive frames before confirming a detected gesture. This temporal smoothing reduces false positives caused by brief occlusions or noisy detections in single frames, ensuring more stable and reliable gesture recognition with just one camera.

* *Angle calculations* currently rely on 2D landmarks, but using normalized 3D coordinates from MediaPipe would yield more accurate joint angles. This would enhance the robustness of gesture detection in three-dimensional space, especially when the user moves or rotates.

* *Calibration* is necessary because different users have varying body proportions and movement styles. The current fixed thresholds (for example, angle < 35°) may not generalize well across all users. An effective improvement would be to incorporate a machine learning model that personalizes these thresholds, adapting to each user for better accuracy and reliability.

## Poses

Unlike gesture recognition, which relies on joint angles and MediaPipe heuristics, **pose classification** for full-body states (e.g., standing, sitting, or lying down) is delegated to **Moondream**, a vision-language model queried via a service. This approach improves flexibility, as body posture may not be easily inferred from 2D landmarks.

The process consists of the following steps:

1. **Person Detection (YOLO):** The full frame is processed using YOLOv8 to detect people and extract bounding boxes.
2. **Crop and Prompt Construction:** Each detected person is cropped from the frame, and a natural language prompt is created, asking Moondream to classify the person’s pose.
3. **Query Execution:** The cropped region and the prompt are sent to the `CropQuery` service client. The response is parsed to determine the pose.

Here is a simplified version of the relevant logic from `count_by_pose_callback`:

```python
for person in self.people:
    x1, y1, x2, y2 = person["bbox"]

    prompt = f"Reply only with 1 if the person is {pose_requested}. Otherwise, reply only with 0."
    status, response_q = self.moondream_crop_query(
        prompt, [float(y1), float(x1), float(y2), float(x2)]
    )
    if status:
        response_clean = response_q.strip()
        if response_clean == "1":
            pose_count[pose_requested_enum] += 1
```

And the lower-level query call:

```python
def moondream_crop_query(self, prompt: str, bbox: list[float]) -> tuple[int, str]:
        """Makes a query of the current image using moondream."""
        self.get_logger().info(f"Querying image with prompt: {prompt}")

        height, width = self.image.shape[:2]

        ymin = bbox[0] / height
        xmin = bbox[1] / width
        ymax = bbox[2] / height
        xmax = bbox[3] / width

        request = CropQuery.Request(query=prompt, ymin=ymin, xmin=xmin, ymax=ymax, xmax=xmax)
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

### Areas of Improvement

* *Robustness*: While Moondream improves over heuristic methods, its performance still depends on bounding box quality and context. Responses may vary due to ambiguous crops or lighting conditions. A secondary confirmation method or pose tracking across time could increase confidence.

* *It lacks temporal context*: Because pose classification is queried per frame, temporary occlusions or motion blur may lead to inconsistent results. Implementing a simple voting mechanism or temporal smoothing over a short window of frames could significantly improve stability and reliability in real-time settings.