import logging
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from .models import PlantsInfo  # Django 데이터베이스 모델

# 로거 설정
logger = logging.getLogger(__name__)

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

    # 식물 정보 크롤링하여 딕셔너리에 저장
    plant_info = {
        "name": html2.select_one('div.basic-information-prefer-name').get_text(strip=True) if html2.select_one('div.basic-information-prefer-name') else "정보 없음",
        "engname": html2.select_one('div.basic-information-latin-name').get_text(strip=True) if html2.select_one('div.basic-information-latin-name') else "정보 없음",
        "lifespan": html2.select('div.plant-info-field-item-text')[0].get_text(strip=True) if len(html2.select('div.plant-info-field-item-text')) > 0 else "정보 없음",
        "species": html2.select('div.plant-info-field-item-text')[1].get_text(strip=True) if len(html2.select('div.plant-info-field-item-text')) > 1 else "정보 없음",
        "cultivation_season": html2.select('div.plant-info-field-item-text')[2].get_text(strip=True) if len(html2.select('div.plant-info-field-item-text')) > 2 else "정보 없음",
        "blooming_season": html2.select('div.plant-info-field-item-text')[3].get_text(strip=True) if len(html2.select('div.plant-info-field-item-text')) > 3 else "정보 없음",
        "harvesting_season": html2.select('div.plant-info-field-item-text')[4].get_text(strip=True) if len(html2.select('div.plant-info-field-item-text')) > 4 else "정보 없음",
        "temperature": html2.select('div.plant-info-field-item-text')[10].get_text(strip=True) if len(html2.select('div.plant-info-field-item-text')) > 10 else "정보 없음",
        "sunlight": html2.select('div.basic-information-item-content-title')[1].get_text(strip=True) if len(html2.select('div.basic-information-item-content-title')) > 1 else "정보 없음",
        "watering_frequency": html2.select('div.basic-information-item-content-title')[0].get_text(strip=True) if len(html2.select('div.basic-information-item-content-title')) > 0 else "정보 없음",
        "pests_diseases": ", ".join([item.get_text(strip=True) for item in html2.select('div.diseases-basic-information-title')[:4]]) if len(html2.select('div.diseases-basic-information-title')) > 0 else "정보 없음"
    }

    # 크롤링한 정보를 데이터베이스에 저장
    plant_info_db = PlantsInfo(
        name=plant_info['name'],
        engname=plant_info['engname'],
        lifespan=plant_info['lifespan'],
        species=plant_info['species'],
        cultivation_season=plant_info['cultivation_season'],
        blooming_season=plant_info['blooming_season'],
        harvesting_season=plant_info['harvesting_season'],
        temperature=plant_info['temperature'],
        sunlight=plant_info['sunlight'],
        watering_frequency=plant_info['watering_frequency'],
        pests_diseases=plant_info['pests_diseases']
    )

    try:
        plant_info_db.save()  # 데이터베이스에 저장
        logger.info(f"Plant '{plant_name}' data scraped and saved to database.")
        return plant_info  # 저장한 정보를 반환
    except Exception as e:
        logger.error(f"Error saving plant info to database: {e}")
        return None
