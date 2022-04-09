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
    #1페이지에서 첫 번째 영화를 선택
    for l in range(1,21):
        driver.get(url)
        driver.find_element_by_xpath(f'// *[ @ id = "old_content"] / ul / li[{l}] / a').click()
        #리뷰는 li[6] 아닌애가 있었다.. 그냥 넘길까.. 감동의 나날뿐일까..?ㅋㅋㅋㅋ
        try:
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
                            print('페이지당리뷰가10개미만')
                            break
                except NoSuchElementException:
                    print('리뷰페이지가1개이하')
                    break
        except NoSuchElementException:
            print('리뷰탭위치이상함')
            continue
df_title = pd.DataFrame(title_list, columns=['title'])  # 리스트를 dataFrame화
df_reviews = pd.DataFrame(reviews_list, columns=['reviews'])  # 리스트를 dataFrame화
df_data = pd.concat([df_data, df_title, df_reviews],
                                axis='columns', ignore_index=True)  # 만든 dataFrame 합치기, axis='columns'->옆으로 합치기
df_data.to_csv('./crawling_data/reviews_{}.csv'.format('2022'), index=False)  # index=False-> 만든 csv에 index 제거


driver.close()


from selenium import webdriver
import pandas as pd
import time

option = webdriver.ChromeOptions()
#options.add_argument('headless')
option.add_argument('lang=ko_KR')
option.add_argument('--no-sandbox')
option.add_argument('--disable-dev-shm-usage')
option.add_argument('disable-gpu')
driver = webdriver.Chrome('./chromedriver', options=option)
driver.implicitly_wait(1)

# https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open=2022&page=1 첫 페이지
# //*[@id="old_content"]/ul/li[1]/a 영화 제목 1
# //*[@id="old_content"]/ul/li[2]/a 영화 제목 2
# //*[@id="old_content"]/ul/li[20]/a 영화 제목 20

# //*[@id="movieEndTabMenu"]/li[6]/a/em 리뷰 버튼
# //*[@id="old_content"]/div[3]/table/tbody/tr/td[2]/a 영화 페이지 버튼
# https://movie.naver.com/movie/bi/mi/review.naver?code=193794&page=2   리뷰 페이지 url

# //*[@id="reviewTab"]/div/div/ul/li[1]/a/strong 리뷰 제목 1
# //*[@id="reviewTab"]/div/div/ul/li[2]/a/strong 리뷰 제목 1

# //*[@id="content"]/div[1]/div[2]/div[1]/h3/a 영화 제목
# //*[@id="content"]/div[1]/div[4]/div[1]/div[4]리뷰
movie_page_url = 'https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open=2022&page={}'
movie_title_xpath = '//*[@id="old_content"]/ul/li[{}]/a'
review_page_url = 'https://movie.naver.com/movie/bi/mi/review.naver?code=193794&page={}'
review_tab_xpath = '//*[@id="movieEndTabMenu"]/li[{}]/a'
#//*[@id="movieEndTabMenu"]/li[{}]/a/em
#//*[@id="movieEndTabMenu"]/li[6]/a/em
review_title_xpath = '//*[@id="reviewTab"]/div/div/ul/li[{}]/a/strong'
title_xpath = '//*[@id="content"]/div[1]/div[2]/div[1]/h3/a'
review_xpath = '//*[@id="content"]/div[1]/div[4]/div[1]/div[4]'
titles = []
reviews = []

for i in range(1, 14):
    url = movie_page_url.format(i) # 영화 페이지
    for j in range(1, 21):
        try:
            try:
                driver.close()
            except:
                pass
            driver = webdriver.Chrome('./chromedriver', options=option)
            driver.implicitly_wait(1)
            print(url)
            driver.get(url)
            print('debug10')
            time.sleep(0.2)
            try:
                print('j :', j)
                driver.find_element_by_xpath(movie_title_xpath.format(j)).click() # 영화 제목 클릭
                time.sleep(0.2)
                for k in range(6, 0, -1):
                    if driver.find_element_by_xpath(review_tab_xpath.format(k)).text == '리뷰':
                        print(review_tab_xpath.format(k))
                        review_page_url = driver.find_element_by_xpath(review_tab_xpath.format(k)).get_attribute('href')
                        print(review_page_url)
                        driver.find_element_by_xpath(review_tab_xpath.format(k)).click() # 리뷰 버튼 클릭
                        time.sleep(0.2)

                        break

                for l in range(1, 7):
                    print('l :', l)
                    try:
                        print(review_page_url)
                        #driver.get(review_page_url + '&page={}'.format(l))
                        driver.find_element_by_xpath('//*[@id="pagerTagAnchor{}"]'.format(l)).click()
                        print('debug02')
                        time.sleep(0.2)
                        for k in range(1, 11):
                            try:
                                driver.find_element_by_xpath(review_title_xpath.format(k)).click() # 리뷰 제목 클릭
                                time.sleep(0.2)
                                print('k :', k)
                                try:
                                    title = driver.find_element_by_xpath(title_xpath).text
                                    title = title.replace(',', ' ')
                                    review = driver.find_element_by_xpath(review_xpath).text
                                    review = review.replace(',', ' ')
                                    titles.append(title)
                                    reviews.append(review)
                                    try:
                                        driver.back()  # 리뷰 페이지로
                                        time.sleep(0.2)
                                    except:
                                        driver.get(review_page_url.format(l))
                                        time.sleep(0.2)
                                except:
                                    try:
                                        driver.back()  # 리뷰 페이지로
                                        time.sleep(0.2)
                                    except:
                                        driver.get(review_page_url.format(l))
                                        time.sleep(0.2)

                            except:
                                print('{}페이지 {}번째 영화 리뷰 {}페이지 {}번째 리뷰 error'.format(i, j, l, k))
                                driver.back()
                                continue
                    except:
                        print('{}페이지 {}번째 영화 리뷰 {}페이지 error'.format(i, j, l))
                        #driver.get(url)
                        break
            except:
                print('{}페이지 {}번째 영화 error'.format(i, j))

        except:
            print('{}page error'.format(i))
    df = pd.DataFrame({'title':titles, 'reviews':reviews})
    print(df.tail())
    df.to_csv('./crawling_data/reviews_{}.csv'.format(2022), index=False)
driver.close()










