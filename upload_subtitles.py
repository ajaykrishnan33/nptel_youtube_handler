#!/usr/bin/python

# Usage example:
# python captions.py --videoid='<video_id>' --name='<name>' --file='<file>' --language='<language>' --action='action'

import httplib2
import os
import sys
import csv

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

CSV_FILE = "./videos.csv"

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains

# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the {{ Google Cloud Console }} at
# {{ https://cloud.google.com/console }}.
# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
CLIENT_SECRETS_FILE = "client_secret.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
YOUTUBE_READ_WRITE_SSL_SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0
To make this sample run you will need to populate the client_secrets.json file
found at:
   %s
with information from the APIs Console
https://console.developers.google.com
For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

# Authorize the request and store authorization credentials.
def get_authenticated_service():
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_READ_WRITE_SSL_SCOPE,
    message=MISSING_CLIENT_SECRETS_MESSAGE)

    storage = Storage("%s-oauth2.json" % sys.argv[0])
    credentials = storage.get()

    credentials = run_flow(flow, storage, None)

      # Trusted testers can download this discovery document from the developers page
      # and it should be in the same directory with the code.
    return build(API_SERVICE_NAME, API_VERSION, http=credentials.authorize(httplib2.Http()))


# Call the API's captions.list method to list the existing caption tracks.
def list_captions(youtube, video_id):
    results = youtube.captions().list(
        part="snippet",
        videoId=video_id
    ).execute()

    for item in results["items"]:
        id = item["id"]
        name = item["snippet"]["name"]
        language = item["snippet"]["language"]

    return results["items"]


# Call the API's captions.insert method to upload a caption track.
def upload_caption(youtube, video_id, language, name, file):
    insert_result = youtube.captions().insert(
        part="snippet",
        body=dict(
            snippet=dict(
                videoId=video_id,
                language=language,
                name=name,
                isDraft=False
            )
        ),
        media_body=file
    ).execute()

    id = insert_result["id"]
    name = insert_result["snippet"]["name"]
    language = insert_result["snippet"]["language"]
    status = insert_result["snippet"]["status"]
    print "Uploaded caption track '%s(%s) in '%s' language, '%s' status." % (name,
      id, language, status)
    return id


# If a new binary file is present, update the track with the file.
def update_caption(youtube, caption_id, file):
    update_result = youtube.captions().update(
        part="snippet",
        body=dict(
            id=caption_id,
            snippet=dict(
                isDraft=False
            )
        ),
        media_body=file
    ).execute()

    name = update_result["snippet"]["name"]
    if file:
        print "Updated the track " + name + " with the new uploaded file."


if __name__ == "__main__":

    # argparser.add_argument('--data', help='location of data file')
    argparser.add_argument('--folder', help='location of transcript files')
    args = argparser.parse_args()

    youtube = get_authenticated_service()
    try:
        with open(CSV_FILE, 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                transcript_file = row[2].strip()
                if transcript_file == "None":
                    continue
                video_id = row[0]
                caption_list = list_captions(youtube, video_id)
                if len(caption_list)==0:
                    upload_caption(youtube, video_id, "en", 'NPTEL Official', os.path.join(args.folder, transcript_file))
                elif len(caption_list)==1:
                    update_caption(youtube, caption_list[0]["id"], os.path.join(args.folder, transcript_file))

    except HttpError, e:
        print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
    else:
        print "Created and managed caption tracks."