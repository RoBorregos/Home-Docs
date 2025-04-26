# Functions for GPSR

Every command can have 2 arguments: the characterisitc and the complement. The complement contains very valuable information of the command, and the characteristic often specifices more details. However, both the complement and the characteristic are not always needed.
Many commands involve the interaction of several areas. For such tasks, the idea would be to extend the genric task to implement the interactions.

# Single Areas
## Nav
### go (complement='location to go')
	- purpose: navigate to a location
	- pseudocode: go to predefined loc (nav)

## Manipulation
### pick(complement = "object to pick", characteristic = "")
	- purpose: pick an object
    - preconditions: assumes robot is at a picking spot, and that the object is on the picking spot
    - behaviour: picks the object from the picking spot.
    - postconditions: robot has the object.
    - pseudocode: pick object (manipulation)

### place(complement = "", characteristic = "")
    - purpose: place an object in a location
    - preconditions: have an object, be in front of the placing location
    - behaviour: places an object if possible
    - postconditions: robot is in front of the placing location, without an object
    - pseudocode: place()

## HRI
### contextual_say(complement = "complete command", characteristic = "previous command" | "information to answer")
    - purpose: Say something grounded on the information known to the robot, which can include the results of previous executions, robot information, and general knowledge information.
    - preconditions: Have the available information in the database.
    - behaviour: If the name of a command is specified, fetch the execution results of the last command and generate the response. Uses the complete command to elaborate a response. After generated, say the response. 
    - postconditions: none
    - pseudocode: say(llm_response(complement, fetch_info(characteristic)))

### ask_answer_question(complement = "", characteristic = "")
    - purpose: answer the user's question.
    - preconditions: be in front of the user.
    - behaviour: Ask a question, then confirm question, finally say the answer to the question
    - postconditions: none
    - pseudocode: while get_question(): if confirm_question(): answer_question()

## Vision
### visual_info(complement = "biggest" | "largest" | "smallest" | "heaviest" | "lightest" | "thinnest", characteristic = object_category | "object")
    - purpose: get some information about an image.
    - preconditions: have the camera located in the needed position to get the frame.
    - behaviour: Get the requested data. Consider the characteristic as a filter.
    - postconditions: robot saves the specified information.
    - pseudocode: return get_info(complement)

# Multiple Areas

## HRI, Manipulation 
### give(complement = "", characteristic = "")
    - purpose: give an object to a person
    - preconditions: have an object, be in front of a person
    - behaviour: gives an object to a person. Confirms if person has grabbed the object before releasing
    - postconditions: robot is in front of a person, without an object
    - pseudocode: move_arm(giving_location), if await confirmation(user_grabbing_object): gripper(open), move_arm(standard_position) 


## HRI, Nav
### follow_person_until(complement = room | location | 'canceled', characteristic = name | "")
    - purpose: follow a person until a specific condition is triggered.
    - preconditions: robot is in front of the person it will follow
    - behaviour: if complement is a location, follow the person until it arrives to the location. If complement is 'canceled', it will follow the person until the person cancels the follow. The characteristic 
        may include the name of a person. In such case, it could be used to improve the interaction with the person.
    - postconditions: the robot is in the room where the user canceled the operation or in the target room.
    - pseudocode: while not_in_room() or not_canceled(): follow_person()

### guide_to(complement = "person" | name, characteristic = loc_room)
    - purpose: guide a person to a target location.
    - preconditions: the robot is in front of the person. If a name is specified, the robot already knows the name and face of the person.
    - behaviour: The robot expresses its intent and the goes to location. (stretch) ocasionally, the robot confirms the user is following it.
    - postconditions: the robot is in the target location, as well as the guided person
    - pseudocode: say(intent), go(characteristic)


## HRI, Vision 
### find_person_info(complement = "name" | "pose" | "gesture", characteristic = "")
    - purpose: get some information about a person.
    - preconditions: be in front of the person.
    - behaviour: If complement is a pose or gesture, the information is computed by the robot on its own. If the complement is "name" fetch the name from previous known names, or interact with the person if the name is not known.
    - postconditions: robot saves the specified information about the person.
    - pseudocode: if (complement == 'gesture' || complement == 'posture) return visual_info(complement) else return get_person_name()

## Nav, Vision
### find_object(complement = "placement location" | "room", characteristic = "object to find")
    - purpose: find an object in a place, and approach it for a pick
    - preconditions: assumes robot is at a location
    - behaviour: if it is a placement location, find object only on the placement. If complement is a room, go to all the placements in the location and search for the object. After the object
        is found, approach the object to a position where the robot can pick the object.
    - postconditions: robot is at a location where it can pick the object.
    - pseudocode: for location in room, go to location (nav). If object in location (vision), approach object for picking (nav)

## Manipulation, Vision
### count(complement = "placement location" | "room", characteristic = "object" | "person with cloth + color" | "person with posture" | "person with gesture")
    - purpose: Compute the amount of a specific target to later communicate it to a person.
    - preconditions: assumes robot is at a location
    - behaviour: If a placement is given, count the number of the item. If a room is given, gaze at several non-overlapping points and return the sum of the target across the several pictures.
    - postconditions: count result saved in memory
    - pseudocode: for degree in [-45, 0, 45], gaze(degree), total_count += count_in_frame(characteristic), return total_count

## Manipulation, Nav, Vision
### find_person(complement = "gesture" | "posture" | "cloth with color" | "", characteristic = "clothes" | "gesture" | "posture" | "")
    - purpose: find a person and approach it for further interaction. Further interaction may be: following the person, guiding the person, interacting with the person, describing the person, give an object to a person.
    - preconditions: assumes robot is at a location
    - behaviour: robot identifies a person with the specified complement, and approaches the person. If no complement is specified, only tries to find any person. The characteristic is only passed
        to the method in case it could help the function distinguish the types of modules to invoke.
    - postconditions: robot approaches the person for further interaction
    - pseudocode: for degree in [-45, 0, 45], gaze(degree), if person(complement, characteristic): approach_person(complement, characteristic), else: deus_machina()


## HRI, Manipulation, Nav, Vision
### find_person_by_name(complement = "name", characteristic = "")
    - purpose: find a person, approach it to interact, and save its information for further interactions. Further interaction may be: following the person, guiding the person, interacting with the person, describing the person, give an object to a person. Also, mention the name of the person found if it was known or unkown.
    - preconditions: assumes robot is at a location
    - behaviour: robot keeps searching for a specific person in the room until found. For each person, it checks if it's already saved, if it's not known the name is asked and saved.
    - postconditions: robot approaches the person with the specified name, and also saves all the people it finds.
    - pseudocode: for degree in [-45, 0, 45], gaze(degree), if person: approach_person() and if get_person_name() == "name": exit, elif retrie > max_retries: deus_machina()

