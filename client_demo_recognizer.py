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
	global sliding_window, invalidate

	print data
	sliding_window += 1

##########################################################################################
# reading data and sending it

sliding_window = 0

def runRecognizer():
	prev_sliding_window = 0

	while client_connected:
		if not prev_sliding_window == sliding_window:
			if sliding_window % 10 == 0:
				prev_sliding_window = sliding_window
				sio.emit('data', data={'t': time.time(), 'classification': sliding_window})

##########################################################################################
# start app

if __name__ == '__main__':
	sio.connect('http://localhost:5000')
	sio.wait()
