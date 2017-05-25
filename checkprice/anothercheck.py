from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import os
import datetime
import json
# import sys


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
def get_pagesource(url):
    pagesource = None
    # driver = webdriver.Chrome(executable_path=os.path.join(BASE_DIR, 'chromedriver/chromedriver'))
    driver = webdriver.PhantomJS(executable_path=os.path.join(BASE_DIR,'phantomjs-2.1.1-macosx/bin/phantomjs'))
    driver.get(url)

    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "sh-trip-item-0-0"))
        )
        pagesource = driver.page_source
        print "Got page soure..."
    finally:
        driver.quit()
    return pagesource

def get_price(pagesource):
    bsObj = BeautifulSoup(pagesource, 'html.parser') 
    trip = bsObj.find(id="trip-0")
    trip_head = trip.find(class_='sh-trip-head')
    trip_list = trip.find(class_='sh-list-view')
    # data_list = []
    t_head = {}
    t_head['price_list'] = []
    # t_head['timestamp'] = time.time()

    for c in trip_head.children:
        t_head[c['class'][0]] = c.text

    for child in trip_list.children:
        temp = {}
        temp['intro'] = child.find(class_='sh-intro').text
        # intro = child.find(class_='sh-intro').text
        cabins = child.find(class_='cab-0')
        price = cabins.find(class_='price')
        if price:
            temp['price'] = price.text
        else:
            temp['price'] = None
        t_head['price_list'].append(temp)
    # data_list.append(t_head)
    # return data_list
    json_data = json.dumps(t_head, ensure_ascii=False, encoding = 'utf8', indent=4, sort_keys=True) + ','
    return json_data

#CAN-KIX
url = "http://b2c.csair.com/ita/intl/zh/flights?flex=1&m=1&p=200&t=CAN-KIX-20171007-20171015&egs=ITA,ITA"

#CAN-NYC

# url = "http://b2c.csair.com/ita/intl/zh/flights?flex=1&m=0&p=100&t=CAN-NYC-20171007&egs=ITA,ITA"

pagesource = get_pagesource(url)
# price =  get_price(pagesource)

if pagesource:
    # trip_prices_list.add(get_price(pagesource))
    price =  get_price(pagesource)
    if price: 
        print "Got the price..."
        check_time = datetime.datetime.strftime(datetime.datetime.now(), \
            "%Y-%m-%d-%H:%m")
        with open("{}.json".format(check_time), "w") as f:
        # try:
        #     old_price = json.loads(f)
        #     price.append(old_price)
        # except Exception:
        #     print Exception
        #     pass 
        # writeJSON = json.dumps(price,  indent=4, separators=(',', ': '))
        # f.write(writeJSON)
            f.write(price.encode('utf8'))
            print "Done!"
    else:
        print "Cannot get the price something's wrong, retry later."





