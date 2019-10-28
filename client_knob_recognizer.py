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
	sio.emit('init', data={'data': 'r', 'action': 'w'})
	client_connected = True
	print('I\'m connected!')
	sio.start_background_task(runRecognizer)

@sio.event
def disconnect():
	global client_connected
	client_connected = False
	sio.disconnect()
	print('I\'m disconnected!')
	sys.exit(0)

@sio.on('data')
def on_data(data):
	global x, y, z, invalidate

	print data

	x = data['x']
	y = data['y']
	z = data['z']
	invalidate = True

##########################################################################################
# reading data and sending it

x = 0
y = 0
z = 0
invalidate = False

def runRecognizer():
	global invalidate

	while client_connected:
		if invalidate:
			if x > 0.3 and x < 0.6:
				sio.emit('data', data={'t': time.time(), 'action': 'enable'})
			else:
				sio.emit('data', data={'t': time.time(), 'action': 'disable'})

			if y > 0.1:
				sio.emit('data', data={'t': time.time(), 'action': 'left'})
			elif y < -0.1:
				sio.emit('data', data={'t': time.time(), 'action': 'right'})

			invalidate = False

##########################################################################################
# start app

if __name__ == '__main__':
	sio.connect('http://localhost:5000')
	sio.wait()
