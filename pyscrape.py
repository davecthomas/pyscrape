from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup

from datetime import datetime
import webbrowser
import random

def get_available_products_urls(url):
    list_product_urls = []
    req = Request(url,headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    pagesoup = soup(webpage, "html.parser")
    # Luckily, this css class is only present in the case there are no search results
    p = pagesoup.find("p", class_="note-msg")
    if p is None:
        # text = p.renderContents().decode("utf-8")
        # if (text.find('returned zero result') != -1):
        print("Alledgedly found products, clicking in to check further...")
        list_product_urls = get_products_in_stock(pagesoup)
    return list_product_urls

def get_products_in_stock(pagesoup):
    a_s = pagesoup.find_all('a', {'class': 'product-image'})
    list_urls = []
    for a in a_s:
        if a.has_attr('href'):
            a_href = a['href']
            if a_href is not None and len(a_href)>0:
                # print("Checking for products here: {}".format(a_href))
                req_product = Request(a_href,headers={'User-Agent': 'Mozilla/5.0'})
                webpage_product = urlopen(req_product).read()
                pagesoup_product = soup(webpage_product, "html.parser")
                d = pagesoup_product.find("button", title="Notify Me")
                if d is None:
                    list_urls.append(a_href)
    return list_urls

list_shopping = [
    # {
    #     "url": "https://www.roguefitness.com/weightlifting-bars-plates/barbells/mens-20kg-barbells?baruse[0]=multipurpose&is_salable[0]=0",
    #     "name": "test"
    # },
    {
        "url": "https://www.roguefitness.com/weightlifting-bars-plates/barbells?bardiameter2[0]=29mm&baruse[0]=multipurpose&is_salable[0]=1",
        "name": "barbells"
    },
    {
        "url": "https://www.roguefitness.com/weightlifting-bars-plates/bumpers?bumpertype[0]=multipurpose&bumpertype[1]=training&bumperweighttype2[0]=lb&cat3[0]=bumperplates_id_4683&is_salable[0]=1&manufacturer[0]=roguefitness",
        "name": "plates"
    }
]
len_list = len(list_shopping)

dict_config = {
    "sleep_minutes_per_iteration": 30,
    "sleep_seconds_per_product": 20,
    "random_timeout_variety": 20,
    "start_hour": 4,
    "end_hour": 17,
    "shopping_closed_retry_minutes": 15,
    "shopping_hours_override" : False
}

import time
print("\nLet's go shopping at Rogue Fitness!\n")

while True:
    sleep_minutes_per_iteration_rand = dict_config["sleep_minutes_per_iteration"] + round(random.random()*dict_config["random_timeout_variety"], 1)
    sleep_seconds_per_product_rand = dict_config["sleep_seconds_per_product"] + round(random.random()*dict_config["random_timeout_variety"], 1)
    hour = datetime.now().hour
    if dict_config["shopping_hours_override"] or (hour >= dict_config["start_hour"] and hour < dict_config["end_hour"]):
        for idx, product_dict in enumerate(list_shopping):
            print("Looking for {} on {}".format(product_dict["name"], datetime.now().strftime("%A %B %d %H:%M:%S")), flush=True)
            product_urls = get_available_products_urls(product_dict["url"])
            if len(product_urls) > 0:
                print ("\n\a\a\a\a\a\a\a\a{} found!\nOpening {} product pages".format(product_dict["name"], len(product_urls)), flush=True)
                for product_url in product_urls:
                    webbrowser.open(product_url)
            else:
                print ("No {} in stock ".format(product_dict["name"]))
            if idx < len_list-1:
                print("\nHanging back for {} seconds\n".format(sleep_seconds_per_product_rand), flush=True)
                time.sleep(sleep_seconds_per_product_rand)
        print("\nChecking again in {} minutes...\n".format(sleep_minutes_per_iteration_rand), flush=True)
        time.sleep(sleep_minutes_per_iteration_rand * 60)

    else:
        if hour >= dict_config["end_hour"]:
            retry_sleep_hours = (24-hour + dict_config["start_hour"])
        else:
            retry_sleep_hours = dict_config["start_hour"]-hour
        print("Not shopping unless the time is between {}:00 and {}:00 hours. Checking again in {} hours".format(
            dict_config["start_hour"], dict_config["end_hour"], retry_sleep_hours))
        time.sleep(retry_sleep_hours*60*60)
