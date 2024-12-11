# General Purpose Serivce Robot

## Previous related work

- GPSR wiki by Adán: https://github.com/RoBorregos/home/wiki/TMR-@HOME-2024

## Description

The robot is asked to understand and execute commands requiring a wide range of different
abilities

`Main Goal`: Execute 3 commands requested by the operator.

`Optional Goals`: Understand a command given by a non-expert operator

## Possible points

| **Category**                    | **Action**                                                                       | **Score** |
| ------------------------------- | -------------------------------------------------------------------------------- | --------- |
| **Regular Rewards**             | Executing the task associated with each command                                  | 3×400     |
| **Bonus Rewards**               | Understanding a command given by a non-expert operator                           | 3×100     |
| **Deus ex Machina Penalties**   | Using a custom operator                                                          | 3×–50     |
|                                 | Bypassing speech recognition                                                     | 3×–50     |
|                                 | Instructing a human to perform parts of the task will apply a percentage penalty | 3×–400    |
| **Special Penalties & Bonuses** | Not attending (see sec. 3.9.1)                                                   | –500      |
|                                 | Using alternative start signal (see sec. 3.7.8)                                  | –100      |
|                                 | Outstanding performance (see sec. 3.9.3)                                         | 200       |
| **Total**                       | Total Score (excluding special penalties & standard bonuses)                     | 1500      |

## Command generator

### Source

The commands are generated using: `https://github.com/johaq/CommandGenerator`

This repository contains examples including names, objects, and locations: `https://github.com/johaq/CompetitionTemplate`.

### Types of commands

The commands are divided into:

```bash
'1': Any command,
'2': Command without manipulation,
'3': Command with manipulation,
'4': Batch of three commands,
'5': Generate EGPSR setup,
'0': Generate QR code,
```

Some examples of commands are:

```bash
Bring me a milk from the sink
Take a knife from the kitchen table and deliver it to me
Follow the person raising their left arm at the desk lamp
Greet the person wearing a white coat in the kitchen and follow them to the pantry
Find a coffee grounds in the kitchen then get it and give it to the lying person in the kitchen
Locate a dish in the bedroom then grasp it and deliver it to me
Tell me what is the thinnest object on the storage rack
Follow the sitting person in the bedroom
Find an orange juice in the bedroom then grasp it and bring it to the standing person in the bedroom
Tell me how many persons raising their left arm are in the office
Tell me what is the biggest cleaning supply on the sink
Go to the office then find the standing person and answer a question
Tell me how many cleaning supplies there are on the tv stand
Meet Charlie at the armchair then look for them in the kitchen
Navigate to the storage rack then find the person pointing to the left and follow them
Guide the person raising their left arm from the storage rack to the bedroom
Go to the living room then find an apple and get it and give it to the lying person in the office
Tell me the pose of the person in the bedroom
Greet the person wearing a red blouse in the kitchen and follow them
```

### Understanding the command generator

The script divides the commands in 2 categories: HRI & people perception, and object manipulation & perception. Unless one category is specified, any command can be generated at [random](https://github.com/johaq/CommandGenerator/blob/master/gpsr_commands.py#L104).

For each command, the script generates a command with placeholders that contain names, locations, verbs, connectors, among others. The script then replaces these placeholders with random values from the lists in the `CompetitionTemplate` repository. The lists in the verb dictionary and the preposition dictionary are built-in the script, but other values (e.g. names, locations, objects) can be dinamically loaded.

Some commands are a combination of a start command + one or more follow up command.

The following are all the commands available:

```bash
# HRI and people perception commands
        person_cmd_list = ["goToLoc", "findPrsInRoom", "meetPrsAtBeac", "countPrsInRoom", "tellPrsInfoInLoc",
                           "talkInfoToGestPrsInRoom", "answerToGestPrsInRoom", "followNameFromBeacToRoom",
                           "guideNameFromBeacToBeac", "guidePrsFromBeacToBeac", "guideClothPrsFromBeacToBeac",
                           "greetClothDscInRm", "greetNameInRm", "meetNameAtLocThenFindInRm", "countClothPrsInRoom",
                           "tellPrsInfoAtLocToPrsAtLoc", "followPrsAtLoc"]
        # Object manipulation and perception commands
        object_cmd_list = ["goToLoc", "takeObjFromPlcmt", "findObjInRoom", "countObjOnPlcmt", "tellObjPropOnPlcmt",
                           "bringMeObjFromPlcmt", "tellCatPropOnPlcmt"]
```

### Breaking down each command

1. `goToLoc`: The robot is asked to navigate to a specific location and interact with people or an object. The command has a start command up to 2 follow up commands.

#### Start command

`command_string`:"{go | navigate} to the {loc_room | (select either location or room)} then " + `follow up command`

Steps:
| Action | Status |
| -------- | ---------- |
| Understand location | ✔️ |
| Navigate to location | ✔️ |

#### Follow up command

There are 3 options for a follow up command: `findPrs`, `findObj`, `meetName`.

##### `findPrs`

self.generate_command_followup("atLoc", {people | objects})

command_string = "{find | locate | look for} the {either gesture or pose} and" either:

- {tell | say} {"something about yourself" | "the time" | "what day is today" | "what day is tomorrow" | "your teams name" | "your teams country" | "your teams affiliation" |"the day of the week" | "the day of the month"}
- {answer} a {quiz | question} -> the quiz or questions aren't specified, so the robot can answer anything
- {follow} them.
- {follow} them to {loc or room}.
- {guide | escort | take | lead} them to {loc or room}.

##### `meetName`

command_string = "{meet} the {loaded name} and" same as findPrs:

##### `findObj`

command_string = "{find | locate | look for} the {object or single_category} and {take | get | grasp | fetch} and " (self.generate_command_followup("hasObj")) either:

- {place | put} it on the {placement loc | differs from first location}.
- {deliver | give} it to {person speaking}.
- {bring | give | deliver} it to the {gesture or pose} in the {room}"
- {deliver | give} it to the {name} in the {room}"

2. `takeObjFromPlcmt`: The robot is asked to navigate to take an object form a location to another and perform an action.

- The follow up action (self.generate_command_followup("hasObj")) are the same as the follow up for `findObj` discussed above.

3. `findPrsInRoom`: The robot is asked to find a person in a room and perform an action.

- The actions performed are the same as the follow up for `findPrs` discussed above. It seems to be equivalent to `goToLoc` but with the location specified syntactically differently.

4. `findObjInRoom`: The robot is asked to find an object in a room and perform an action. The action is the same as `findObj` discussed above.

5. `meetPrsAtBeac`: The robot is asked to meet a person at a location and perform an action. The action is the same as the follow up of `findPrs` discussed above.

6. `countObjOnPlcmt`: The robot is asked to count objects on a placement.

```bash
{tell me how many} {'drinks', 'fruits', 'snacks', 'foods', 'dishes', 'toys', 'cleaning supplies'} there are on the {location}
```

7. `countPrsInRoom`: The robot is asked to count people in a room that have a particular gesture or pose.

```bash
{tell me how many} {posture or gesture} are in the {room}"
```

8. `tellPrsInfoInLoc`: The robot is asked to tell information about people in a location.

```bash
{tell} me the {name | pose | gesture} of the person in the {room or loc}
```

9. `tellObjPropOnPlcmt`: The robot is asked to tell information about objects on a placement.

```bash
{tell} me the what is the {"biggest" | "largest" | "smallest" | "heaviest" | "lightest" | "thinnest"} object on the {placement location}
```

10. `talkInfoToGestPrsInRoom`: The robot is asked to tell information to a specific person in a room.

```bash
{tell | say} {"something about yourself" | "the time" | "what day is today" | "what day is tomorrow" | "your teams name" |"your teams country" | "your teams affiliation" | "the day of the week" | "the day of the month"} to the {gesture person} in the {room}
```

11. `answerToGestPrsInRoom`: The robot is asked to answer a question to a specific person in a room.

```bash
{answer} the {"question" | "quiz"} of the {gesture person} in the {room}"
```

12. `followNameFromBeacToRoom`: The robot is asked to follow a person from a location to another.

```bash
{follow} {name} from the {loc} to the {room}
```

13. `guideNameFromBeacToBeac`: The robot is asked to guide a person from a location to another.

```bash
{guide} {name} from the {loc} to the {room or room 2}
```

14. `guidePrsFromBeacToBeac`: Same as `guideNameFromBeacToBeac` but with a person. Identify the person either with a gesture or pose.

15. `guideClothPrsFromBeacToBeac`: Same as `guideNameFromBeacToBeac` but with a person. Identify the person with a cloth description (clothe + color).

16. `bringMeObjFromPlcmt`: The robot is asked to bring an object from a placement to the person giving the instruction.

17. `tellCatPropOnPlcmt`: Similar to `tellObjPropOnPlcmt` but with a category of objects.

18. `greetClothDscInRm`: Greet person by cloth and then follow up. The follow up is the same as `findPrs`.

19. `greetNameInRm`: Greet person by name and then follow up. The follow up is the same as `findPrs`.

20. `meetNameAtLocThenFindInRm`: Meet a person at a location and then find them in a room.

21. `countClothPrsInRoom`: Count people in a room by cloth description.

22. `tellPrsInfoAtLocToPrsAtLoc`: Tell information about a person at a location to a person at another location.

23. `followPrsAtLoc`: Follow a person at a location. Identify by either gesture or pose and found in a specified room.

## Tasks per Area

### Vision

- Save names and associate with persons.
- Be able to recall previous persons
- Save gestures and poses and associate with persons
- Be able to identify the following gestures and poses:

```bash
# Gestures
["waving person", "person raising their left arm", "person raising their right arm" "person pointing to the left", "person pointing to the right"]

# Poses
["sitting person", "standing person", "lying person"]
```

- Be able to identify the following clothes and colors:

```bash
color_list = ["blue", "yellow", "black", "white", "red", "orange", "gray"]
clothe_list = ["t shirt", "shirt", "blouse", "sweater", "coat", "jacket"]
```

### Navigation

- Follow persons
- Guide persons (go to x while making sure person follows)
- Go to locations
- General obstacle avoidance

### HRI

- Recognize and remember person asking the question
- Understand commands
- Find someone by name
- Answer questions related to this context:

```
{"something about yourself" | "the time" | "what day is today" | "what day is tomorrow" | "your teams name" | "your teams country" | "your teams affiliation" |"the day of the week" | "the day of the month"}
```

- Answer generic questions or quizzes
- Interpret objects by category and properties

### Manipulation

- Pick and place or give to a person the objects that appear in the rulebook.
- Some of the objects are:

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
