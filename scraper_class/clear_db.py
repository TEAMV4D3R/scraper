import requests

for x in range(99):

    url = f'https://allscrapedjobs.herokuapp.com/api/v1/scraped_jobs/{x}/'

    res = requests.delete(url)

    print(res)
