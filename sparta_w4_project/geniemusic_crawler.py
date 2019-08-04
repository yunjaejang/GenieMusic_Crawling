import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20190715',headers=headers)

client=  MongoClient('localhost',27017)
db = client.dbsparta

soup = BeautifulSoup(data.text, 'html.parser')

musics = soup.select('#body-content > div.newest-list > div.music-list-wrap > table > tbody > tr')

for music in musics:
    rank = music.find('td', {'class': 'number'}).text[0:2].strip('\n')
    title = music.select_one('td.info > a.title.ellipsis').text.strip()
    singer = music.select_one('td.info > a.artist.ellipsis').text.strip()
    data = {'순위' :  rank, '곡 제목' : title, '가수' : singer}
    db.geniemusic.insert_one(data)


