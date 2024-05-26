import pandas
from selenium import webdriver  # класс управления браузером
from selenium.webdriver.chrome.options import Options  # Настройки
from selenium.webdriver.common.by import By  # селекторы
from selenium.webdriver.support.ui import WebDriverWait  # класс для ожидания
from selenium.webdriver.support import expected_conditions as EC
import time
import json

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"

url = "https://www.youtube.com/@staspognali/videos"
chrome_option = Options()
chrome_option.add_argument(f'user_agent={user_agent}')
driver = webdriver.Chrome(options=chrome_option)
try:
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    time.sleep(1)
    page_height = driver.execute_script("return document.documentElement.scrollHeight")
    print(f'Initial page height:{page_height}')
    while True:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(1)
        new_size = driver.execute_script("return document.documentElement.scrollHeight")
        if new_size == page_height:
            break
        page_height = new_size
    print(f'Final page height: {page_height}')
    title_xpath = "//*[@id='video-title-link']"
    views_xpath = "//*[@id='metadata-line']/span[1]"
    age_xpath = "//*[@id='metadata-line']/span[2]"
    video_titles = driver.find_elements(By.XPATH, title_xpath)
    video_views = driver.find_elements(By.XPATH, views_xpath)
    video_age = driver.find_elements(By.XPATH, age_xpath)
    data = []
    for i in range(len(video_titles)):
        title = video_titles[i].text
        views = video_views[i].text
        age = video_age[i].text
        print(title, views, age)
        data.append({'title': title, 'views': views, 'age': age})
    with open('videos.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    df = pandas.DataFrame(data)
    df.to_csv('videos.csv')
except Exception as er:
    print(f'Error {er}')
finally:
    driver.quit()
