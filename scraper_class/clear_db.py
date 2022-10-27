import requests

def clear_db():

    for x in range(10):
        url = f'https://allscrapedjobs.herokuapp.com/api/v1/scraped_jobs/{x}/'
        res = requests.delete(url)
        return res


if __name__ == "__main__":
    print(clear_db())
