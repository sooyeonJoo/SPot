import os
## Python이 실행될 때 DJANGO_SETTINGS_MODULE이라는 환경 변수에 현재 프로젝트의 settings.py파일 경로를 등록합니다.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "s_pot.settings")
## 이제 장고를 가져와 장고 프로젝트를 사용할 수 있도록 환경을 만듭니다.
import django
django.setup()
from sikmul.models import PlantsInfo


import requests  
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.get('https://www.picturethisai.com/ko/')
time.sleep(3) # 페이지가 완전히 로딩되도록 3초 동안 기다림

# 검색 버튼 클릭해 검색창 열기
search_button = driver.find_element(By.CLASS_NAME, 'header-wrap-top-main-content-search-wrap')
search_button.click()
time.sleep(3)

# 식물 이름 입력 받아 검색하기
plant = input('식물 이름을 입력하세요\n')
search_box = driver.find_element(By.ID, 'search')
search_box.send_keys(plant)
search_box.send_keys(Keys.RETURN) # 엔터
time.sleep(3)

# 현재 페이지의 HTML 가져오기 (동적)
html_text = driver.page_source
# BeautifulSoup을 사용하여 HTML 파싱
html = bs(html_text, 'html.parser')

# 검색하여 나온 식물들 모두 배열에 넣기
search_plants = html.select('div.pcsearch_contentblock_commonNames')
search_plants_list = []
for search_plant in search_plants :
  search_plants_list.append(search_plant.get_text().strip())

# 사용자 입력 식물과 동일한 식물이 있는지 확인 후 인덱스 뽑기
num = -1 
for i in search_plants_list:
  if i == plant:
    num = search_plants_list.index(i)
    break
else:
  if num == -1:
    print("해당 식물이 없습니다.")
    exit()

# 해당 인덱스를 가진 식물 클릭하기
content_box = driver.find_elements(By.CLASS_NAME, 'pcsearch_contentblock_commonNames')[num]
content_box.click()

url = driver.current_url
# requests의 get함수 - 해당 url로부터 html이 담긴 자료 받아옴
response = requests.get(url)
response.encoding='utf-8'  
# 얻고자 하는 html 문서 담기
html2_text = response.text
# html을 잘 정리된 형태로 변환
html2 = bs(html2_text, 'html.parser')

# 크롤링하여 딕셔너리에 저장
myplant = {"name" : html2.select_one('div.basic-information-prefer-name'), 
           "nameE" : html2.select_one('div.basic-information-latin-name'),
           "lifespan" : html2.select('div.plant-info-field-item-text')[0],
           "species" : html2.select('div.plant-info-field-item-text')[1],
           "cultivation_season" : html2.select('div.plant-info-field-item-text')[2],
           "blooming_season" : html2.select('div.plant-info-field-item-text')[3], 
           "harvesting_season" : html2.select('div.plant-info-field-item-text')[4], 
           "temperature" : html2.select('div.plant-info-field-item-text')[10],
           "sunlight" : html2.select('div.basic-information-item-content-title')[1],
           "watering_frequency" : html2.select('div.basic-information-item-content-title')[0],
           "pests&diseases" : html2.select('div.diseases-basic-information-title')[:4]
          }
'''
# 딕셔너리 출력
for key, value in myplant.items() :
  if key == "pests&diseases" :
    print(key, ":", ", ".join([values.get_text().strip() for values in value]))
  else :
    print(key, ":", value.get_text().strip())


# 크롤링한 데이터 처리
myplant_data = {
    "name": myplant["name"].get_text().strip(),
    "nameE": myplant["nameE"].get_text().strip(),
    "lifespan": myplant["lifespan"].get_text().strip(),
    "species": myplant["species"].get_text().strip(),
    "cultivation_season": myplant["cultivation_season"].get_text().strip(),
    "blooming_season": myplant["blooming_season"].get_text().strip(),
    "harvesting_season": myplant["harvesting_season"].get_text().strip(),
    "temperature": myplant["temperature"].get_text().strip(),
    "sunlight": myplant["sunlight"].get_text().strip(),
    "watering_frequency": myplant["watering_frequency"].get_text().strip(),
    "pests_diseases": ", ".join([value.get_text().strip() for value in myplant["pests&diseases"]])
}

# 데이터베이스에 저장
plant_info = PlantsInfo.objects.create(**myplant_data)
print("식물 정보가 데이터베이스에 저장되었습니다.")

'''