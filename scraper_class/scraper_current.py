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

        # resp = requests.get(url, headers=HEADERS)
        # content = BeautifulSoup(resp.content, "html.parser")

        # print(content)

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
            try:
                data = {
                    "job_title": post.select('.jobTitle')[0].get_text().strip(),
                    "company": post.select('.companyName')[0].get_text().strip(),
                    "rating": post.select('.ratingNumber')[0].get_text().strip(),
                    "location": post.select('.companyLocation')[0].get_text().strip(),
                    "date": post.select('.date')[0].get_text().strip(),
                    "job_desc": post.select('.job-snippet')[0].get_text().strip(),
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
                "url": "www.indeed.com"
            }

            url = 'https://allscrapedjobs.herokuapp.com/api/v1/scraped_jobs/'

            x = requests.post(url, json=scraped_data)

        return x.text


if __name__ == "__main__":

    current_url = Scraper.scrape_url_indeed(
        'https://www.indeed.com/', 'Software', 'Seattle, WA')
    df_Seattle = Scraper.scrape_job_details(current_url)

    current_url = Scraper.scrape_url_indeed(
        'https://www.indeed.com/', 'Software', 'Portland, OR')
    df_Portland = Scraper.scrape_job_details(current_url)

    current_url = Scraper.scrape_url_indeed(
        'https://www.indeed.com/', 'Software', 'Chicago, IL')
    df_Chicago = Scraper.scrape_job_details(current_url)

    current_url = Scraper.scrape_url_indeed(
        'https://www.indeed.com/', 'Software', 'New York')
    df_New_York = Scraper.scrape_job_details(current_url)

    current_url = Scraper.scrape_url_indeed(
        'https://www.indeed.com/', 'Software', 'San Francisco')
    df_San_Francisco = Scraper.scrape_job_details(current_url)

    current_url = Scraper.scrape_url_indeed(
        'https://www.indeed.com/', 'Software', 'Los Angeles')
    df_Los_Angeles = Scraper.scrape_job_details(current_url)

    current_url = Scraper.scrape_url_indeed(
        'https://www.indeed.com/', 'Software', 'Miami, FL')
    df_Miami = Scraper.scrape_job_details(current_url)

    current_url = Scraper.scrape_url_indeed(
        'https://www.indeed.com/', 'Software', 'San Diego')
    df_San_Diego = Scraper.scrape_job_details(current_url)

    print(df_Seattle)
    print(df_Portland)
    print(df_Chicago)
    print(df_New_York)
    print(df_San_Francisco)
    print(df_Los_Angeles)
    print(df_Miami)
    print(df_San_Diego)
