import logging
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from .models import PlantsInfo  # Django 데이터베이스 모델from bs4 import BeautifulSoup

# 로거 설정
logger = logging.getLogger(__name__) #콘솔창에 흔적 남김

def crawl_and_save_plant(plant_name):
    # 크롬 웹 드라이버 실행
    driver = webdriver.Chrome()
    driver.get('https://www.picturethisai.com/ko/')
    time.sleep(3)

    # 검색 버튼 클릭
    search_button = driver.find_element(By.CLASS_NAME, 'header-wrap-top-main-content-search-wrap')
    search_button.click()
    time.sleep(3)

    # 검색 창에 식물 이름 입력
    search_box = driver.find_element(By.ID, 'search')
    search_box.send_keys(plant_name)
    search_box.send_keys(Keys.RETURN)
    time.sleep(3)

    # 페이지의 HTML 파싱
    html_text = driver.page_source
    html = bs(html_text, 'html.parser')

    # 검색된 식물 목록 추출
    search_plants = html.select('div.pcsearch_contentblock_commonNames')
    search_plants_list = [search_plant.get_text().strip() for search_plant in search_plants]

    # 검색어와 일치하는 식물 찾기
    num = -1
    for i in search_plants_list:
        if i == plant_name:
            num = search_plants_list.index(i)
            break

    # 식물이 없으면 종료
    if num == -1:
        logger.info(f"Plant '{plant_name}' not found on the website.")
        return None

    # 해당 인덱스의 식물 클릭
    content_box = driver.find_elements(By.CLASS_NAME, 'pcsearch_contentblock_commonNames')[num]
    content_box.click()

    # 상세 페이지의 HTML 파싱
    time.sleep(3)
    html2_text = driver.page_source
    html2 = bs(html2_text, 'html.parser')

    #수명이라는 텍스트가 포함된 요소 찾기
    lifespan_element = html2.find('div', class_='key-fact-text', string='수명')
    #수명 텍스트를 포함하는 부모 요소에서 정보 추출
    lifespan = "정보없음"
    if lifespan_element:
        #key-fact-content 부모요소에서 ke-fact-title 찾기
        lifespan_title = lifespan_element.find_previous_sibling('div', class_='key-fact-title')
        if lifespan_title:
            lifespan = lifespan_title.get_text(strip=True)


    sunlight_element = html2.find('div',class_='key-fact-text', string='햇빛')
    sunlight = "정보없음"
    if sunlight_element:
        sunlight_title = sunlight_element.find_previous_sibling('div', class_='key-fact-title')
        if sunlight_title:
            sunlight = sunlight_title.get_text(strip=True)


    species_element = html2.find('div',class_='key-fact-text',string='종류')
    species = "정보없음"
    if species_element:
        species_title = species_element.find_previous_sibling('div',class_='key-fact-title')
        if species_title:
            species = species_title.get_text(strip=True)


    blooming_season_element = html2.find('div',class_='key-fact-text',string='개화 시기')
    blooming_season = "정보없음"
    if blooming_season_element:
        blooming_season_title = blooming_season_element.find_previous_sibling('div',class_='key-fact-title')
        if blooming_season_title:
            blooming_season = blooming_season_title.get_text(strip=True)

    
    cultivation_season_element = html2.find('div', class_='key-fact-text',string='재배 시기')
    cultivation_season = "정보없음"
    if cultivation_season_element:
        cultiavation_season_title = cultivation_season_element.find_previous_sibling('div',class_='key-fact-title')
        if cultiavation_season_title:
            cultiavation_season = cultiavation_season_title.get_text(strip=True)

    
    harvesting_season_element = html2.find('div',class_='key-fact-text',string='수확 시기')
    harvesting_season = "정보없음"
    if harvesting_season_element:
        harvesting_season_title =  harvesting_season_element.find_previous_sibling('div',class_='key-fact-title')
        if  harvesting_season_title:
            harvesting_season =  harvesting_season_title.get_text(strip=True)

    
    watering_frequency_element = html2.find('div',class_='key-fact-text',string='물')
    watering_frequency = "정보없음"
    if watering_frequency_element:
        watering_frequency_title = watering_frequency_element.find_previous_sibling('div',class_='key-fact-title')
        if watering_frequency_title:
            watering_frequency = watering_frequency_title.get_text(strip=True)

    
    temperature_element = html2.find('div',class_='key-fact-text',string='이상적인 온도')
    temperature = "정보없음"
    if temperature_element:
        temperature_title = temperature_element.find_previous_sibling('div',class_='key-fact-title')
        if temperature_title:
            temperature = temperature_title.get_text(strip=True)

    
    pests_diseases_element = html2.find('div',class_='key-fact-text',string='독성')
    pests_diseases = "정보없음"
    if pests_diseases_element:
        pests_diseases_title = pests_diseases_element.find_previous_sibling('div',class_='key-fact-title')
        if pests_diseases_title:
            pests_diseases = pests_diseases_title.get_text(strip=True)

    image_url = "정보없음" 
    image_element = html2.find('img', class_='description-main-image')
    if image_element:
        image_url = image_element.get('src', '정보없음')


    # 정보 추출
    plant_info = {
        "name": html2.select_one('div.description-main-left-title').get_text(strip=True) if html2.select_one('div.description-main-left-title') else "정보 없음",
        "engname": html2.select_one('div.scientific-name-item-text i').get_text(strip=True) if html2.select_one('div.scientific-name-item-text i') else "정보 없음",
        "lifespan": lifespan,
        "sunlight": sunlight,  
        "species": species,    
        "blooming_season": blooming_season, 
        "cultivation_season": cultivation_season,  
        "harvesting_season": harvesting_season,  
        "watering_frequency": watering_frequency,  
        "temperature": temperature,  
        "pests_diseases": pests_diseases,  
        "image_url":image_url

    }


    # 크롤링한 정보를 데이터베이스에 저장
    plant_info_db = PlantsInfo(
        name=plant_info['name'],
        engname=plant_info['engname'],
        lifespan=plant_info['lifespan'],
        sunlight=plant_info['sunlight'],
        species=plant_info['species'],
        blooming_season=plant_info['blooming_season'],
        cultivation_season=plant_info['cultivation_season'],
        harvesting_season=plant_info['harvesting_season'],
        watering_frequency=plant_info['watering_frequency'],
        temperature=plant_info['temperature'],
        pests_diseases=plant_info['pests_diseases'],
        image_url=plant_info['image_url']
    )
    plant_info_db.save()

    driver.quit()

    logger.info(f"Plant information for '{plant_name}' has been saved")
    return plant_info

