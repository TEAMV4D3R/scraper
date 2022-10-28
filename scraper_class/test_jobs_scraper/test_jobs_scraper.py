from asyncio.constants import ACCEPT_RETRY_DELAY
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import pytest
from scraper_class.jobs_scraper import Scraper


def test_components():
    driver = webdriver.Chrome(service=ChromeService(
        executable_path=ChromeDriverManager().install()))

    driver.get("https://www.selenium.dev/selenium/web/web-form.html")

    title = driver.title
    assert title == "Web form"

    print("Correct title is Web Form, return is : ", title)

    driver.implicitly_wait(0.5)

    text_box = driver.find_element(by=By.NAME, value="my-text")
    submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")

    text_box.send_keys("Selenium")
    submit_button.click()

    message = driver.find_element(by=By.ID, value="message")
    value = message.text
    assert value == "Received!"

    print("Correct value is Received, return is : ", value)

    driver.quit()


def test_csv():
    scraper = Scraper
    assert len(scraper.load_csv()) >= 0


def test_find_Seattle():
    scraper = Scraper
    assert scraper.load_csv()[0] == 'Seattle WA'
