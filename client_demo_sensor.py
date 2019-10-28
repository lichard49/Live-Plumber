import eventlet
import socketio

import time
import socket
import os
import sys

##########################################################################################
# set up environment

sio = socketio.Client()
client_connected = False

##########################################################################################
# lifecycle functions

@sio.event()
def connect():
	global client_connected
	sio.emit('init', data={'data': 'w', 'compute': 'w'})
	client_connected = True
	print('I\'m connected!')

@sio.event
def disconnect():
	global client_connected
	client_connected = False
	sio.disconnect()
	print('I\'m disconnected!')
	sys.exit(0)

@sio.on('data')
def on_data(data):
	print data

##########################################################################################
# reading data and sending it

def readSensors():
	for i in xrange(1000000):
		if client_connected:
			sio.emit('data', data={'t': time.time(), 'x': i, 'y': i*2, 'z': i**2})
			# print 'send'
			sio.sleep(0.01)

##########################################################################################
# start app

if __name__ == '__main__':
	sio.connect('http://localhost:5000')
	sio.start_background_task(readSensors)
	sio.wait()
