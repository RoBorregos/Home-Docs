# Tasks per area

## Manipulation

- Follow faces when interacting (restaurant, receptionist, gpsr)
- Pour milk (serving breakfast)
- Pick and place objects in table and cabinet shelves (storing groceries)
- Identify placing areas within shelves
- Pick and place or give to a person the objects that appear in the rulebook (gpsr)

```bash
gpsr_objects_example =
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

## Computer Vision

- Detect calling or waving customer (restaurant)
- Re-identify person (gpsr, help me carry my luggage, restaurant, stickler to the rules)
- Feedback to perform DEM (all)
- Associate names with persons (receptionist, gpsr)
- Associate gestures and poses with persons (gpsr)
- Detect trash in the floor (stickler to the rules)
- Detect shoes on/off (stickler to the rules)
- Detect cups / drinks (stickler to the rules)
- Idenfiy the objects specified in the rulebook (gpsr, storing groceries, restaurant)
- Identify the following gestures and poses: (gpsr)

  - Gestures: "waving person", "person raising their left arm", "person raising their right arm" "person pointing to the left", "person pointing to the right"
  - Poses: "sitting person", "standing person", "lying person"

- Identify and count the following clothing (gpsr):
  - "Types of clothes: t shirt", "shirt", "blouse", "sweater", "coat", "jacket"
  - Colors: "blue", "yellow", "black", "white", "red", "orange", "gray"

## Navigation

- Follow persons (Help me carry my luggage, gpsr).
- Guide persons [go to a destination while making sure person follows] (receptionist, gpsr).
- Save locations and navigate on request (all).
- Approach tables or places where a pick could be performed.
- Go to locations with obstacle avoidance (receptionist, gpsr, storing groceries).
- Go to unknown locations with obstacle avoidance (restaurant, Help me carry my luggage).
- Interpret item location given pose [i.e. forbidden room] (stickler to the rules).
- Idle routine to move by the arena (stickler to the rules, egpsr).

## Human Robot Interaction

- Talk
- Listen & interpret audio
- Take an order from a customer, talk, interpret objects to be served (restaurant)
- Extract information of person you are talking to (receptionist, gpsr)
- Interpret commands (gpsr)
- Interpret objects by category and properties (storing groceries, gpsr)
- Interpret shelve categories (storing groceries)
- Answer generic questions or quizzes (gpsr)
- Answer questions related to this context (gpsr):

```bash
{"something about yourself" | "the time" | "what day is today" | "what day is tomorrow" | "your teams name" | "your teams country" | "your teams affiliation" |"the day of the week" | "the day of the month"}
```
