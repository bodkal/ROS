#!/usr/bin/env python
from Map_compare import map_deffrent
import rospy
import numpy as np
from geometry_msgs.msg import Pose2D
from nav_msgs.msg import OccupancyGrid
from std_msgs.msg import Bool

from time import sleep
import matplotlib.pyplot as plt
import pickle
from Maps_data import MAP_A as map_b_real ,res_map


class turtlebot_move():
    def __init__(self):
        rospy.init_node('turtlebot_move', anonymous=False)
        rospy.loginfo("Press CTRL + C to terminate")

        delta = 0.05
        self.center=np.array([0.032,0])
        self.i=int(0)
        self.Gmap=0
        self.world_start = int(np.round(0.5 / delta))-2
        self.world_end = int(np.round(4.9 / delta))

        self.path_status = rospy.Subscriber("in_place", Bool, self.in_place_callback)
        self.read_goal = rospy.Subscriber("map", OccupancyGrid, self.read_goal_callback)
        self.path_pub = rospy.Publisher('goal_node', Pose2D, queue_size=10)

        self.rate = rospy.Rate(50)
        self.status=False

        rospy.sleep(1)


    def read_goal_callback(self, msg):
        self.Gmap=np.array(msg.data).reshape(msg.info.height,msg.info.width).T
        self.Gmap = self.Gmap[self.world_start:self.world_end, self.world_start:self.world_end]

    def in_place_callback(self,msg):
        self.status=msg.data

    @staticmethod
    def get_path(file_name):
        data = np.loadtxt(file_name, delimiter=" ")
        return data


if __name__ == '__main__':

    try:

        robot=turtlebot_move()
        map = map_deffrent(map_b_real,'./config/map_b_watchers.txt')

        path = turtlebot_move.get_path('./config/map_b_path.txt') # +np.ones((1,2))
        plt.imshow(map_b_real)
        plt.scatter(path[:, 1]/0.2 + 1, path[:, 0]/0.2 + 1, 40, color='orange')
        plt.show()
        next=Pose2D()

        #map_c = map_deffrent(map_b_real, res_map)
        #map_c.compare_map(map_b_real, res_map)
        #map_c.show(a=res_map, fig_num=1, show=True, seen=True)
        print(path/0.2)

        for index ,step in enumerate(path):

            next.x=step[0]
            next.y=step[1]
            whach=map.get_seen_cells(step)+np.ones((1,2))

            robot.path_pub.publish(next)
            while not robot.status:
                #print(robot.status)
                sleep(0.05)
            sleep(2)
            map.show(a=robot.Gmap, fig_num=2, show=False, seen=True)

            plt.draw()
            plt.pause(0.001)
            plt.clf()
            # map_c.show(a=map_b_real, fig_num=1, show=False, seen=True)
            map.compare_map(map_b_real, robot.Gmap,whach,path[(index+1):])
            plt.draw()
            plt.pause(0.001)
            plt.clf()
            with open(str(np.round(step[0],1))+","+str(np.round(step[1],1)), 'wb') as f:
                # Pickle the 'data' dictionary using the highest protocol available.
                pickle.dump(robot.Gmap, f, pickle.HIGHEST_PROTOCOL)
            print(robot.status)
        while not robot.status:
            print(robot.status)
            sleep(0.05)
        input()

    except rospy.ROSInterruptException:
        rospy.loginfo("Action terminated.")
        exit(0)

