from crud.views import video
from config import v
from crawler import RIPE, task
from flask import render_template


def load_v(video):
    task()
    return video

@video.blue.route('/')
def home_page():
    videos = v.find({'type': RIPE})
    return render_template('video/home.html', v=videos)