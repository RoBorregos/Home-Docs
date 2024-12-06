# General Purpose Serivce

## Description

The robot is asked to understand and execute commands requiring a wide range of different
abilities

`Main Goal`: Execute 3 commands requested by the operator.

`Optional Goals`: Understand a command given by a non-expert operator

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
                           "countClothPrsInRoom", "tellPrsInfoAtLocToPrsAtLoc", "followPrsAtLoc"]
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

Steps:
| Action | Status |
| -------- | ---------- |
| Find people or objects | ✔️ |
| Interact with people or objects | ✔️ |

## Tasks per Area

### Vision

- Be able to identify the following gestures and poses:

```bash
# Gestures
["waving person", "person raising their left arm", "person raising their right arm" "person pointing to the left", "person pointing to the right"]

# Poses
["sitting person", "standing person", "lying person"]
```

### Navigation

- Follow persons
- Guide persons
- Go to locations
- General obstacle avoidance
