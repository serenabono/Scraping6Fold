from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import csv
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
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

def save_list(table, filepath):
    with open(filepath, 'a', newline='') as csvfile:
        wr = csv.writer(csvfile)
        text = list()
        print(table.find_elements(By.XPATH, "//*[contains(@class, 'round')]"))
        for row in table.find_elements(By.XPATH, "//*[contains(@class, 'round')]"):
            text = list()
            for d in row.find_elements(By.CSS_SELECTOR,'li'):                
                text.append(d.text)
            wr.writerow(text)

def save_drop_menu_tables(table):
    for row in table.find_elements(By.CSS_SELECTOR,'tr'):
        docid = row.get_attribute("id")
        try: 
            elem = row.find_elements(By.CSS_SELECTOR,'td')[0]
        except:
            continue
        actions = ActionChains(driver)
        actions.move_to_element(elem)
        actions.click()
        actions.perform()
        string = "votes"+str(docid)
        time.sleep(1)
        table = driver.find_element(By.ID, string)
        save_list(table, "table_drop_down_menu.csv")
        string2 = "$('tr#votes" + str(docid) + "').slideUp();"
        driver.execute_script(string2)
        

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
    "download.prompt_for_download": True,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True
    }
)

driver=webdriver.Chrome("chromedriver", options=chrome_options)
URL = "https://www.sixfold.org/login"
authenticate(driver, URL)
DATAURL = "https://www.sixfold.org/issues.html"
driver.get(DATAURL)
issueslink = [element.find_element(By.TAG_NAME, 'a').get_attribute('href') for element in driver.find_elements(By.ID, "issues")]

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




# actions = ActionChains(driver)
# actions.move_by_offset(512, 512).click().perform()
# import time
# time.sleep(5)
#driver.quit()