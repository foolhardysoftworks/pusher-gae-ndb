Pusher Appengine NDB Module
===========================

Synopsis
--------

This module allows you to easily trigger pusher events on multiple channels in appengine. It uses the NDB asycronous API (i.e., the urlfetch is run in a tasklet).


Installation
------------

Download pusher.py and ensure that pusher.py is in your path.


Example
-------


.. code::

   import pusher
   
   app = pusher.Pusher('my-app-id', 'my-app-key', 'my-app-secret')

   channels = ['channel_1', 'channel_2']  #  Can also be a string.
   event_data = {'message': "Hello World!"}

   result = app.trigger_async('cool_event, channels, event_data).get_result()
   

To Do
-----

Unit testing, socket id, and more than just event triggering.
   
   

