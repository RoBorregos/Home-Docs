# Node Overview

## General Nodes

### Object Detector (Trained Model) 
- Objects specified in the rulebook  
- Objects given in competition  

### Object Detector (Meta)
- Potentially new objects (other tools)  

### Object Detector (3D)

### Face Recognition
- Recognize known faces  
- Save new face  

### Person Tracker
- Single tracker (track one person)  
  - By toggle  
  - By pose/gesture/pose  
- Multi tracker (keep track of multiple people)  

---

## Task-Specific Nodes

### GPSR
- gpsr_commands
    - Person counting  
    - Object counting  
- *Face recognition*  
- *Person tracking*  

### Carry My Luggage
- carry_commands 
    - Pointing detection  
    - Bag detection  
- *Person tracking*  

### Receptionist
- receptionist_commands
    - Seat detection  
    - Person detection  
- *Face recognition*  

### Breakfast
- Object detector 2D  
- Object detector 3D  

### Storing Groceries
- groceries_commands
    - List objects (moondream)  
- *Object detector 2D*  
- *Object detector 3D* 

### Stickler for the Rules
- stickler_commands
    - Trash detection  
    - Shoes on/off detection  
    - Cups/drinks detection  
    - Person detection  
- *Person tracking*  

### Restaurant
- restaurant_commands
    - Customer detection (waving)  
- *Object detection*  
- *Person tracking*  

---

## Utils (Classes)

### Pose/Gesture/Clothes Detector 
- Given an image with a person, return:  
  - Pose  
  - Gesture  
  - Clothes and color  
- Given an image with a person, return:  
  - Is visible (is chest visible)  
  - Center of the person (chest)  
  - Angle of the person  

### Moondream2 Wrapper 
- Given a prompt and an image, return the output  
- Check fastest way to import moondream (ollama, transformers, etc)  

---

## Details

### Gestures
- "waving person"  
- "person raising their left arm"  
- "person raising their right arm"  
- "person pointing to the left"  
- "person pointing to the right"  

### Poses
- "sitting person"  
- "standing person"  
- "lying person"  

### Types of Clothes
- "t-shirt"  
- "shirt"  
- "blouse"  
- "sweater"  
- "coat"  
- "jacket"  

### Colors
- "blue"  
- "yellow"  
- "black"  
- "white"  
- "red"  
- "orange"  
- "gray"  
