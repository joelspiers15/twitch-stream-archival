from http.server import HTTPServer
from RequestHandler import RequestHandler
from config import *
from TwitchDLBridge import dlQueueConsumer
from TwitchApi import TwitchApi
import _thread as thread
import ssl
import sys
import logging

## Logging setup
logging.basicConfig()
logging.root.setLevel(log_level)
LOG = logging.getLogger('init')

## Haven't implemented automatic event sub management, doing it all manually through Postman
# twitchApi = TwitchApi(clientId, clientSecret)
# LOG.debug(twitchApi.getEventSubs())

## Start DL Queue consumer threads
if dlThreadCount <= 0:
    LOG.error("dlThreadCount must be greater than 0. Check your config file and use a value >0")
    exit(1)
for i in range(dlThreadCount):
    thread.start_new_thread(dlQueueConsumer, ())

## Configure server
server_address = (server_address, 443)
httpd = HTTPServer((bind_address, 443), RequestHandler)
httpd.socket = ssl.wrap_socket(httpd.socket, server_side=True, keyfile="ssl/privkey.pem", certfile="ssl/fullchain.pem")

## Start server
LOG.info("Listening for callbacks")
httpd.serve_forever()

