import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

# Django settings 모듈 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 's_pot.settings')
django.setup()

from sikmul.models import PlantsInfo
import requests  
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

def crawl_and_save_plant(plant_name):

    existing_plant = PlantsInfo.objects.filter(name=plant_name).first()
    if existing_plant:
        print(f"{plant_name} 데이터베이스에서 발견됨.")
        return existing_plant
    
    driver = webdriver.Chrome()
    driver.get('https://www.picturethisai.com/ko/')
    time.sleep(3)  # 페이지가 완전히 로딩되도록 3초 동안 기다림

    # 검색 버튼 클릭해 검색창 열기
    search_button = driver.find_element(By.CLASS_NAME, 'header-wrap-top-main-content-search-wrap')
    search_button.click()
    time.sleep(3)

    # 식물 이름 입력 받아 검색하기
    #plant = input('식물 이름을 입력하세요\n')
    #plant = plant_name
    search_box = driver.find_element(By.ID, 'search')
    search_box.send_keys(plant_name)
    search_box.send_keys(Keys.RETURN)  # 엔터
    time.sleep(3)

    # 현재 페이지의 HTML 가져오기 (동적)
    html_text = driver.page_source
    html = bs(html_text, 'html.parser')

    # 검색하여 나온 식물들 모두 배열에 넣기
    search_plants = html.select('div.pcsearch_contentblock_commonNames')
    search_plants_list = []
    for search_plant in search_plants:
        search_plants_list.append(search_plant.get_text().strip())

    # 사용자 입력 식물과 동일한 식물이 있는지 확인 후 인덱스 뽑기
    num = -1
    for i in search_plants_list:
        if i == plant_name:
            num = search_plants_list.index(i)
            break
    else:
        if num == -1:
            print("해당 식물이 없습니다.")
            driver.quit()
            return

    # 해당 인덱스를 가진 식물 클릭하기
    content_box = driver.find_elements(By.CLASS_NAME, 'pcsearch_contentblock_commonNames')[num]
    content_box.click()

    url = driver.current_url
    response = requests.get(url)
    response.encoding = 'utf-8'
    html2_text = response.text
    html2 = bs(html2_text, 'html.parser')

    # 크롤링하여 딕셔너리에 저장
    myplant = {
        "name": html2.select_one('div.basic-information-prefer-name').get_text().strip(),
        "nameE": html2.select_one('div.basic-information-latin-name').get_text().strip(),
        "lifespan": html2.select('div.plant-info-field-item-text')[0].get_text().strip(),
        "species": html2.select('div.plant-info-field-item-text')[1].get_text().strip(),
        "cultivation_season": html2.select('div.plant-info-field-item-text')[2].get_text().strip(),
        "blooming_season": html2.select('div.plant-info-field-item-text')[3].get_text().strip(),
        "harvesting_season": html2.select('div.plant-info-field-item-text')[4].get_text().strip(),
        "temperature": html2.select('div.plant-info-field-item-text')[10].get_text().strip(),
        "sunlight": html2.select('div.basic-information-item-content-title')[1].get_text().strip(),
        "watering_frequency": html2.select('div.basic-information-item-content-title')[0].get_text().strip(),
        "pests_and_diseases": ", ".join([values.get_text().strip() for values in html2.select('div.diseases-basic-information-title')[:4]])
    }


    # Plants 모델 인스턴스 생성 및 데이터베이스에 저장
    plant_instance = PlantsInfo(
        name=myplant["name"],
        engname=myplant["nameE"],
        lifespan=myplant["lifespan"],
        species=myplant["species"],
        cultivation_season=myplant["cultivation_season"],
        blooming_season=myplant["blooming_season"],
        harvesting_season=myplant["harvesting_season"],
        temperature=myplant["temperature"],
        sunlight=myplant["sunlight"],
        watering_frequency=myplant["watering_frequency"],
        pests_diseases=myplant["pests_and_diseases"]
    )
    plant_instance.save()

    print(f"{myplant['name']} 데이터베이스에 저장 완료.")

    driver.quit()
    return myplant