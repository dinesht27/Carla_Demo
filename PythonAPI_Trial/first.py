#!/usr/bin/env python

# Copyright (c) 2020 Computer Vision Center (CVC) at the Universitat Autonoma de
# Barcelona (UAB).
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

"""
Part1 - Introduction to Carla
"""

import glob
import os
import sys
import cv2
import random
import matplotlib.pyplot as plt 
import time
import numpy as np 
import argparse

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass 
	
import carla

def main():
	actorList = []
	try:
	
		client = carla.Client('localhost', 2000) 
		client.set_timeout(10.0)
		world = client.load_world('Town03') # this is to load different maps 
		#print(client.get_available_maps()) # this if you want to view maps 
		# Creating the object
		blueprintLibrary = world.get_blueprint_library() # taking in the blueprint lib
		vechicle_bp = blueprintLibrary.filter('cybertruck')[0] # Cyberpunk inspired haha
		transform = carla.Transform(carla.Location(x = 130,y = 195, z = 40), carla.Rotation(yaw=180)) # providing the location
		vechicle = world.spawn_actor(vechicle_bp, transform)
		actorList.append(vechicle)
		
		# Camera for taking snap and saving in a folder 
		camera_bp = blueprintLibrary.find('sensor.camera.rgb')
		camera_bp.set_attribute('image_size_x','800') # the picture size 
		camera_bp.set_attribute('image_size_y','600')
		camera_bp.set_attribute('fov','90') # fov = field of view 90deg
		camera_transform = carla.Transform(carla.Location(x=1.5,z=2.4))
		camera = world.spawn_actor(camera_bp,camera_transform,attach_to=vechicle)
		camera.listen(lambda image: image.save_to_disk('output/%d064.png'%image.frame))
		
		
		# Creating multiple vehicles 
		transform.rotation.yaw = 180
		for _ in range(0,2):
			transform.location.y+=8.0
			bp = blueprintLibrary.filter('cybertruck')[0]
			npc = world.try_spawn_actor(bp, transform)
		# Checking for npc is running 	
			if npc is not None:
				actorList.append(npc)
				npc.set_autopilot = True
				print('created%s'%npc.type_id)
				
		time.sleep(15)
	finally:
		print('del actorList')
		#destroying the object
		client.apply_batch([carla.command.DestroyActor(x) for x in actorList])
		#client.ApplyBatch([carla.command.DestroyActor(x) for x in actorList])
if __name__ == "__main__":
	main()