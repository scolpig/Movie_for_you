# crawling 작업

# crawling은 각자 진행 하고 빨리 완성되는 코드로 연도를 나눠서 진행하겠습니다.
# 일단 2022년 개봉작만 진행해 주시고 저장형식은 csv로 하겠습니다.
# 나머지는 연도별로 나눠서 작업하고 합칠게요.
# 컬럼명은 ['title', 'reviews']로 통일해주세요.
# index=False 옵션으로 인덱스 없이 저장해주세요.
# 파일명은 "reviews_{}.csv".format(연도)로 해주세요.
# 크롤링한 데이터 파일은 아래 링크로 올려주세요.
# https://drive.google.com/drive/folders/1NLkgk0zSJlmNwSGq-q1qf6oBUZZLN9AK?usp=sharing

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

title_list = []
reviews_list = []
df_data = pd.DataFrame()
#영화 리스트 페이지
for p in range(1, 3):
    url = f'https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open=2022&page={p}'  # 페이지
    driver.get(url)  # url앞의 url 받기
    time.sleep(0.01)
#li는 20까지 한 페이지에 20개의 li
#각각의 영화 들어가기
#첫 페이지에 영화는 //*[@id="old_content"]/ul/li[20]/a 20개
    for l in range(1,21):
        driver.get(url)
        driver.find_element_by_xpath(f'// *[ @ id = "old_content"] / ul / li[{l}] / a').click()
        #리뷰는 li[6]
        driver.find_element_by_xpath('//*[@id="movieEndTabMenu"]/li[6]/a').click()

        #리뷰는 리뷰탭에서 한 페이지에 10개씩 60개면 range(1,7)
        for rp in range(1,7):
            try:
                driver.find_element_by_xpath('//*[@id=\"pagerTagAnchor' + str(rp) + '\"]').click()
                #2페이지로 넘어와서
                for r in range(1,11):
                    try:
                        driver.find_element_by_xpath(f'//*[@id="reviewTab"]/div/div/ul/li[{r}]/a').click()
                        time.sleep(0.1)
                        title = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[2]/div[1]/h3').text
                        # title = re.compile('[^가-힣a-zA-Z ]').sub(' ', title)
                        reviews = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[4]/div[1]/div[4]').text
                        # reviews = re.compile('[^가-힣a-zA-Z ]').sub(' ', reviews)
                        title_list.append(title)
                        reviews_list.append(reviews)
                        driver.back()
                    except NoSuchElementException:
                        print('NoSuchElementException')
                        break
            except NoSuchElementException:
                print('NoSuchElementException')
                break
df_title = pd.DataFrame(title_list, columns=['title'])  # 리스트를 dataFrame화
df_reviews = pd.DataFrame(reviews_list, columns=['reviews'])  # 리스트를 dataFrame화
df_data = pd.concat([df_data, df_title, df_reviews],
                                axis='columns', ignore_index=True)  # 만든 dataFrame 합치기, axis='columns'->옆으로 합치기
df_data.to_csv('./crawling_data/reviews_{}.csv'.format('2022'), index=False)  # index=False-> 만든 csv에 index 제거


driver.close()



