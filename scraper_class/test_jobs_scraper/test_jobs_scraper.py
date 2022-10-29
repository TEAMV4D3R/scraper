from asyncio.constants import ACCEPT_RETRY_DELAY
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import pytest
from scraper_class.jobs_scraper import Scraper


def test_driver_form_component():
    driver = webdriver.Chrome(service=ChromeService(
        executable_path=ChromeDriverManager().install()))

    driver.get("https://www.selenium.dev/selenium/web/web-form.html")

    title = driver.title
    assert title == "Web form"

    driver.quit()


def test_driver_find_element():
    driver = webdriver.Chrome(service=ChromeService(
        executable_path=ChromeDriverManager().install()))

    driver.get("https://www.selenium.dev/selenium/web/web-form.html")

    driver.implicitly_wait(0.5)

    text_box = driver.find_element(by=By.NAME, value="my-text")
    submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")

    text_box.send_keys("Selenium")
    submit_button.click()

    message = driver.find_element(by=By.ID, value="message")
    value = message.text
    assert value == "Received!"

    driver.quit()


def test_csv():
    scraper = Scraper
    assert len(scraper.load_csv()) >= 0


def test_find_Seattle():
    scraper = Scraper
    assert scraper.load_csv()[0] == 'Seattle WA'


def test_scrape_url_indeed():
    scraper = Scraper
    s = scraper.scrape_url_indeed('https://www.indeed.com/', 'Software',
                                  'San Francisco, CA')
    assert s == 'https://www.indeed.com/jobs?q=Software&l=San+Francisco%2C+CA&from=searchOnHP&vjk=685fb92c1c8d354f'


def test_scrape_job_details():
    scraper = Scraper
    s = scraper.scrape_job_details(
        'https://www.indeed.com/jobs?q=Software&l=San+Francisco%2C+CA&from=searchOnHP&vjk=685fb92c1c8d354f')
    assert s != None
