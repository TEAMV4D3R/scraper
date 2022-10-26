import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding": "gzip, deflate",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"}

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.google.com/")

# class Scraper:

#     def __init__(self, url=None):
#         self.url = url

# def scrape_indeed(self):
#     """
#     Arguments:
#         url
#     """

#     page = requests.get(url)

#     print(page)

#     soup1 = BeautifulSoup(page.content, "html.parser")

#     # soup2 = soup1.prettify()

#     print(soup1)

# finds = re.findall(r'current_retail\\\"\:\d+(?:\.\d+)?', soup2)

# item_found = []

# for find in finds:
#     item_found.append(find)

# if item_found is None:
#     actual_price = "Price not available"
#     return actual_price
# else:
#     actual_price = re.findall(r'\d+(?:\.\d+)?', item_found[0])
#     print(float(actual_price[0]))
#     return float(actual_price[0])


def get_current_url(url, job_title, location):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(3)
    driver.find_element_by_xpath(
        '//*[@id="text-input-what"]').send_keys(job_title)
    time.sleep(3)
    driver.find_element_by_xpath(
        '//*[@id="text-input-where"]').send_keys(location)
    time.sleep(3)
    driver.find_element_by_xpath('/html/body/div').click()
    time.sleep(3)
    try:
        driver.find_element_by_xpath('//*[@id="jobsearch"]/button').click()
    except:
        driver.find_element_by_xpath(
            '//*[@id="whatWhereFormId"]/div[3]/button').click()
    current_url = driver.current_url

    return current_url


current_url = get_current_url(
    'https://www.indeed.com/', 'Data Scientist', 'Seattle')

print(current_url)

# if __name__ == '__main__':

#     # url = 'https://jobs.libertymutualgroup.com/job/16551427/software-engineer-remote-remote/?mode=job&iis=Job+Board&iisn=Indeed.com&extcmp=Indd-paid-text-Tech'

#     # Scraper.scrape_indeed(url)

#     current_url = Scraper.get_current_url(
#         'https://www.indeed.com/', 'Data Scientist', "Seattle")
#     print(current_url)
