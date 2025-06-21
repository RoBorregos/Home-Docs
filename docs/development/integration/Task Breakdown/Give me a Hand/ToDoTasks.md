# To Do Tasks - Give me a Hand

# Section 1: Approaching & Pick

## Manipulation & Vision
- Approaching a human hand -> 50x5 points
    - Scoresheet states to approach a human's hand, so it is assumed the human will first hand the item close to the robot and then we can ask for them to hand it over
  
# Manipulation & Mechanics & Electronics
- Detect an object in the robot's gripper. 5x100 points
    - It will be considered a Deus Ex Machina if the robot tells the human when to leave the object in the gripper, such as counting down to 0. We have to detect the object in the robot and then warn the used that we will pick it up. We lose 75 points if the robot has to use Deus Ex Machina.
    - We need a working sensor to detect the object in the gripper.

# Section 2: Conversation & Place 

## HRI
- Conversational node -> 5x50 points
    - Receives the robot's knowledge of the environment as in GPSR
    - Has to *initiate* conversation, and get their attention.
    - Has to continue conversation until an unambiguous placement location is obtained -> a place location + description e.g. "<besides> the <apple>", "<on> the <yellow table>", "<in> the <shelf>"
    - Has to be able to ask for clarification if the location is not clear

## Vision
- Has to infer visual queues as to which position the object should be placed in
    - If a human is pointing left, right, up.... it may be able to provide this extra information to the conversational node, connected with the estimated locations the person may be aiming at. E.g. if the robot is aiming right and this is the direction of a table and the kitchen, we can assume the person is pointing at either of them. Should this connection be addressed here or in HRI? Either way, to accomplish this a connection with the map and its semantic information is needed.

## Manipulation
- A list of instructions that can be added to the place task:
    - Place on 
    - Place to the left of
    - Place to the right of
    - Place in front of
    - Place behind
    -  Place on top of
    -  ...
- Execute place tasks with said added instructions -> 5x100 points

## Integration
- We have to connect the instruction to real world objects, either by searching for them or connecting to the map's locations.
    - If instruction is "<besides> the <apple>", we have to find the apple in the map and then place the object next to it.
    - If instruction is "<on> the <yellow table>", we may already know which table that is from mapped locations.
    - If instruction is "<in> the <shelf>", shelf is expected to be a mapped location too.
- It is necessary to address additional ambiguities that may show up on execution. For example, we can leave the conversation with the instruction to place the object "<inside> the <green bin> in the <kitchen table>", but the robot may encounter two green bins on this place. We should be capable to ask for clarification.