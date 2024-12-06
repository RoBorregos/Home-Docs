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

## Tasks per Area

### Vision

- Detect calling or waving customer
- Re-identify the person in case they lower their hand and the robot loses sight of them
- Detect objects from the kitchen bar

### Navigation
- Reach a customer’s table in an unknown environment
- Return to the kitchen bar
- If computer vision is used to re-identify the customer, the robot should return to the customer’s table according to the customer’s position provided by the vision system. However, a different approach would be to keep track of the customer’s position by online mapping or other means.

### Manipulation
- Follow the face of a person when taking an order
- Pick up an object from the kitchen bar
- Place the object on the table

### HRI
- Take an order from a customer
- Communicate any needs to the bar man
- Interpret the objects to be served

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
  <img width="500px" src="/assets/tasks/restaurantDiagram.png" alt="Restaurant state diagram">
</p>

