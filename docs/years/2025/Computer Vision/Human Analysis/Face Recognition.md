# Face Recognition

This node uses the `face_recognition` library to detect and recognize faces in images. 

It also implements a manual tracker that improves performance by reducing the number of comparisons made during the recognition process. The tracker uses the position of the face in the previous frame to determine if it should be processed again, thus avoiding unnecessary computations.

It allows:

- Save a new face
- Recognize known faces
- Publish the coordinates of a face by: the largest face in the frame, or by a given name

## Areas of improvement

- Should be modular: keep the face recognition in a separate class
- Implement an abstract interface for face recognition so we could easily switch to another library if needed
- Add it to a separate ROS package