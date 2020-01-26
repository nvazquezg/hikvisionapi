import hikvisionapi
import hikvisionapi.System
import hikvisionapi.Streaming as Streaming
import hikvisionapi.RTSPutils
from datetime import datetime
import re
import os

server = hikvisionapi.HikVisionServer("192.168.1.239", "admin", "")

channelList = hikvisionapi.xml2dict(hikvisionapi.Streaming.getChannels(server))

if not os.path.exists("Downloads"):
    os.makedirs("Downloads")
os.chdir("Downloads")

for channel in channelList['StreamingChannelList']['StreamingChannel']:
    cid = channel['id']
    # The channel is a primary channel
    if (int(cid) % 10 == 1):
        # This makes sure that we only get today's recordings
        starttime = datetime.now().replace(
            hour=0, minute=0, second=0, microsecond=0).isoformat() + "Z"
        endtime = datetime.now().replace(
            hour=23, minute=59, second=59, microsecond=0).isoformat() + "Z"

        response = Streaming.getPastRecordingsForID(server, cid, starttime,
                                                    endtime)
        recordings = hikvisionapi.xml2dict(response)

        # If didn't have any recordings for this channel today
        if int(recordings['CMSearchResult']['numOfMatches']) == 0:
            continue

        recordinglist = recordings['CMSearchResult']['matchList']
        for recording in recordinglist['searchMatchItem']:
            url = recording['mediaSegmentDescriptor']['playbackURI']
            url = url.replace(server.host, server.hostWithAuth())
            name = re.sub(r'[-T\:Z]', '', recording['timeSpan']['startTime'])
            print("Downloading ", url, " ", name + ".mkv")
            hikvisionapi.RTSPutils.downloadRTSP(url, name + ".mkv",
                                                debug=True, force=True)
            print("Finished downloading", name + ".mkv")
