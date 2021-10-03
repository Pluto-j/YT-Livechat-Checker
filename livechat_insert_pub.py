#!/usr/bin/python

# 使い方：パラメータ１つ目　Youtubeの「枠ID」（URLのWatch〜の部分）
# パラメータ２つ目　書き込む内容

import pickle
import json
import os
import sys

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from googleapiclient.errors import HttpError

CLIENT_SECRETS_FILE = 'client_secret.json'
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
SCOPES = ["https://www.googleapis.com/auth/youtube",
          "https://www.googleapis.com/auth/youtube.force-ssl"]

# ↓にAPIキーを記述する
YOUTUBE_API_KEY = ''

# MISSING_CLIENT_SECRETS_MESSAGE  =   """
# Warning : Please Configure OAuth2.0
# """ %   os.path.abspath(os.path.join(os.path.dirname(__file__),
#        CLIENT_SECRETS_FILE))


def get_authenticated_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle',    'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle',    'wb') as token:
            pickle.dump(creds,  token)

    return build(API_SERVICE_NAME, API_VERSION,
                 developerKey=YOUTUBE_API_KEY,
                 credentials=creds)


def YouTubeLiveChatDetail(youtube,  stream_id):
    details = youtube.videos().list(
        part='liveStreamingDetails',
        id=stream_id
    ).execute()
    detailitems = details['items'][0]
    streamdetails = detailitems['liveStreamingDetails']
    activeLiveChatID = streamdetails['activeLiveChatId']

    return activeLiveChatID


def YouTubeLiveChatSend(youtube,    livechat,   send_message):
    request = youtube.liveChatMessages().insert(
        part='snippet',
        body=dict(
            snippet=dict(
                liveChatId=livechat,
                type='textMessageEvent',
                textMessageDetails=dict(
                    messageText=send_message
                )
            )
        )
    ).execute()
    return request


if __name__ == "__main__":
    args = sys.argv
    STREAM_ID = args[1]
    SEND_MESSAGE = args[2]

    youtube = get_authenticated_service()
    activeLiveChat = YouTubeLiveChatDetail(youtube,  STREAM_ID)

    print('Stream ID: ', STREAM_ID,  'ActiveLiveChatID --> ',   activeLiveChat)
    print('Message : ', SEND_MESSAGE)

    response = YouTubeLiveChatSend(youtube,    activeLiveChat, SEND_MESSAGE)

    print('Stream ID : ',    STREAM_ID,  '\n')
    print('LiveChat ID : ', activeLiveChat, '\n')
    print('Message : ', SEND_MESSAGE,   '\n')
    print('\n')
    print('Result : ',  response,   '\n')
