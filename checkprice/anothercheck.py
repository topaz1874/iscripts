from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import os
import datetime
import json
import schedule
import time
import re


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
        temp['intro'] = ' '.join(child.find(class_='sh-intro').stripped_strings)
        # intro = child.find(class_='sh-intro').text
        cabins = child.find(class_='cab-0')
        price = cabins.find(class_='price')
        if price:
            temp['price'] = price.find_next().text
        else:
            temp['price'] = None
        t_head['price_list'].append(temp)
    # data_list.append(t_head)
    # return data_list
    json_data = json.dumps(t_head, ensure_ascii=False, indent=4, sort_keys=True)
    return json_data

#CAN-KIX
url = "http://b2c.csair.com/ita/intl/zh/flights?flex=1&m=1&p=200&t=CAN-KIX-2010507-20171015&egs=ITA,ITA"

#CAN-NYC

# url = "http://b2c.csair.com/ita/intl/zh/flights?flex=1&m=0&p=100&t=CAN-NYC-20171007&egs=ITA,ITA"

def main():
    pagesource = get_pagesource(url)
    # pattern = r'.+(?P<go_date>\d{8})-(?P<back_date>\d{8})'
    # m = re.match(pattern, url)
    # go_datetime = datetime.datetime.strptime(m.group('go_date'), '%Y%m%d')
    # today = datetime.date.today()
    # time_diff = go_datetime -  today > datetime.timedelta(days=1)
    if pagesource:
        price =  get_price(pagesource)
        check_time = datetime.datetime.strftime(datetime.datetime.now(), \
                "%Y-%m-%d-%H:%M")
        
        with open("{}.json".format(check_time), "w") as f:
            if price: 
                print "On {} got the price...".format(check_time)
                f.write(price.encode('utf8'))
                print "Done!"
            else:
                error_msg = "Cannot get the price something's wrong, retry later."
                f.write(error_msg)
                print error_msg

schedule.every(1).minutes.do(main)
while True:
    schedule.run_pending()
    time.sleep(1)



