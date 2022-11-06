import random
import re
from bs4 import BeautifulSoup
import requests
from django import shortcuts
from datetime import datetime
from unite_religions.religions import Christianity, Islam, Sikhism

def index(request):
    Sikhism(request).sri_guru_granth_sahib()
    return shortcuts.render(request, "index.html")

def reader(request):

    if random.randint(1, 2) == 1:
        ret = Christianity(request).bible()
    else:
        ret = Islam(request).quran()

    return ret