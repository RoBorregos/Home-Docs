# Navigation docs

## How to run 
1- connect to roborregos_home on wifi
On your computer:
'bash'
    ssh jetson@192.168.31.161

Inside jetson nano the schema of repos
    repo with main branch = /home/jetson/home2
    repo for development  = /home/jetson/home_development

!!WARNING!! 
only use development to change any value and commit and push after using the repo
we dont want to lose progress
Dont change main repo to another branch which is not main, we need a stable repo for the jetson

- Compiling our basics
We dont have to build all the repository because we only want to use 
-Navigation packages 
-Description packages

Recommendation only build nav_main sllidar_ros2 frida_description
How to build
- Development
'bash'
cd /home/jetson/home_development
colcon build --packages-select nav_main sllidar_ros2 frida_description
source install/setup.bash

- Main repo
'bash'
cd /home/jetson/home2
colcon build --packages-select nav_main sllidar_ros2 frida_description
source install/setup.bash

## Running lidar_vi
1- Compile the repository on jetson nano
run following command on jetson
'bash'
ros2 launch nav_main pr


--to be completed