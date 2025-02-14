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

### navigate_to_target

Move to a target coordinate (customer)

*Subtask Manager*

Args
- coordinates: Tuple[float,float,float] (3D coordinates to set nav goal)

Return
- None

### navigate_to_origin

Return to starting point (kitchen bar)

*Subtask Manager*

Args
- None

Return
- None

## Manipulation

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

## HRI
### say
Say text provided

### get_order
Get items asked by customer and quantity

*Subtask Manager*

Args
- None

Return
- order: string? (will depend on picking approach
)

## Vision

### detect_waving_customer

  Check if a person is waving/raising their hand.

  *Subtask Manager*

  Args
  - None

  Return 
  - status: int (success, execution error, terminal error or target not found ENUM)
  - coordinates: Tuple[float,float,float] (3D coordinates to set nav goal)

  *Node implementation: First iteration:*
  
  Capture current frame and check if there is a person waving/raising their hand.

  Service that returns msg:
  - bool found: if a person waving/raising hand is found
  - point coordinates (from geometry msgs): 3D coordinates of the person detected

  *Node implementation: Second iteration (if first option is unstable for nav):*

  If needed, the person detected should be tracked and their coordinates should be published 
  to improve performance.

  Service that returns msg:
  - bool found
  - point coordinates(from geometry msgs)

  Publisher:
  - point coordinates (from geometry msgs) of the person being tracked 

### follow_person
  Activate tracking to publish coordinates of person that will be followed.

  *Subtask Manager*
  Args
  - None

  Return
  - None

### follow_face
A node should publish the coordinates of the largest face available so that the arm can follow it.

<hr />

## Main states

### Detecting customers
- In this state, the robot should look for a customer calling or waving. 

### Navigation to the customer
- The robot should navigate to the customer’s table.
- This could be achieved with a *follow person* approach as long as the customer can be re-identified.
- Another approach would involve online mapping.

### Taking the order
- For this state, the robot should take the order from the customer.

### Navigation to the kitchen bar
- The robot should return to the kitchen bar to pick up the objects.

### Picking objects
- If a tray is used, the robot should request the objects from the barman to be placed in the tray or pick them and placing them in the tray by itself.
- If no tray is used, the robot should pick up the objects one by one.

### Returning to the customer
- The robot should return to the customer’s table to serve the order.

### Placing objects
- The robot should place the objects on the table.
- If a tray is used, the robot should serve the objects from the tray or request the customer to take them.

<p align="center">
  <img width="500px" src="/assets/tasks/RestaurantDiagram.png" alt="Restaurant state diagram">
</p>

