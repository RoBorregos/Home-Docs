# Tasks 

## Stage 1
### Receptionist
The receptionist task requires the robot to receive a person from the entrance of the door, introduce itself and obtain the name and favorite drink. Then, the robot should guide the person to the living room, introducing them to a guest that is already waiting there. Additionally, the robot should describe the person and then repeat the process once again for a second guest.

**Current status:**
The robot can fully perform the task, interpreting their names and favorite drinks with llms, identifying people through face recognition, describing them using a local vision-language model and navigating through the room.

### Carry my luggage
For this taks, the robot should help a person to carry a bag that they point to and then follow them through an unknown environment.

**Current status:**
Using a custom bag detection model, the robot is able to identify the bags and using computer vision algorithms for pose detection, is able to recognize the bag that is being pointed. Nonetheless, if the bags are on the floor, the robot is unable to pick them up and requires assistance to place them in the arm. Finally, the robot can follow the person using person-reidentification and __

### Storing groceries 
For this task, the robot stores groceries into a cabinet with shelves. However, objects should be placed according to their similrarity to other objects, as each shelve contains items of a category.

### GPSR (General Purpose Service Robot)
The robot is asked to understand and execute commands requiring a wide range of different abilities.

**Current status:**
The robot is able to understand and execute commands.

