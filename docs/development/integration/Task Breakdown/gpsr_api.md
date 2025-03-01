# Proposed API for GPSR

## Vision

1. count(target: str) -> int

- target (str): The target to identify and count. There can be many targets for this function.
- int -> returns the amount of targets found in the environment.
  The following are required:
  - Related to gestures or postures
    - sitting_person, standing_person, lying_person, waving_person, person_raising_left_arm, person_raising_right_arm, person_pointing_left, person pointing to the right
  - Related to clothing, the following combinations:
    - color_list = ["blue", "yellow", "black", "white", "red", "orange", "gray"]
    - clothe_list = ["t shirt", "shirt", "blouse", "sweater", "coat", "jacket"]

2. locate(target: str) -> point(x, y, z)

- target (str): The target to identify and locate. There can be many targets for this function.
- point(x, y, z) -> returns the coordinates of the target in the environment.
  The following are required:
  - Related to gestures or postures
  - sitting_person, standing_person, lying_person, waving_person, person_raising_left_arm, person_raising_right_arm, person_pointing_left, person pointing to the right
  - Related to clothing, the following combinations:
    - color_list = ["blue", "yellow", "black", "white", "red", "orange", "gray"]
    - clothe_list = ["t shirt", "shirt", "blouse", "sweater", "coat", "jacket"]

3. identify(target_name: str) -> point(x, y, z)

- Identify a person by a previously defined name.

4. save_person(new_name: str) -> void

- Save a person (face) with a given name.

5. object detection model (to allow pick and place):

- All robocup objects
- Some examples are:

```bash
{
 'orange juice', 'red wine', 'milk', 'iced tea', 'cola',
 'tropical juice', 'juice pack', 'apple', 'pear', 'lemon',
 'peach', 'banana', 'strawberry', 'orange', 'plum', 'cheezit',
 'cornflakes', 'pringles', 'tuna', 'sugar', 'strawberry jello',
 'tomato soup', 'mustard', 'chocolate jello', 'spam', 'coffee grounds',
 'plate', 'fork', 'spoon', 'cup', 'knife', 'bowl', 'rubiks cube',
 'soccer ball', 'dice', 'tennis ball', 'baseball', 'cleanser', 'sponge'
}
```
