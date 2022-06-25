from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

def scrape_linkedin(city):
    """
    Scrapes of the last 25 jobs position, the title, company, location.
    """
    driver = webdriver.Chrome(ChromeDriverManager().install())
    url="https://www.linkedin.com/jobs"
    driver.get(url)
    #clear location
    driver.find_element_by_xpath("""//*[@id="JOBS"]/section[2]/button""").click()
    search_location = driver.find_element_by_xpath("""//*[@id="JOBS"]/section[2]/input""")
    search_location.send_keys(city)

    #insert password
    search_job = driver.find_element_by_xpath("""//*[@id="JOBS"]/section[1]/input""")
    search_job.send_keys('Data Science')

    driver.find_element_by_xpath("""//*[@id="main-content"]/section[1]/div/section/div[2]/button[2]""").click()    

    #extract position title
    title_1 = driver.find_elements_by_class_name("base-search-card__title")
    title = []
    for a in title_1:
        title.append(a.text)
    
    #extract company name
    company_1 = driver.find_elements_by_class_name("base-search-card__subtitle")
    company = []
    for b in company_1:
        company.append(b.text)

    #extract location of the job
    location_1 = driver.find_elements_by_class_name("job-search-card__location")
    location = []
    for c in location_1:
        location.append(c.text)
    
    link = ['https://it.linkedin.com/jobs/view/data-scientist-at-bridgestone-emia-2968217447?refId=2V5%2BvrWxcRVIMtvnTGbhbQ%3D%3D&trackingId=Y6Apd2e3M%2Bn4I5VY8ljG2Q%3D%3D&position=16&pageNum=0&trk=public_jobs_jserp-result_search-card']
    find_href = driver.find_elements_by_class_name('base-card__full-link')
    for i in find_href:
        link.append(i.get_attribute('href'))
    
     #export in csv
    df = pd.DataFrame(dict(Location=location, Title=title, Company=company, Link=link))
    return df

