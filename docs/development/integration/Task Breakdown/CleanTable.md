# Clean Table

## Description
Clean the table by placing drinks on the trash bin, placing tableware and cutlery in the dishwasher, and wiping the table. (10 minutes)

`Main Goal:`: Clean up all the objects on the table. Tableware and cutlery have to be placed correctly inside the dishwasher and drinks must be placed inside the trash bin.

`Optional goals`:
1. Opening the dishwasher door
2. Pulling out the dishwasher rack
3. Placing a dishwasher tab inside the dishwasher
4. Wipe the table area where the drink was

## Task Breakdown
1. Pick up each drink and place them in the trash bin. (Place potentially with deus)
2. Pick tableware (cup and potentially plate) and place them in the dishwasher with deus.
3. Attempt to wipe table?

**Points we could achieve:**

- Navigation: 15
- Pick cup, bowl and drinks: 4×50
- Autonomously picking any object: 50

Total: 265 

If we place drinks in trash bin: +150 = 415
If we pick up the tab: +100 = 515


## Possible points
| **Category** | **Action** | **Score** |
|---|---|---|
| **Main Goal** | Navigate to the table to pick up items | 15 |
| | Picking up the cup, bowl and drinks for transportation | 4×50 |
| | Picking up cutlery (spoon, fork) for transportation | 2×80 |
| | Picking up the plate for transportation | 100 |
| | Placing the tableware and cutlery inside the dishwasher | 5×50 |
| | Placing an item correctly (cleanable, convenient like a human would) in the dishwasher | 5×75 |
| | Placing a drink inside the trash bin | 2×50 |
| **Bonus Rewards** | Pulling and pushing the dishwasher rack | 2×100 |
| | Opening and closing the dishwasher door | 2×200 |
| | Picking up the dishwasher tab for transportation to the dishwasher | 100 |
| | Placing the dishwasher tab inside the dishwasher’s hatch intended for the tab | 200 |
| | Wiping the area where the drink was | 2×50 |
| | Autonomously Picking any Object | 50 |
| | Autonomously Placing any Object | 50 |
| **Deus Ex Machina Penalties** | Handing cup, bowl and drinks over to the robot | 3×–50 |
| | Handing cutlery over to the robot | 2×–80 |
| | Handing the plate over to the robot | –100 |
| | Having a human place an object in the dishwasher | 5×–50 |
| | Having a human place a drink inside the trash bin | 2×–50 |
| | A human pointing at the trash bin | 2×–25 |
| **Special Penalties & Bonuses** | Not attending (see sec. 3.9.1) | –500 |
| | Using alternative start signal (see sec. 3.7.8) | –100 |
| | Outstanding performance (see sec. 3.9.3) | 230 |
| **Total** | Total Score (excluding special penalties & standard bonuses) | 2300 |

# Tasks per Area

## Navigation

- Navigate to predefined location (table, dishwasher, trash bin)

## Vision

- Detect objects (drinks, tableware, cutlery)

## HRI

- Say 

## Manipulation

- Pick up objects (drinks, tableware --> cup, bowl, plate)
- Pick up cutlery (spoon, fork, knife)
- Place objects in the trash bin (could measure height to place?)
- Place objects in the dishwasher (probably deux)
- Optional: wipe table
- Optional: open and close dishwasher door
- Optional: pull and push dishwasher racks
- Optional: pick up dishwasher tab
- Optional: place dishwasher tab inside the dishwasher hatch

