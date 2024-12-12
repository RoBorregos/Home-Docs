# Storing Groceries

## Description

The task consists of storing groceries in a cabinet from a table with the objects. 

- In the cabinet, there are shelves where the groceries must be placed, there might be some groceries already placed.
  - If this is the case, the robot must place the groceries in the shelves that have the same category of the groceries being placed.

## Needs from other areas

- Manipulation: The robot must be able to pick up and place objects. Must have reach for the table and the cabinet shelves.
- Perception: translate the shelf layer into a placing location.
- Vision: Object detection.
- Navigation: Known map and locations and approach table.
- Speech: Say.
- HRI: Hability to clasify shelves and objects.

## Score sheet

| Action | Score |
| ---- | ---- |
| **Main Goal** | |
| Navigating to the table | 15 |
| Perceiving object and categorizing it correctly | 5×15 | 
| Picking up an object for transportation to the cabinet | 5×50 |
| Perceiving objects in shelf and saying on which layer the currently handled object should be placed | 5×15 |
| Placing an object in the cabinet | 5×15 |
| Placing an object next to similar objects on the cabinet | 5×50 |
| **Bonus Rewards** | |
| Opening the cabinet door without human help | 200 |
| Picking up a tiny object | 70 |
| Placing a tiny object | 30 |
| Picking up a heavy object | 70 |
| Placing a heavy object | 30 |
| **Deus Ex Machina Penalties** | |
| A human handing an object over to the robot | 5×–50 |
| A human placing an object in the cabinet | 5×–15 |
| A human placing an object in the cabinet next to similar objects | 5×–50 |
| A human pointing at a target location | 5×–25 |
| **Special Penalties & Bonuses** | |
| Not attending (see sec. 3.9.1) | –500 |
| Using alternative start signal (see sec. 3.7.8) | –100 |
| Outstanding performance (see sec. 3.9.3) | 114 | 
| **Total Score (excluding special penalties & standard bonuses)** | 1140 |

![Storing Groceries](-assets/tasks/StoringGroceries.png)