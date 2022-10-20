from typing_extensions import Self
import requests
from bs4 import BeautifulSoup
import re


class Scraper:

    # def __init__(self, url=None):
    #     self.url = url

    # def scrape_amazon(self, url):
    #     """
    #     Arguments:
    #         url

    #     Returns:
    #         actual price or 999999
    #     """
    #     headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36", "Accept-Encoding": "gzip, deflate",
    #                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"}

    #     page = requests.get(url, headers=headers)

    #     soup1 = BeautifulSoup(page.content, "html.parser")

    #     soup2 = soup1.find_all(class_="a-offscreen")
    #     if soup2:
    #         finds = re.findall(
    #             r'\$\d{1,3}(?:[,]\d{3})*(?:[.]\d{0,2})?|\d{1,3}(?:[ ]\d{3})*(?:[,]\d{0,2})?', str(soup2[0]))

    #         if finds is None:
    #             actual_price = "Price not available"
    #             return actual_price
    #         else:
    #             actual_price = re.findall(
    #                 r'\d{1,3}(?:[,]\d{3})*(?:[.]\d{0,2})?|\d{1,3}(?:[ ]\d{3})*(?:[,]\d{0,2})?', finds[0])
    #             print(float(actual_price[0]))
    #             return (float(actual_price[0]))
    #     else:
    #         print("999999")
    #         return 999999

    def scrape_indeed(self, url):
        """
        Arguments:
            url
        """

        page = requests.get(url)

        print(page)

        soup1 = BeautifulSoup(page.content, "html.parser")

        # soup2 = soup1.prettify()

        print(soup1)

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


if __name__ == '__main__':

    url = 'https://jobs.libertymutualgroup.com/job/16551427/software-engineer-remote-remote/?mode=job&iis=Job+Board&iisn=Indeed.com&extcmp=Indd-paid-text-Tech'

    Scraper().scrape_indeed(url)
