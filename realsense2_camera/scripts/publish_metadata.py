#!/usr/bin/env python
import os
import sys
import rospy
from realsense2_camera.msg import Metadata
import json
from geometry_msgs.msg import Vector3Stamped
from math import floor

class MetadataHandler():
    def __init__(self, topic):
        self._depth_sub = rospy.Subscriber(topic, Metadata, self._metadata_cb)
        self._delays_pub = rospy.Publisher('~delays', Vector3Stamped,
                                           queue_size=1)

    def _metadata_cb(self, msg):
        aa = json.loads(msg.json_data)
        os.system('clear')
        print('header:', msg.header)
        print('\n'.join(['%10s:%-10s' % (key, str(value)) for key, value in aa.items()]))
        hw_timestamp      = 0.001*aa['hw_timestamp']
        frame_timestamp   = 0.001*aa['frame_timestamp']
        backend_timestamp = 0.001*aa['backend_timestamp']
        time_of_arrival   = 0.001*aa['time_of_arrival']

        delays = Vector3Stamped(header=msg.header)
        d = backend_timestamp - frame_timestamp
        delays.vector.x = d - floor(d)
        delays.vector.y = time_of_arrival - backend_timestamp
        delays.vector.z = msg.header.stamp.to_sec() - backend_timestamp
        self._delays_pub.publish(delays)

if __name__ == '__main__':
    if len(sys.argv) < 2 or '--help' in sys.argv or '/?' in sys.argv:
        print ('USAGE:')
        print('publish_metadata.py <topic>')
        print('Demo for listening on given metadata topic.')
        print('App subscribes on given topic')
        print('App then prints metadata from messages')
        print('')
        print('Example: echo_metadata.py /camera/depth/metadata')
        print('')
        exit(-1)

    topic = sys.argv[1]

    rospy.init_node('metadata_tester', anonymous=True)
    handler = MetadataHandler(topic)
    rospy.spin()
