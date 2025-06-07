# Receptionist

## Description

The robot has to take two new guests to the living room to introduce them and offer a free place
to sit. (6 min limit)

`Main Goal`: The robot welcomes and assists two newcomers at a party while maintaining
appropriate gaze direction during conversation (at person speaking, direction of navigation).

`Optional Goals`: 
1. Open the entrance door for each arriving guest.
2. Describe the first guest for the second guest before reaching the living room
3. Identify similarities between the guests and the host and incorporate them into the conversation.


## Possible points
| **Category**                     | **Action**                                                      | **Score**   |
|-----------------------------------|----------------------------------------------------------------|-------------|
| **Main Goal**                     | Show the guest around (navigate to the beverage area and living room) | 2×30        |
|                                   | Look in the direction of navigation or at the navigation goal  | 2×15        |
|                                   | Confirm favorite drink                                          | 2×20        |
|                                   | Confirm interest of guest                                       | 2×20        |
|                                   | Tell position of favorite drink                                 | 2×20        |
|                                   | Offer a free seat to the new guest                             | 2×100       |
|                                   | Look at the person talking                                     | 2×75        |
|                                   | Introduce both guests to each other                           | 75          |
| **Bonus Rewards**                 | Open the entrance door for a guest                            | 2×200       |
|                                   | State a shared interest between two or more persons           | 50          |
|                                   | Describe the first guest to the second guest (per correct attribute) | 4×30        |
| **Penalties**                     | Wrong guest information was memorized (continue with wrong name or drink) | 2×–50  |
|                                   | Interest was not or wrongly memorized                         | 2×–50       |
|                                   | Persistent inappropriate gaze (away from conversational partner) | –50     |
|                                   | Persistent gaze not in the direction of navigation while moving | –25      |
|                                   | Describe the first guest to the second guest (per incorrect attribute) | 4×–30  |
|                                   | Wrongly stating a similarity                                  | –30         |
| **Deus Ex Machina**               | Alternative HRI                                               | 2×–75       |
|                                   | Not recognizing people                                        | 2×–200      |
| **Special Penalties & Bonuses**   | Not attending (see sec. 3.9.1)                                | –500        |
|                                   | Outstanding performance (see sec. 3.9.3)                      | 120         |
| **Total Score (excluding special penalties & standard bonuses)** |                            | 1205        |

<hr />
<br />

# Tasks per Area

## Navigation

### navigate_to

Move to a predefined position (entrance, beverage_area, living_room)

Args

- position: to be defined but should represent predefined locations

Return

- None

## Manipulation

### move_to_position
Move the arm to predefined positions: 

Navigation: Arm should be pointing to the navigation direction.

Gaze: Arm should be positioned at an angle to see guest faces of potentially different heights.

Table: Arm should be pointed to a table top-view to identify items.

<br />
Args

- position: string, int or enum (find best option), representing positions

Return:

- None

### pan_to

Move the arm horizontally at gaze level given an angle to allow the camera to have a different field of view for seat detection.

*Subtask Manager*

Args

- angle: int (in degrees, where 0 is the center, - is to the left and + is to the right)

Return

- None

### follow_face

Follow the face of a person with the arm. The vision topic will always be publishing the Point of the face to be tracked, so for manipulation, there should be a service to start following the face with the arm when requested or to stop following.

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

### is_positive
The robot will sometime need to ensure it heard something correctly, so it will ask for confirmation. Hence a function is necessary to identify if the response is positive (yes) or not.

Args

- statement: str (guest response, eg: yes, that's right, wrong, etc)

Return 

- result: bool 

### common_interest
Given the common interest and name of two people, find something in common and return a message such as: X is interested in soccer and Y in basketball, so you both like team sports.

Args

- person1: tuple (name: str, interest: str)
- person2: tuple (name: str, interest: str)

Return

- common_message: string

## Vision

### find_drink

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

### save_face_name
  Save the name of a guest and associate it to a face.

  *Subtask Manager*
  Args

  - name: string

  Return

  - status: int (success, execution error, terminal error or target not found ENUM)

### follow_face
A node should publish the coordinates of the largest face available so that the arm can follow it.

### detect_person
Return true when a person is detected or stop when timeout is reached.

Args:

- timeout: float (time limit)

Return:

- None

### detect_guest
There should be a service to change the person's face to be followed to a specific guest instead of publishing largest face and vice-versa. Additionally, when following by name, the service should only return true when the person is detected or a timeout is reached.

 Args:

 - name: str (either person name or "largest_face")
 - timeout: float? (time limit)

 Return:

 - result: bool (return true when the person is detected)

### describe_guest
Given the image of the guest, provide a description of the person.

Args:

- None

Return:

- description: string

<br />
<hr />

# Main states

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
