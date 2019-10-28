# Live Plumber

Simple infrastructure based on [socket.io](https://socket.io/) for making connections between services easy.  These services might be:

1. Data providers, such as sensor streams or user interactions
2. Data processing pipelines
3. Output or actuation mechanisms

The modularity of the system enables fast rapidly iterating on each component independently.

# Installation

The server is built around flask and flask-socketio:

`pip install flask flask-socketio`

In order to run the Knob example (by getting smartphone sensor data), ngrok was used.  [Make an account on ngrok](https://ngrok.com/product) and then install pyngrok, which will install the ngrok binary:

`pip install pyngrok`

For the Python-based clients, install python-socketio (the web-based clients grab the socket.io library from a CDN):

`pip install python-socketio`

# Examples

## Demo Example

Run each of these as a separate process:

```
$ python app.py
$ python client_demo_recognizer.py
$ python client_demo_plot.py
$ python client_demo_actuator.py
```

At this point, some connections will be established, but nothing will be streaming yet.  To kick things off, run the following (again as a separate process):

`python client_demo_sensor.py`

The demo sensor will simply stream some fake signals to the `data` and `compute` channels.  The demo plot script registered to listen to the `data` channel, so it prints out all of the sensor values.  The demo recognizer script, on the other hand, registered to listen to the `compute` channel, so it gets a copy of the same sensor values.  On every 10th received value, it emits a "classification" value of "NULL" to the `action` channel.  This example simply shows how different components can interact.

## Demo Example + Visualization

With everything from the demo example running, navigate to:

`0.0.0.0:5000/plot`

And you will see the live plotting of the fake signals coming from the synthetic sensor.  This addition demonstrates how Python scripts can interact with web apps through the infrastructure.

## Knob Example

The knob example presents a more realistic scenario by using the orientation sensors in a smartphone to control a virtual knob on the computer screen.  It also highlights the advantage of being able to facilitate communication between different platforms (Python scripts, web apps on desktop and mobile).  Again, run these as separate processes:

```
$ python app.py
$ python client_knob_recognizer
```

When running the main server script, a URL should have been printed:

`online at http://<UNIQUE_ID>.ngrok.io`

On your smartphone's browser, navigate to [(NOTE: sensor access with the web API is only allowed over HTTPS)](https://developers.google.com/web/updates/2017/09/sensors-for-the-web#only_https):

`https://<UNIQUE_ID>.ngrok.io/sensor`

Now on your desktop's browser, go to:

`0.0.0.0:5000/knob`

If you tilt your phone so it is mostly vertical, you should see the knob "turn on".  Then, rotate your phone clockwise or counterclockwise to twist the knob.