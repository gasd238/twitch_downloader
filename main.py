#-*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import json
import os
import datetime
import requests
import urllib
from threading import Thread
import re

with open('config.json') as json_file:
    json_data = json.load(json_file)
    client_id = json_data["client_id"]
    token = json_data["token"]

def get_StreamerId(query):
    headers = {'client-id' : client_id, 'Authorization':token}
    page = requests.get("https://api.twitch.tv/helix/search/channels?query={}".format(query), headers=headers)
    soup=BeautifulSoup(page.text, 'lxml')
    try:
        return json.loads(soup.select('p')[0].text)['data'][0]['id']
    except:
        return 0

def get_Video(streamerID):
    headers = {'client-id' : client_id, 'Authorization':token}
    page = requests.get("https://api.twitch.tv/helix/videos?user_id={}&first=100".format(str(streamerID)), headers=headers)
    soup=BeautifulSoup(page.text, 'lxml')
    return json.loads(soup.select('p')[0].text)['data']

def get_VideoUrl(query):
    streamerID = get_StreamerId(query)
    if streamerID == 0:
        print("없음")
        exit(0)
    videos = get_Video(streamerID)
    streamDate = []
    m3u8Src = []
    link = {}
    title = []
    for video in videos:
        title.append(video['title'])
        img = video['thumbnail_url']
        m3u8Src.append("https://vod-secure.twitch.tv/"+img.replace('https://static-cdn.jtvnw.net/cf_vods/d2nvs31859zcd8/', "").replace('//thumb/thumb0-%{width}x%{height}.jpg', "")+"/chunked/index-dvr.m3u8")
        streamDate.append(re.search(r'(\d+-\d+-\d+)', video['created_at']).group())

    return m3u8Src, title, streamDate

now = datetime.datetime.now()

query = input("검색할 스트리머 > ")
m3u8Src, title, streamDate = get_VideoUrl(query)
print("영상이 총 {}개 검색 되었습니다. 아래 목록에서 영상을 골라주세요".format(len(title)))
for i in range(len(title)):
    print(str(i+1)+". " + "{} {} 방송".format(streamDate[i], title[i]))
while True:
    select = input("번호 입력 > ")
    try:
        select = int(select)-1
        break
    except:
        continue
title = re.search(r'(\d+-\d+-\d+)', streamDate[select]).group() + " " + title[select]
title = title.rstrip().replace(" ", "_")
#os.system("streamlink hls://{} best -o {}.mp4".format(m3u8Src[select], title))  //다운로드용 코드
print(title+"\n"+m3u8Src[select])
