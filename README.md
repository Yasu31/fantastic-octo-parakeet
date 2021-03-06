# Mini Mobile Manipulator
storage for Individual Projects(自主プロ) at UTokyo

## [Progress is documented in the wiki.](https://github.com/Yasu31/fantastic-octo-parakeet/wiki)

## demo
general run-through of robot
[![](img/video1.png)](https://www.youtube.com/watch?v=AJrDMAA22wg)

pick up trash(kind of)
[![](img/video2.png)](https://www.youtube.com/watch?v=ZHt5yPhyLIU)

## documents
### final report for school project(Japanese)
[![report_image](img/report.png)](/project_submissions/mmm_jishupro_report.pdf)

## To move the robot(as of Jan.10)
* make sure to be on the same network as robot(NOT eduroam)
* For VM Ubuntu, set ROS_MASTER_URI to http://(IP of raspi):11311 inside ~/.bashrc, set robot_ip on moveit_planning_execution.launch to (IP of raspi).
* `roslaunch mmm_control robot.launch` on RasPi, which launches roscore, handles communication between Arduino, and audio, and ...
* `roslaunch mmm_moveit_config moveit_planning_execution.launch` which starts MoveIt and RVIZ.
* `rosrun image_view image_view image:=/raspicam_node/image _image_transport:=compressed` to view camera feed


![](https://github.com/Yasu31/fantastic-octo-parakeet/blob/master/img/model.jpg)

careful- the MMM currently sources the  setup file  for the ice-cream catkin_ws!

## To Move the robot (for MayFes)
* make sure to be on same network as robot
* on the computer (not RasPi), set ROS_MASTER_URI to http://(IP of raspi):11311 inside ~/.bashrc


1. Run `roslaunch mmm_control robot.launch`on the robot. This will launch the arduino connection and the camera and QR code&circle tracking nodes.
1. `python pagekite.py 5000 sub-yasu31.pagekite.me` on the PC will let it become a server for the LINE chatbot.
1. Run `python3 bot.py` the same computer that runs pagekite.py, this will start the LINE chatbot. This will publish stuff to the /command ros topic accordingly to control the robot.
1. Run `roslaunch mayfes behavior.py` (on the robot, if the communication is unstable) to start the actual behavior created for MayFes. This listens in on the /command ROS topic, and takes steps to realize that behavior.
1. run `roslaunch mayfes behavior.launch` on the PC.


### some tips(??)
I am having a hard time launching the MoveIt! stuff. As suggested on this page, I tried [sudo apt install ros-kinetic*](https://answers.ros.org/question/253506/unable-to-connect-to-move_group-action-server-pickup-within-allotted-time/). It didn't work, it may be an issue with the eduroam security settings or something. I'm pretty sure the same thing worked at home. Oh well, I deleted all the moveit stuff from my code so it's all right now.
