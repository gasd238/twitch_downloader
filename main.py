#-*- coding:utf-8 -*-
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import json

chrome_options = Options()
chrome_options.add_argument("--headless")
chrdir = "./chromedriver.exe"
driver = webdriver.Chrome(chrdir, chrome_options=chrome_options)# 
driver.get("https://www.twitch.tv/dkwl025/videos?filter=archives&sort=time")
html = driver.find_element_by_tag_name('html')
html.click()

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
    m3u8Src.append("https://vod-secure.twitch.tv/"+i['src'].lstrip('https://static-cdn.jtvnw.net/cf_vods/d2nvs31859zcd8/').rstrip('//thumb/thumb0-320x180.jpg')+"/chunked/index-dvr.m3u8")
    streamDate.append(i['title'])

for i in range(len(title)):
    link[streamDate[i]] = {}
    link[streamDate[i]]['title'] = title[i]
    link[streamDate[i]]['link'] = m3u8Src[i]

with open('./test.json', 'w', encoding='utf-8') as make_file:
    json.dump(link, make_file, indent="\t", ensure_ascii=False)