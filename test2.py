from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import re
import time

option = webdriver.ChromeOptions()
option.add_argument('lang=ko_KR')
option.add_argument('--no-sandbox')
option.add_argument('--disable-dev-shm-usage')
option.add_argument('disable-gpu')
option.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36")
driver = webdriver.Chrome('./chromedriver', options = option)
driver.implicitly_wait(10)

url = f'https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open=2022&page=1'  # 페이지
driver.get(url)  # url앞의 url 받기
time.sleep(0.01)

#첫번째 영화 찾아가서
driver.find_element_by_xpath(f'// *[ @ id = "old_content"] / ul / li[1] / a').click()
#리뷰는 li[6] 아닌애가 있었다.. 그냥 넘길까.. 감동의 나날뿐일까..?ㅋㅋㅋㅋ
# ul id="movieEndTabMenu" li의 a의 title='리뷰
tabName = driver.find_element_by_id('movieEndTabMenu')
aList = tabName.find_elements_by_tag_name('a')
for l in aList:
    if l.text == '리뷰':
        l.click()
        // *[ @ id = "pagerTagAnchor1"]


# driver.close()
# driver.find_element_by_xpath('//*[@id="movieEndTabMenu"]/li[6]/a').click()