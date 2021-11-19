from http.server import HTTPServer
from RequestHandler import RequestHandler
from config import *
from TwitchDLBridge import dlQueueConsumer
from TwitchApi import TwitchApi
from datetime import datetime, timedelta, time
import _thread as thread
import ssl
import sys
import logging
import time
import os
import pause

def cleanupHandler():
    LOG.info("Old VOD cleanup started")

    # Loop through each channel in config.py and clean
    for channel in eventSubs:
        LOG.debug("Cleaning " + channel["channel"])

        # Don't clean vods if daysToKeepVods is <= 0
        if(channel["daysToKeepVods"] > 0):
            try:
                # Loop through all vods for channel
                channelDir = os.path.join(targetDLDir, channel["channel"])
                os.chdir(channelDir)
                for file in os.listdir():
                    # Figure out how old the vods are
                    curFile = os.path.join(channelDir, file)
                    t = os.stat(curFile)[8]
                    fileAge = datetime.fromtimestamp(t) - datetime.today()
                    LOG.debug(curFile + " created " + str(fileAge) + " ago")

                    # Delete old vods
                    if fileAge.days <= -channel["daysToKeepVods"]:
                        LOG.info("Deleting old VOD:\t" + curFile)
                        #os.remove(curFile)
            except Exception:
                LOG.error("Failed downloading vod for " + channel["channel"])

    LOG.info("Finished cleanup")

    # Wait till tomorrow at midnight
    pause.until(datetime.combine(datetime.now().date(), datetime.strptime("0000","%H%M").time()) + timedelta(1))

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

## Start cleanupHandler thread
thread.start_new_thread(cleanupHandler, ())

## Start server
LOG.info("Listening for callbacks")
httpd.serve_forever()



