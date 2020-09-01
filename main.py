#-*- coding:utf-8 -*-
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import json
import os
import datetime

chrome_options = Options()
chrome_options.add_argument("--headless")
chrdir = "./chromedriver.exe"
driver = webdriver.Chrome(chrdir, chrome_options=chrome_options)# 
driver.get("https://www.twitch.tv/dkwl025/videos?filter=archives&sort=time")
html = driver.find_element_by_css_selector("html")
for _ in range(5):
    time.sleep(2)
    html.send_keys(Keys.END)

soup=BeautifulSoup(driver.page_source, 'lxml')
driver.quit()

print("창 종료")

title = soup.find_all('h3', class_="tw-ellipsis tw-font-size-5")
for i in range(len(title)):
    title[i] = title[i].text
img = soup.select("div.preview-card-thumbnail__image img")
streamDate = []
m3u8Src = []
link = {}
for i in img:
    src = str(i['src'])
    m3u8Src.append("https://vod-secure.twitch.tv/"+src.replace('https://static-cdn.jtvnw.net/cf_vods/d2nvs31859zcd8/', "").replace('//thumb/thumb0-320x180.jpg', "")+"/chunked/index-dvr.m3u8")
    streamDate.append(i['title'])

for i in range(len(title)):
    link[streamDate[i]] = {}
    link[streamDate[i]]['title'] = title[i]
    link[streamDate[i]]['link'] = m3u8Src[i]

print("영상이 총 {}개 검색 되었습니다. 아래 목록에서 영상을 골라주세요".format(len(title)+1))
for i in range(len(title)):
    print(str(i+1)+". " + "{} 방송".format(streamDate[i]))
    if i%3 == 0 and i != 0:
        print('\n')

select = int(input(">")) - 1
print(m3u8Src[select])
# title = streamDate[select] + " " + title[select]
# title = title.rstrip().replace(" ", "_")

# dir_ = input("다운받을 폴더 위치 > ")

# print("youtube-dl -o {}/{}.mp4 {}".format(dir_, title, m3u8Src[select]))

# if os.path.isdir(dir_):
#     os.system("youtube-dl -o {}{}.mp4 {}".format(dir_, title, m3u8Src[select]))
now = datetime.datetime.now()
with open('./'+str(now.month)+str(now.day)+'.json', 'w', encoding='utf-8') as make_file:
    json.dump(link, make_file, indent="\t", ensure_ascii=False)