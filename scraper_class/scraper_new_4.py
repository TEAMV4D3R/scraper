import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding": "gzip, deflate",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"}

# class Scraper:

# def __init__(self, url=None):
#     self.url = url


def scrape_url_indeed(url, job_title, location):

    URL = url

    options = Options()
    options.add_argument("start-maximized")
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)

    driver.get(URL)

    # page = driver.page_source
    # driver.close()
    # print(page)

    time.sleep(3)
    driver.find_element('xpath',
                        '//*[@id="text-input-what"]').send_keys(job_title)
    time.sleep(3)
    driver.find_element('xpath',
                        '//*[@id="text-input-where"]').send_keys(location)
    time.sleep(3)
    driver.find_element('xpath', '/html/body/div').click()
    time.sleep(3)
    try:
        driver.find_element('xpath', '//*[@id="jobsearch"]/button').click()
    except:
        driver.find_element('xpath',
                            '//*[@id="whatWhereFormId"]/div[3]/button').click()

    current_url = driver.current_url

    return current_url


def scrape_job_details(url):

    URL = url

    options = Options()
    options.add_argument("start-maximized")
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)

    driver.get(URL)

    wait = WebDriverWait(driver, 5)

    content = driver.page_source

    content = BeautifulSoup(content, "lxml")

    driver.close()

    links = []
    while True:
        new_links = wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, ".jobtitle.turnstileLink ")))
        links.extend([l.get_attribute("href") for l in new_links])

        try:  # EC needed as otherwise the element was not clickable
            next_page = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//ul[contains(@class, 'agination')]/li[last()]/a")))
            # ActionChains is needed as Indeed opens a small window and it is needed to be closed to continue
            ActionChains(driver).move_to_element(next_page).click().perform()
        except TimeoutException:
            print("links scraped")
            break

#     jobs_list = []
#     for post in content.select('.job_seen_beacon'):
#         # print("post start here ====>>   ", post)
#         try:
#             data = {
#                 "job_title": post.select('.jobTitle')[0].get_text().strip(),
#                 "company": post.select('.companyName')[0].get_text().strip(),
#                 "rating": post.select('.ratingNumber')[0].get_text().strip(),
#                 "location": post.select('.companyLocation')[0].get_text().strip(),
#                 "date": post.select('.date')[0].get_text().strip(),
#                 "job_desc": post.select('.job-snippet')[0].get_text().strip(),
#             }
#         except IndexError:
#             continue
#         jobs_list.append(data)
#     dataframe = pd.DataFrame(jobs_list)

#     return dataframe


current_url = scrape_url_indeed(
    'https://www.indeed.com/', 'Data Scientist', 'Seattle')

df = scrape_job_details(current_url)

print(df)