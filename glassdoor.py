from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from time import sleep
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
import pandas as pd
final_data = []

page_1 = 'https://www.glassdoor.com/Reviews/MGM-Resorts-International-Reviews-E1260.htm'
page_2 = 'https://www.glassdoor.com/Reviews/MGM-Resorts-International-Reviews-E1260_P2.htm?filter.iso3Language=eng'
page_3 = 'https://www.glassdoor.com/Reviews/MGM-Resorts-International-Reviews-E1260_P3.htm?filter.iso3Language=eng'
page_4 = 'https://www.glassdoor.com/Reviews/MGM-Resorts-International-Reviews-E1260_P4.htm?filter.iso3Language=eng'
urls = [page_1, page_2, page_3, page_4]

for i in range(len(urls)):
    service = Service(executable_path="C:\Development\chromedriver.exe")  # this is the path to your chrome web driver
    capabilities = DesiredCapabilities.CHROME
    capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-popup-blocking')
    driver = webdriver.Chrome(service=service, options=options, desired_capabilities=capabilities)
    # Enable network interception
    driver.execute_cdp_cmd('Network.enable', {})

    # Block the gd-user-hardsell-overlay.bundle.js file
    driver.execute_cdp_cmd('Network.setBlockedURLs', {'urls': ['*gd-user-hardsell-overlay.bundle.js*']})
    driver.get(urls[i])
    page_source = driver.page_source
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(3)
    soup = BeautifulSoup(page_source, 'html.parser')
    containers = soup.find_all('li', class_='noBorder empReview cf pb-0 mb-0')
    for container in containers:
        rating = container.find('span', class_='ratingNumber mr-xsm').get_text()
        title = container.find('h2', class_='mb-xxsm mt-0 css-93svrw el6ke055').get_text()
        pros = container.find('span', {'data-test': 'pros'}).get_text()
        cons = container.find('span', {'data-test': 'cons'}).get_text()
        reviewer_title = container.find('span', class_='middle common__EiReviewDetailsStyle__newGrey').get_text().split("-")[1]
        try:
            reviewer_location = container.find('span', class_='common__EiReviewDetailsStyle__newUiJobLine').get_text().split("\xa0in")[1]
        except:
            reviewer_location = 'null'
        reviewer_datetime = container.find('span', class_='middle common__EiReviewDetailsStyle__newGrey').get_text().split("-")[0]
        is_current_job = "current" in container.find('span', class_="pt-xsm pt-md-0 css-1qxtz39 eg4psks0").get_text().lower()

        data = {
            'rating': rating,
            'title': title,
            'pros': pros,
            'cons': cons,
            'reviewer_title': reviewer_title,
            'reviewer_location': reviewer_location,
            'datetime': reviewer_datetime,
            'is_current_job': is_current_job,
        }
        final_data.append(data)

    driver.close()
    print(f"page {i + 1} scraped.")
    sleep(2)
print(final_data)
print(len(final_data))

# create csv
df = pd.DataFrame(final_data)
df.to_csv('glassdoor_data.csv', index=False)
# print(soup.prettify())
