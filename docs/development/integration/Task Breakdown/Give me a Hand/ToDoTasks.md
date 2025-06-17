# To Do Tasks - Give me a Hand

# HRI
- Conversational node
    - Receives the robot's knowledge of the environment as in GPSR
    - Has to continue conversation until an unambiguous placement location is obtained -> a place location + description e.g. "<besides> the <apple>", "<on> the <table>", "<in> the <shelf>"
    - Has to be able to ask for clarification if the location is not clear

# Vision
- Has to infer visual queues as to which position the object should be placed in
    - If a human is pointing left, right, up.... it may be able to provide this extra information to the conversational node, connected with the estimated locations the person may be aiming at. E.g. if the robot is aiming right and this is the direction of a table and the kitchen, we can assume the person is pointing at either of them.

# Manipulation
- A list of instructions that can be added to the place task:
    - Place on 
    - Place to the left of
    - Place to the right of
    - Place in front of
    - Place behind
    -  Place on top of
    -  ...
- Execute place tasks with said added instructions