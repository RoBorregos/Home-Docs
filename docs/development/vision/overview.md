# Node Overview

## General Nodes

### Object Detector (Trained Model) - Emi
- Objects specified in the rulebook  
- Objects given in competition  

### Object Detector (Meta) - Joce
- Potentially new objects (other tools)  

### Object Detector (3D)

### Face Recognition
- Recognize known faces  
- Save new face  

### Person Tracker - Ale
- Single tracker (track one person)  
  - By toggle  
  - By pose/gesture/pose  
- Multi tracker (keep track of multiple people)  

---

## Task-Specific Nodes

### GPSR - Danae
- gpsr_commands
    - Count by gestures, poses, clothes, colors
    - Count by objects
    - Find pose/gesture/name of person
    - Publish bbox of gestures, poses, clothes, colors
- *Face recognition*  
- *Person tracking* (trigger by gestures, poses, clothes, colors, name) 

### Carry My Luggage
- carry_commands 
    - Pointing detection (pending) 
    - Bag detection  
- *Person tracking*  

### Receptionist (done)
- receptionist_commands
    - Seat detection  
    - Person detection  
- *Face recognition*  

### Storing Groceries
- groceries_commands
    - Shelf detection (each level bbox)  
- *Object detector 2D*  
- *Object detector 3D* 

### Restaurant - Yair
- restaurant_commands
    - Customer detection (waving)  
- *Object detection*  
- *Person tracking* (trigger by waving)

---

## Utils (Classes)

### Pose/Gesture/Clothes Detector - Gil
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

 
