from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup

from datetime import datetime
import webbrowser
import random

def get_me_some_url_shit(txt, url):
    req = Request(url,headers={'User-Agent': 'Mozilla/5.0'})
    now = datetime.now()
    current_time = now.strftime("%A %B %d %H:%M:%S")
    print("{}".format(current_time))
    print("Looking for {}".format(txt))
    webpage = urlopen(req).read()
    pagesoup = soup(webpage, "html.parser")
    p = pagesoup.find("p", class_="note-msg")
    text = p.renderContents().decode("utf-8")
    # How to use find()
    if (text.find('returned zero result') != -1):
        print ("No {} in stock ".format(txt))
    else:
        print ("\n\a\a\a\a\a\a\a\a{} found!\n\n".format(txt))
        webbrowser.open(url)

url_barbells = "https://www.roguefitness.com/weightlifting-bars-plates/barbells?bardiameter2[0]=29mm&baruse[0]=multipurpose&is_salable[0]=1"
url_plates = "https://www.roguefitness.com/weightlifting-bars-plates/bumpers?bumpertype[0]=multipurpose&bumpertype[1]=training&bumperweighttype2[0]=lb&cat3[0]=bumperplates_id_4683&is_salable[0]=1&manufacturer[0]=roguefitness"

req_barbells = Request(url_barbells,headers={'User-Agent': 'Mozilla/5.0'})
req_plates = Request(url_plates,headers={'User-Agent': 'Mozilla/5.0'})
sleep_minutes = 40
sleep_seconds_twixt = 20

import time
starttime=time.time()
print("\nLet's go shopping at Rogue Fitness!\n\n")
while True:
    sleep_minutes_rand = sleep_minutes + round(random.random()*10, 1)
    sleep_seconds_twixt_rand = sleep_seconds_twixt + round(random.random()*10, 1)
    get_me_some_url_shit("barbells", url_barbells)
    print("\nHanging back for {} seconds\n".format(sleep_seconds_twixt_rand))
    time.sleep(sleep_seconds_twixt_rand)
    get_me_some_url_shit("plates", url_plates)

    print("Checking again in {} minutes...\n".format(sleep_minutes_rand))
    time.sleep(sleep_minutes_rand * 60)
