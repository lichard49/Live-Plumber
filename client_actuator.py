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
	sio.emit('init', data={'action': 'r'})
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
# start app

if __name__ == '__main__':
	sio.connect('http://localhost:5000')
	sio.wait()
