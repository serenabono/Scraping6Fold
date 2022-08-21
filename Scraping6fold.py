from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import csv
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.action_chains import ActionChains

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

def save_tables(table, filepath):
    with open(filepath, 'a', newline='') as csvfile:
        wr = csv.writer(csvfile)
        for row in table.find_elements(By.CSS_SELECTOR,'tr'):
            text = list()
            try:
                link = row.find_elements(By.CSS_SELECTOR,'td')[0].find_element(By.TAG_NAME, 'a').get_attribute('href')
                text.append(link)
            except:
                continue
            for d in row.find_elements(By.CSS_SELECTOR,'td'):                
                text.append(d.text)
            wr.writerow(text)

def save_list(table, filepath, identifier):
    with open(filepath, 'a', newline='') as csvfile:
        csv_columns = ['docid','round','author','score']
        wr = csv.DictWriter(csvfile, fieldnames=csv_columns)
        i=0
        for round in table.find_elements(By.XPATH, "//*[contains(@class, 'round')]"):
            for d in round.find_elements(By.CSS_SELECTOR,'li'):
                row = {"docid": identifier, "round": i, "author": d.find_elements(By.TAG_NAME, "span")[0].text, "score": d.find_elements(By.TAG_NAME, "span")[1].text}
                wr.writerow(row)
            i+=1

def save_drop_menu_tables(table):
    for row in table.find_elements(By.CSS_SELECTOR,'tr'):
        docid = row.get_attribute("id")
        try: 
            elem = row.find_elements(By.CSS_SELECTOR,'td')[4]
        except:
            continue
        actions = ActionChains(driver)
        actions.move_to_element(elem)
        actions.click()
        actions.perform()
        string = "votes"+str(docid)
        time.sleep(1)
        table = driver.find_element(By.ID, string)
        save_list(table, "table_drop_down_menu.csv", row.find_element(By.TAG_NAME, 'a').get_attribute('href'))
        string2 = "$('tr#votes" + str(docid) + "').slideUp();"
        driver.execute_script(string2)
        time.sleep(1)
        

# def save_links(table):
#     links = []
#     for row in table.find_elements(By.CSS_SELECTOR,'tr'):
#         for d in row.find_elements(By.CSS_SELECTOR,'td'):
#             try: 
#                 links.append(d.find_element(By.TAG_NAME, 'a').get_attribute('href'))
#             except:
#                 pass
#     return links


chrome_options = Options()
chrome_options.add_experimental_option('prefs',  {
    "download.default_directory": "/home/serena/Desktop/CBMMtutorials/project/Computational Aesthetics/pdfs/",
    "download.prompt_for_download": False,
    "download.directory_upgrade": False,
    "plugins.always_open_pdf_externally": False
    }
)

driver=webdriver.Chrome("chromedriver", options=chrome_options)
URL = "https://www.sixfold.org/login"
authenticate(driver, URL)
DATAURL = "https://www.sixfold.org/issues.html"
driver.get(DATAURL)
issueslink = [element.find_element(By.TAG_NAME, 'a').get_attribute('href') for element in driver.find_elements(By.ID, "issues")]

# for issuelink in issueslink:
#     driver.get(issuelink)
#     flag = True
#     while(flag):
#         try:
#             driver.find_element(By.XPATH, "// a[contains(text(),\'Next')]").click()
#             issueslink.append(driver.current_url)
#         except:
#             flag = False


bios = list()
names = list()
pdfs = list()
pdfTitles = list()

i = 0
for issuelink in issueslink:
    i+=1
    driver.get(issuelink)
    table = driver.find_element(By.ID, "bigresults")
    save_drop_menu_tables(table)