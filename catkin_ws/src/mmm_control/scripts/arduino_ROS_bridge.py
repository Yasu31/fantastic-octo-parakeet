#!/usr/bin/env python3
# pip3 install pyYAML
# pip3 install rospkg
# pip3 install catkin_pkg
import i2c
import rospy
import audio
from sensor_msgs.msg import JointState
corrections=[-1,1,-1,1,-1,-1,1]
def publishSensors():
    pub=rospy.Publisher('joint_states', JointState, queue_size=10)
    rospy.init_node('joint_state_publisher_a', anonymous=True)
    rate=rospy.Rate(10)
    jointState=JointState()
    audio.playSound(5)
    while not rospy.is_shutdown():
        try:
            sensorInfos=i2c.readData()
            for i in range(len(sensorInfos)):
                sensorInfos[i]*=corrections[i]
        except:
            print("error received... moving on")
        jointNames=[]
        for i in range(7):
            jointNames.append("link"+str(i)+"_link"+str(i+1)+"_joint")
        jointState.header.stamp=rospy.Time.now()
        jointState.name=jointNames
        # angles are in degrees*100. Convert to radians

        jointState.position=[i/100*3.1415/180 for i in sensorInfos]
        
        jointState.velocity=[]
        jointState.effort=[]
        pub.publish(jointState)
        rate.sleep()
if __name__ == '__main__':
    try:
        publishSensors()
    except rospy.ROSInterruptException:
        pass