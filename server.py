from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, emit, join_room, leave_room
from pyngrok import ngrok

##########################################################################################
# set up environment

app = Flask(__name__)
sio = SocketIO(app, always_connect=True, cors_allowed_origins='*')

# read_from/write_to maintains 'sid' => ['channel1', 'channel2', ...]
client_read_from = {} # use socket.io's room behavior to handle this
client_write_to = {}

##########################################################################################
# template rendering

@app.route('/sensor')
def sensor_page():
	return render_template('client_sensor.html', url=PUBLIC_URL, port=PORT)

@app.route('/plot')
def plot_page():
	return render_template('client_plot.html', url=PUBLIC_URL, port=PORT)

##########################################################################################
# lifecycle functions

@sio.on('connect')
def connect():
	print('connect')

@sio.on('disconnect')
def disconnect():
	print('disconnect')

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
def on_init(data):
	sid = request.sid
	for channel_name in data:
		if 'r' in data[channel_name]:
			# asking to read from this channel
			join_room(channel_name, sid=sid)
			dictSafeAdd(client_read_from, sid, channel_name)
		else:
			leave_room(channel_name, sid=sid)
			dictSafeRemove(client_read_from, sid, channel_name)

		if 'w' in data[channel_name]:
			# asking to write from this channel
			dictSafeAdd(client_write_to, sid, channel_name)
		else:
			dictSafeRemove(client_write_to, sid, channel_name)

@sio.on('data')
def on_data(data):
	sid = request.sid
	print 'RECEIVED', data
	if sid in client_write_to:
		to_channel_names = client_write_to[sid]
		for channel in to_channel_names:
			print 'SENT', data, channel, session.get(channel)
			sio.emit('data', data, room=channel)
	else:
		print 'lost data, client', sid, 'did not ask to write to any channels'

##########################################################################################
# start app

if __name__ == '__main__':
	global PORT, PUBLIC_URL

	PORT = 5000
	PUBLIC_URL = ngrok.connect(port=PORT)
	print 'online at', PUBLIC_URL
	sio.run(app)
