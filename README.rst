Pusher Appengine NDB Module
===========================

Triggers pusher events on multiple channels in appengine. Uses the
NDB asycronous API, i.e. the urlfetch is run in a tasklet.


Example
-------


.. code::

   import pusher
   
   app = pusher.Pusher('my-app-id', 'my-app-key', 'my-app-secret')

   channels = ['channel_1', 'channel_2']  #  Can also be a string.
   event_data = {'message': "Hello World!"}

   result = app.trigger_async('cool_event, channels, event_data).get_result()
   

Notes
-----

- There is currently no support for socket IDs
   
   

