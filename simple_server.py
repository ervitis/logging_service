# -*- coding: utf-8 -*-

from __future__ import print_function
import json

import falcon


class Messages(object):

    def on_post(self, req, resp):
        message = json.loads(req.get_param('msg'))
        print('Type: %s - Message: %s' % (message['type'], message['msg']))


api = falcon.API()
api.add_route('/message', Messages())
