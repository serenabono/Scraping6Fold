from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import csv
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def generate_dataframe(bios, names):
    df = pd.DataFrame({"names": names, "bios":bios})
    df.to_csv(f'bios[{i}].csv', index=False)


def authenticate(driver, authorpath):
    user, password = 'superserena2010@hotmail.com', 'Lorenzo09102000'
    # Github credentials
    username = "superserena2010@hotmail.com"
    password = "Lorenzo09102000"

    driver.get(authorpath)
    driver.find_element("name", "email").send_keys(username)
    driver.find_element("name", "pass").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button").click()

def save_tables(table, typetext, nametext):
    with open(f'table_with_names.csv', 'a', newline='') as csvfile:
        wr = csv.writer(csvfile)
        for row in table.find_elements(By.CSS_SELECTOR,'tr')[1:]:
            text = list()
            try:
                link = row.find_elements(By.CSS_SELECTOR,'td')[0].find_element(By.TAG_NAME, 'a').get_attribute('href')
            except:
                link=""
            text.append(link)
            text.append(nametext)
            text.append(typetext)
            for d in row.find_elements(By.CSS_SELECTOR,'td'):                
                text.append(d.text)
            wr.writerow(text)

def get_bio(bio):
    body = bio.find_element(By.ID, "body")
    description = body.find_elements(By.CSS_SELECTOR, "p")
    if len(description) == 1:
        return ""
    else:
        return description[0].text


def save_bios(table):
    with open(f'bios.csv', 'a', newline='') as csvfile:
        wr = csv.writer(csvfile)
        links = list()
        names = list()
        for row in table.find_elements(By.CSS_SELECTOR,'tr')[1:]:
            text = list()
            name = row.find_elements(By.CSS_SELECTOR,'td')[1]
            try:
                link =  row.find_elements(By.CSS_SELECTOR,'td')[1].find_element(By.TAG_NAME, 'a').get_attribute('href')
                text.append(name.text)
            except:
               link = ""
               text = ""
            names.append(name.text)
            links.append(link)
        for (i,link) in enumerate(links):
            text = list()
            try:
                driver.get(link)
                description = get_bio(driver)
            except:
                description = ""
            text.append(link)
            text.append(names[i])
            text.append(description)
            wr.writerow(text)

def save_links(table):
    links = []
    for row in table.find_elements(By.CSS_SELECTOR,'tr'):
        for d in row.find_elements(By.CSS_SELECTOR,'td'):
            try: 
                links.append(d.find_element(By.TAG_NAME, 'a').get_attribute('href'))
            except:
                pass
    return links

  
chrome_options = Options()
chrome_options.add_experimental_option('prefs',  {
    "download.default_directory": "/home/serena/Desktop/CBMMtutorials/project/Computational Aesthetics/pdfs/",
    "download.prompt_for_download": False,
    "download.directory_upgrade": False,
    "plugins.always_open_pdf_externally": True
    }
)

driver=webdriver.Chrome("chromedriver", options=chrome_options)
URL = "https://www.sixfold.org/login"
authenticate(driver, URL)
DATAURL = "https://www.sixfold.org/issues.html"
driver.get(DATAURL)
issueslink = [element.find_element(By.TAG_NAME, 'a').get_attribute('href') for element in driver.find_elements(By.ID, "issues")]
issuelinkcopy = issueslink.copy()

# for issuelink in issuelinkcopy:
#     driver.get(issuelink)
#     flag = True
#     while(flag):
#         try:
#             driver.find_element(By.XPATH, "// a[contains(text(),\'Next')]").click()
#             issueslink.append(driver.current_url)
#             print(driver.current_url)
#         except:
#             flag = False

import re

bios = list()
names = list()
pdfs = list()
pdfTitles = list()

savebios = False
i = 0

for issuelink in issueslink:
    i+=1
    driver.get(issuelink)
    type = driver.find_element(By.CLASS_NAME, 'lighten')
    nametext = re.findall(r'\|(.*?)\|', type.text)
    if "Fiction" in type.text:
        typetext = "fiction"
    else:
        typetext = "poetry"
    table =  driver.find_element(By.ID, "bigresults")
    save_tables(table, typetext, nametext[0])
    save_bios(table)


driver.quit()