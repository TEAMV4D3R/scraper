import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import csv

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding": "gzip, deflate",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"}


class Scraper:

    def __init__(self, url=None):
        self.url = url

    def scrape_url_indeed(url, job_title, location):

        URL = url

        options = Options()
        options.add_argument("start-maximized")
        driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=options)

        driver.get(URL)

        time.sleep(3)
        driver.find_element('xpath',
                            '//*[@id="text-input-what"]').send_keys(job_title)
        time.sleep(3)
        where = driver.find_element('xpath',
                            '//*[@id="text-input-where"]')

        time.sleep(6)
        where.send_keys(Keys.BACK_SPACE)
        where.send_keys(Keys.BACK_SPACE)
        where.send_keys(Keys.BACK_SPACE)
        where.send_keys(Keys.BACK_SPACE)
        where.send_keys(Keys.BACK_SPACE)
        where.send_keys(Keys.BACK_SPACE)
        where.send_keys(Keys.BACK_SPACE)
        where.send_keys(Keys.BACK_SPACE)
        where.send_keys(Keys.BACK_SPACE)
        where.send_keys(Keys.BACK_SPACE)
        where.send_keys(Keys.BACK_SPACE)
        where.send_keys(Keys.BACK_SPACE)
        where.send_keys(Keys.BACK_SPACE)
        where.send_keys(Keys.BACK_SPACE)
        where.send_keys(location)
        # driver.find_element('xpath',
        #                     '//*[@id="text-input-where"]').send_keys(Keys.CONTROL + "a", Keys.BACKSPACE, location)
        time.sleep(6)
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

        content = driver.page_source

        content = BeautifulSoup(content, "lxml")

        driver.close()

        jobs_list = []
        for post in content.select('.job_seen_beacon'):
            # print("post start here ====>>   ", post)
            l = post.select(".jcs-JobTitle")[0].get("href")

            print("post", l)
            try:
                data = {
                    "job_title": post.select('.jobTitle')[0].get_text().strip(),
                    "company": post.select('.companyName')[0].get_text().strip(),
                    "rating": post.select('.ratingNumber')[0].get_text().strip(),
                    "location": post.select('.companyLocation')[0].get_text().strip(),
                    "date": post.select('.date')[0].get_text().strip(),
                    "job_desc": post.select('.job-snippet')[0].get_text().strip(),
                    "url": post.select(".jcs-JobTitle")[0].get("href")

                }
            except IndexError:
                continue
            jobs_list.append(data)

        length = len(pd.DataFrame(jobs_list))

        for x in range(length):
            scraped_data = {
                "position": pd.DataFrame(jobs_list).iloc[x]['job_title'],
                "location": " ".join(pd.DataFrame(jobs_list).iloc[x]['location'].split(" ")[:2]),
                "company": pd.DataFrame(jobs_list).iloc[x]['company'],
                "url": f"www.indeed.com{pd.DataFrame(jobs_list).iloc[x]['url']}"
            }

            url = 'https://allscrapedjobs.herokuapp.com/api/v1/scraped_jobs/'

            res = requests.post(url, json=scraped_data)
            time.sleep(3)

            return res.text


    def load_csv():
        us_cities = []
        file = open('us_cities.csv')
        csvreader = csv.reader(file)
        for row in csvreader:
            us_cities.append(" ".join(row))
        return us_cities


if __name__ == "__main__":
    s = Scraper
    for city in s.load_csv():
        print(city)
        current_url = s.scrape_url_indeed(
            'https://www.indeed.com/', 'Software', city)
        df_ = s.scrape_job_details(current_url)
        print(df_)

