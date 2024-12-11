# Serve Breakfast

The robot has to set a table for breakfast for one person and prepare cereal for them.

## Main Goal: 

Place breakfast items on a table (bowl, spoon, cereal box, and milk carton) and
prepare cereal.

## Optional Goals:

1. Pour milk into the bowl
2. Place the spoon next to the bowl

## Pipeline

1. Robot outside the house
2. Door opened
3. Navigate to kitchen
4. Navigate to object default place
6. List available objects
7. Pick Cereal
8. Navigate to main table
9. Place Cereal
10. Navigate to object default place
11. Pick milk
12. Navigate to main table
13. Place milk
14. Navigate to object default place
15. Pick spoon
16. Navigate to main table
17. Place spoon
18. Pour cereal in bowl
19. Pour milk in bowl #Optional



## Possible points
| **Category**           | **Action**                                                 | **Score**   |
|-------------------------|-----------------------------------------------------------|-------------|
| **Regular Rewards**     | Initial navigation to pick up area                        | 15          |
|                         | Perceiving object and categorizing it correctly (visualize or say) | 4×15=60       |
|                         | Picking up breakfast items for transportation to the table | 4×50=200       |
|                         | Placing breakfast items on the table                      | 4×50=200        |
|                         | Pouring cereal into the bowl                              | 300         |
| **Bonus Rewards**       | Pouring milk into the bowl                                | 300         |
|                         | Placing a spoon next to the bowl                          | 100         |
| **Regular Penalties**   | Throwing or dropping an object on the table               | 4×–30=-120       |
|                         | Spilling cereal while pouring                             | -100      |
|                         | Spilling milk while pouring                               | -100      |
| **Deus ex Machina Penalties** | Pointing at an object                               | 4×–5=-20      |
|                         | Handing an object over to the robot                       | 4×–50=-200       |
|                         | A human placing an object on the table                    | 4×–50=-200      |
|                         | A human pouring cereal in the bowl                        | –300      |
| **Special Penalties & Bonuses** | Not attending (see sec. 3.9.1)                   | –500        |
|                         | Using alternative start signal (see sec. 3.7.8)          | –100        |
|                         | Outstanding performance (see sec. 3.9.3)                 | 117         |
| **Total**               | Total Score (excluding special penalties & standard bonuses) | 1175    |

## Important notes

- The maximum time for this test is 5:00 minutes.
- *Safe placing:* Objects must be placed with care, namely the robot should place rather than throw or drop objects.
- *Deus ex Machina:* The scores are reduced if human assistance is received, in particular for:
    • pointing to an object or telling the robot where an object is or where to place it
    • handing an object over to the robot
    • having a human place objects on the table
    • having a human pour cereal into the bowl
- *Furniture:*
    – Table: The robot serves breakfast on the table which is announced beforehand.
    – Chairs: Chairs may be placed around the table and won’t be removed.
    – Doors: The robot does not need to open any doors to find the breakfast items.

### THE OBJECTS CAN BE IN DIFFERENT INITIAL PLACES

## Breakdown state machine

Workflow for the task

<p align="center">
  <img src="/assets/tasks/Breakfast.png" alt="RoBorregos Logo">
</p>


## Deus Ex Machina Functionalities

Workflow for each deux ex machina approach

<p align="center">
  <img src="/assets/tasks/DEMBreakfast.png" alt="RoBorregos Logo">
</p>

## Oportunities

- Point count for tree desicion
- Time count for tree desicion
- Place and pick confirmation with visual help
- Different object placement in the main table


# Areas Work 

## Manipulation
- Planning feedback and failure status
- Pick and place service
- Motion planning to point object or place

## Vision
- Object detection with multiple options or sources
- 3d Object position for manipulation and nav feedback
- Place 3d object detection for indications
- DEM feedback

## Navigation
- Place navigation and approach table
- navigation feedback
- Object position planning

## HRI
- Visual and sound state machine feedback
- Friendly interaction


