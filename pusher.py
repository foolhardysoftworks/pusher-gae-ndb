""" Pusher Appengine NDB Module """

import urllib
import hashlib
import time
import json
import hmac

from google.appenging.ext import ndb


class Pusher(object):

    def __init__(self, app_id=None, app_key=None, app_secret=None):
        if not isinstance(app_id, basestring):
            raise ValueError("Application identifier must be a string.")
        if not isinstance(app_key, basestring):
            raise ValueError("Application key must be a string.")
        if not isinstance(app_secret, basestring):
            raise ValueError("Application secret must be a string.")
        
        self._app_id = app_id
        self._app_key = app_key
        self._app_secret = app_secret
        self._event_path = "/apps/%s/events" % self._app_id

    def trigger(self, *args, **kwargs):
        return self.trigger_async(*args, **kwargs).get_result()

    @ndb.tasklet
    def trigger_async(self, channels=None, event_name=None, event_data=None):
        if not isinstance(channels, basestring):
            channels = [channels]
        elif isinstance(channels, (list, set, tuple)):
            for channel in channels:
                if not isinstance(channel, basestring):
                    raise ValueError(
                        "Channel must be a string or a list of strings.")
        else:
            raise ValueError("Channel must be a string or list of strings.")
        if not isinstance(event_name, basestring):
            raise ValueError("Event name must be a string.")
        if event_data is not None and not isinstance(
                event_data, [basestring, dict, list]):
            raise ValueError(
                "Event data must be a string, dictionary, or list.")

        body = json.dumps({
            'name': event_name,
            'data': event_data,
            'channels': channels,
        })
                
        query_string_mapping = [
            ('auth_key', self._app_key),
            ('auth_time', int(time.time())),
            ('auth_version', '1.0'),
            ('body_md5', hashlib.md5(body).hexdigest()),
        ]
        partial_query_string = urllib.urlencode(query_string_mapping)
        
        signature_key = "POST\n%s\n%s" % (self._event_path,
                                          partial_query_string)
        signature = hmac.new(
            self._app_secret, signature_key, hashlib.sha256).hexdigest()
        query_string_mapping.append(('auth_signature', signature))
        query_string = urllib.urlencode(query_string_mapping)
        path = '%s?%s' % (self._event_path, query_string)
        result = yield ndb.get_context().urlfetch.fetch(
            url='http://api.pusherapp.com%s' % path,
            payload=body,
            method='POST',
            headers={'Content-Type': 'application/json'},
        )
        raise ndb.Return(result)
        
