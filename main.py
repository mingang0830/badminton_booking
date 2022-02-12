from bs4 import BeautifulSoup as bs
from selenium import webdriver

import requests
import json
import os

url = "https://yeyak.seoul.go.kr/web"
badminton_suburl = "/reservation/selectReservView.do?rsv_svc_id=S211202171022655257"
driver_path = "/home/mingyeong/chromedriver"
driver = webdriver.Chrome(driver_path)


def close_popup(driver):
    driver.get(url + badminton_suburl)
    driver.find_element_by_class_name('pop_x').click()
    return driver


def get_data():
    response = close_popup(driver)
    able_dates = response.find_elements_by_class_name("able")
    result = {}
    """
    result = {날짜 : '0/2', 날짜2: '1/2'}
    """
    for date in able_dates:
        result[int(date.text.split("\n")[0])] = date.text.split("\n")[1]
    response.close()
    return result

def send_me_via_kakaotalk(data):
    url = "https://yeyak.seoul.go.kr/web"
    template_object = {
        "object_type": "text",
        "text": str(data),
        "link": {
            "web_url": url,
            "mobile_web_url": url,
        },
        "button_title": "바로 확인"
    }
    access_token = os.getenv("ACCESS_TOKEN")
    response = requests.post("https://kapi.kakao.com/v2/api/talk/memo/default/send", 
        headers={"Authorization": f"Bearer {access_token}"},
        data={"template_object": json.dumps(template_object)})


if __name__ == "__main__":
    data = get_data()
    send_me_via_kakaotalk(data)
    print("done!")

    