# Sample Python code for user authorization

import httplib2
import os
import sys

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

try:
    os.mkdir("subtitles")
except:
    pass

OUTPUT_DIR = "./subtitles/"

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.
CLIENT_SECRETS_FILE = "client_secret.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
YOUTUBE_READ_WRITE_SSL_SCOPE = "https://www.googleapis.com/auth/youtubepartner"
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = "WARNING: Please configure OAuth 2.0"

# Authorize the request and store authorization credentials.
def get_authenticated_service(args):
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_READ_WRITE_SSL_SCOPE,
    message=MISSING_CLIENT_SECRETS_MESSAGE)

    storage = Storage("%s-oauth2.json" % sys.argv[0])
    
    credentials = run_flow(flow, storage, args)

    # Trusted testers can download this discovery document from the developers page
    # and it should be in the same directory with the code.
    return build(API_SERVICE_NAME, API_VERSION, http=credentials.authorize(httplib2.Http()))

args = argparser.parse_args()
youtube = get_authenticated_service(args)

### END BOILERPLATE CODE

# Sample python code for channels.list

def uploads_list_mine(service, **kwargs):
    results = service.channels().list(
        **kwargs
    ).execute()

    channel = results['items'][0]
    return channel["contentDetails"]["relatedPlaylists"]["uploads"]

def get_videos_list(service, uploads_list_id):
    # Retrieve the list of videos uploaded to the authenticated user's channel.
    playlistitems_list_request = service.playlistItems().list(
        playlistId=uploads_list_id,
        part="snippet",
        maxResults=50
    )

    videoIDList = []
    videoNameList = []

    while playlistitems_list_request:
        playlistitems_list_response = playlistitems_list_request.execute()

        for playlist_item in playlistitems_list_response["items"]:
            title = playlist_item["snippet"]["title"]
            video_id = playlist_item["snippet"]["resourceId"]["videoId"]
            # print "%s, %s" % (title, video_id)
            videoIDList.append(video_id)
            videoNameList.append(title)

        playlistitems_list_request = service.playlistItems().list_next(
            playlistitems_list_request, playlistitems_list_response)

    return zip(videoIDList, videoNameList)

def download_caption_for_video(service, video):
    video_id = video[0]
    title = "_".join(video[1].split(" ")) + ".srt"
    results = service.captions().list(
        part="snippet",
        videoId=video_id
    ).execute()

    caption = None
    for capt in results["items"]:
        if capt["snippet"]["name"] == "NPTEL Official":
            caption = capt
            break

    subtitle = youtube.captions().download(
        id=caption["id"],
        tfmt="srt"
    ).execute()

    with open(OUTPUT_DIR + title, "w") as f:
        f.write(subtitle)

    return title

def download_caption_for_videos(service, videos):
    for v in videos:
        try:
            title = download_caption_for_video(service, v)
            print title
        except:
            print "error at : " + v[1]


uploads_list_id = uploads_list_mine(youtube, part='snippet,contentDetails,statistics', mine=True)
videos = get_videos_list(youtube, uploads_list_id)
download_caption_for_videos(youtube, videos)
