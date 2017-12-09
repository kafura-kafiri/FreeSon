'''
wat if no tag
'''

import requests
import os
from bs4 import BeautifulSoup
from config import v, tags
from crud.defaults import video
from youtube_dl import YoutubeDL
from datetime import datetime
import random
import math


SEED, GREEN, RIPE, SEEN = range(4)
base_url = 'https://www.xvideos.com'
parser = 'html.parser'
ftp_dir = 'home/pouria/Downloads/FreeSon/'


def download(video):
    # name with id.mp
    path = os.path.join(ftp_dir, str(video['_id']) + '.mp4')
    ydl = YoutubeDL({
        'output': ftp_dir
    })
    ydl.download([video['x']])
    video.ftp = 'http://104.236.232.10:8080/FreeSon' + str(video['_id']) + '.mp4'
    video.type = RIPE
    v.save(video)


def get_tag(name):
    tag = tags.find_one({'title': name})
    if tag:
        return tag
    else:
        from crud.defaults import tag as tag_default
        tag = tag_default.copy()
        tag['title'] = name
        tag['_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        tags.insert_one(tag)
        return tag


def pull_data(video):
    content = requests.get(video['x']).content
    soup = BeautifulSoup(content, 'html.parser')
    video['title'] = soup.select('head title')[0].text
    _tags = soup.select('div.video-tags-list ul li a')
    video['tags'] = [get_tag(_tag.text)['_id'] for _tag in _tags if _tag.text != '+']
    video['type'] = GREEN
    v.save(video)


def search(tags, page=0, cnt=0): # auto append to v if bellow 3 page 2
    params = {
        'k': '+'.join([tag['title'] for tag in tags]),
        'p': str(page)
    }
    content = requests.get(base_url, params=params).content
    soup = BeautifulSoup(content, 'html.parser')
    links = [element['href'] for element in soup.select('div.thumb a')]
    links = [link for link in links if '/video' in link]
    for link in links:
        if '/video' == link[:6]:
            link = base_url + link
        print(link)
        _video = video.copy()
        _video['x'] = link
        try:
            v.insert_one(_video)
            cnt += 1
        except:
            print('wow it worked')
    if cnt > 2:
        return
    search(tags, page + 1, cnt)


def random_tags():
    _tags = tags.find()
    _tags = sorted(_tags, key=lambda x: -weight(x))
    _tags = _tags[:20]
    if len(_tags) < 5:
        return _tags
    return random.sample(_tags, 5)


def best():  # best GREEN # used
    return max(v.find({'type': GREEN}), key=lambda x: score(x))


def weight(tag):
    w = tag['weight']
    update_date = datetime.strptime(tag['_date'], '%Y-%m-%d %H:%M:%S.%f')
    now = datetime.now()
    diff = now - update_date
    diff = diff.total_seconds()
    diff += math.e
    diff = math.log(diff)
    return w / diff

def update_weight(tag):
    tag.weight = weight(tag) + 1
    tag._date = datetime.now()
    tags.save(tag)


def score(video):
    s = 0
    n = len(video['tags'])
    for tag in video['tags']:
        s += weight(tags.find_one({'_id': tag}))
    return s / n


def task():
    while v.find({'type': SEED}).count() < 30:
        search(random_tags())

    while v.find({'type': GREEN}).count() < 30:
        pull_data(v.find_one({'type': SEED}))

    while v.find({'type': RIPE}).count() < 30:
        download(best())

task()