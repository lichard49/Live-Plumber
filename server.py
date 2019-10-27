import eventlet
import socketio
import thread
import time

##########################################################################################
# set up environment

sio = socketio.Server(always_connect=True, cors_allowed_origins='*')
app = socketio.WSGIApp(sio, static_files={
	'/plot': 'client_plot.html'
})

# read_from/write_to maintains 'sid' => ['channel1', 'channel2', ...]
# client_read_from = {} # use socket.io's room behavior to handle this
client_write_to = {}

##########################################################################################
# lifecycle functions

@sio.event
def connect(sid, environ):
	print('connect ', sid)

@sio.event
def disconnect(sid):
	print('disconnect ', sid)

##########################################################################################
# data redirection

def dictSafeAdd(dictionary, key, value):
	if not key in dictionary:
		dictionary[key] = []
	if not value in dictionary[key]:
		dictionary[key].append(value)

def dictSafeRemove(dictionary, key, value):
	if key in dictionary and value in dictionary[key]:
		dictionary[key].remove(value)

@sio.on('init')
def on_init(sid, data):
	for channel_name in data:
		if 'r' in data[channel_name]:
			# asking to read from this channel
			sio.enter_room(sid, channel_name)
		else:
			sio.leave_room(sid, channel_name)

		if 'w' in data[channel_name]:
			# asking to write from this channel
			dictSafeAdd(client_write_to, sid, channel_name)
		else:
			dictSafeRemove(client_write_to, sid, channel_name)

@sio.on('data')
def on_data(sid, data):
	print 'RECEIVED', data
	if sid in client_write_to:
		to_channel_names = client_write_to[sid]
		for channel in to_channel_names:
			print 'SENT', data, channel
			sio.emit('data', data=data, to=channel, skip_sid=sid)
	else:
		print 'lost data, client', sid, 'did not ask to write to any channels'

##########################################################################################
# start app

if __name__ == '__main__':
	eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
