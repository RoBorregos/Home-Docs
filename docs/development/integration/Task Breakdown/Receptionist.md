# Restaurant

## Description

The robot retrieves and serves orders to several customers in a real restaurant previously unknown to the robot.

`Main Goal`: Detect calling or waving customer, reach a customer’s table without prior guidance/training. Take and serve all orders.

`Optional Goals`: Use an unattached tray to transport the order.

## Task Breakdown
1. The robot should identify a customer calling or waving.
2. The robot should reach the customer’s table.
3. The robot should take the order (keep eye contact).
4. The robot should go back to the *Kitchen bar* and pick the requested object.
5. The robot should return to the identified customer and serve the order.


## Possible points
| **Category**           | **Action**                                                 | **Score**   |
|-------------------------|-----------------------------------------------------------|-------------|
| **Regular Rewards**     | Detect calling or waving customer                         | 2×100       |
|                         | Reach a customer’s table without prior guidance/training  | 2×100       |
|                         | Take an order.                                            | 2×300       |
|                         | Serve an order.                                           | 2×300       |
| **Bonus Rewards**       | Use an unattached tray to transport                       | 2×200       |
| **Regular Penalties**   | Not making eye-contact when taking an order               | 2×–80       |
|                         | Not reaching the bar (barman has to move from behind the bar to interact with the robot) | 2×–80 |
| **Deus ex Machina Penalties** | Being guided to a table                              | 2×–200      |
|                         | Asking the Barman to handover object to the robot         | 4×–50       |
|                         | Guest needing to take the object from a tray or the robot’s hand | 4×–50  |
|                         | Being told/pointed where is a table/Kitchen-bar           | 2×–100      |
| **Special Penalties & Bonuses** | Not attending (see sec. 3.9.1)                   | –500        |
|                         | Using alternative start signal (see sec. 3.7.8)          | –100        |
|                         | Outstanding performance (see sec. 3.9.3)                 | 200         |
| **Total**               | Total Score (excluding special penalties & standard bonuses) | 2000    |

<hr />

# Tasks per Area

## Navigation

### navigate_to_position

Move to a predefined position

Args
- position: to be defined

Return
- None

## Manipulation

### move_to_position
Move the arm to predefined positions: Navigation and Interaction
Navigation: Arm should be pointing to the navigation direction.
Interaction: Arm should be positioned at an angle to see guest faces of potentially different heights.

Args
- position: string or int (representing navigation or interaction position)

Return:
- None

### pan_camera

Move the arm horizontally either left or right to allow the camera to have a different field of view for customer detection.

*Subtask Manager*

Args
- direction: int (either -1(pan to left) or 1(pan to right)), maybe also sending the angle 

Return
- None

### follow_face

Follow the face of a person with the arm. There should be a subscriber for the vision topic, but the arm should only start following the face when requested (this could be a service or a subscriber).

*Subtask Manager*

Args
- follow: bool (True to follow the face, False to stop following)

Return
- None

### open_door

For extra points the robot should open the door :o

## HRI
### say
Say text provided

### hear
The robot should listen and be prepared for varying responses in order to identify: name, favorite drink and interests

  Return
  - value: string (either name, drink or interest)

### generate_small_talk
Given 2-3 guest interests, generate an introduction with small talk regarding common interests.

    Return
    - small_talk: string

## Vision

### find_beverage

  Check if there is a beverage available in a table and return its approximate position.

  *Subtask Manager*

  Args
  - drink: string (could be any type of drink)

  Return 
  - status: int (success, execution error, terminal error or target not found ENUM)
  - found: bool (if the drink is available or not)
  - position: string (aproximate position on the table: left, right, center, top, bottom)


### find_seat
  Find an available seat.

  *Subtask Manager*
  Args
  - None

  Return
  - position: Point (normalized)

### save_face
  Save the name of a guest and associate it to a face.

  *Subtask Manager*
  Args
  - name: string

  Return
  - status: int (success, execution error, terminal error or target not found ENUM)

### follow_face
A node should publish the coordinates of the largest face available so that the arm can follow it.

<hr />

## Main states

### Wait for guest
- Wait for a guest to be in front of the robot

### Greeting
- Greet the new guest
- Ask for name 
- Associate name to face

### Navigate to beverages
- Guide guest to beverage area

### Beverages
- Ask for favorite drink
- Check if the drink is available
- Ask for interest

### Navigate to living room
- Guide guest to living room area

### Find seat
- Find an available seat 
- Point to seat
- Ask guest to take a seat

### Introduction
- Gaze at the host and introduce him to the new guest
- If available, gaze at other guest and repeat 

### Navigate to entrance
- Go back to the entrance
