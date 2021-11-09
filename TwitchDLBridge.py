import subprocess
import logging
import os
import _thread as thread, queue, time
from pathlib import Path
from config import *

LOG = logging.getLogger("TwitchDLBridge")

def downloadLatestVod(channelName):
    LOG.debug("Downloading latest vod for " + channelName)
    vodId = getLatestVodId(channelName)
    if vodId is None:
        return False
    return downloadVod(vodId, channelName)

def getLatestVodId(channelName):
    listProcess = subprocess.Popen(  ['python3', twitchDLBin, 'videos', '--limit', "1", channelName],
                                     universal_newlines=True,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE
                                 )
    stdout, stderr = listProcess.communicate()

    if not stdout:
        LOG.error("Empty stdout from twitch-dl videos, command failed to run")
        return None
    elif 'No videos found' in stdout:
        LOG.error("No videos found for channel: " + channelName)
        return None
    idKey = "https://www.twitch.tv/videos/"
    idLen = 10
    idIndex = stdout.index(idKey) + len(idKey)
    vodId = stdout[idIndex: idIndex + idLen]

    LOG.debug("Most recent VOD for " + channelName + ": " + vodId)
    return vodId



def downloadVod(vodId, channelName):
    LOG.debug("Downloading VOD: " + vodId)
    targetDir = targetDLDir + "/" + channelName
    Path(targetDir).mkdir(parents=True, exist_ok=True)
    os.chdir(targetDir)
    status = os.system('python3 ' + twitchDLBin + ' download -q source ' + vodId)

    if status == 0:
        LOG.info('Vod downloaded successfully')
    else:
        LOG.error('Vod download process returned non-success. Check logs above for details')
