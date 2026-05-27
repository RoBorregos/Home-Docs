# Trash Detection

Trash Detection adds two main capabilities to the vision pipeline:

- Tag detections as `trash/<label>` when the object belongs to a category set via service (e.g. `kitchen`).
- Localize trashcan(s) by requesting image points from MoonDream and converting them to 3D coordinates using depth + camera_info.

The main detector (`object_detector_node`) exposes the `SetTrashCategory` service to set the active category; the `trash_detection_node` offers `TrashcanDetection` and publishes a debug image.

## Overview (flow)
1. The `object_detector_node` (detector) processes the RGB image (+ depth/camera_info) and publishes an `ObjectDetectionArray` on `DETECTIONS_TOPIC`.

    - It also exposes the `SetTrashCategory` service (request `{ category: string }`) to set the active category. When a category is set, the detector compares each `label_text` against the `object_to_category` mapping (file `frida_constants/data/objects.json`) and can relabel relevant detections as `trash/<label>` before publishing them.

    - It also provides a `DetectionHandler` (on `DETECTION_HANDLER_TOPIC_SRV`) which allows clients to request filtered detections (by single label, set of labels, or the nearest one).

2. The `trash_detection_node` acts as a specialized service that consumes `DETECTIONS_TOPIC`:

    - To localize trashcan(s) in 3D it calls MoonDream (`ObjectPoints`), obtains normalized image points, maps them to pixels, queries `depth` and `camera_info`, and returns an `ObjectDetectionArray` with `point3d` via the `TrashcanDetection` service.

    - It publishes a debug image on `TRASH_DEBUG_IMAGE_TOPIC` showing the calculated points/bboxes.

## Service Callback: `get_trashcan` (example)

This is the pattern used in `trash_detection_node.py`:

```python
def get_trashcan(self, req, res):
    if self.imageInfo is None or self.depth_image is None:
        res.success = False
        return res

    trashcan_pts = self.get_moondream_points("black trashcan")
    if not trashcan_pts:
        res.success = False
        return res

    trashcans = ObjectDetectionArray()
    for pt in trashcan_pts:
        point2d = (clamp_x, clamp_y)  # normalize and map to pixels
        depth = get_depth(self.depth_image, point2d)
        point3d = deproject_pixel_to_point(self.imageInfo, point2d, depth)
        ptStamped = self.build_point_stamped(point3d)

        trash = ObjectDetection()
        trash.label_text = "trashcan"
        trash.point3d = ptStamped
        trashcans.detections.append(trash)

    res.detection_array = trashcans
    res.success = True
    return res
```

