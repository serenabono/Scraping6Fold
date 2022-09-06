from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import csv
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

def save_list(table, filepath, identifier,name, title,  nametext, typetext):
    with open(filepath, 'a', newline='') as csvfile:
        csv_columns = ['docid','author','namecontext','typecontext','title','round','author','score']
        wr = csv.DictWriter(csvfile, fieldnames=csv_columns)
        i=0
        for round in table.find_elements(By.CLASS_NAME, "round"):
            for d in round.find_elements(By.CSS_SELECTOR,'li'):
                player = WebDriverWait(d, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "player"))
                )
                row = {"docid": identifier,"author":name, "namecontext":namecontext,"typecontext":typecontext ,"title":title, "round": i, "author": d.find_element(By.CLASS_NAME, "player").get_attribute('textContent'), "score": d.find_element(By.CLASS_NAME, "vote").get_attribute('textContent')}
                wr.writerow(row)
            i+=1

def save_drop_menu_tables(table,  nametext, typetext):
    for row in table.find_elements(By.CSS_SELECTOR,'tr')[1:]:
        docid = row.get_attribute("id")
        name = row.find_elements(By.CSS_SELECTOR,'td')[0].text
        title = row.find_elements(By.CSS_SELECTOR,'td')[1].text
        elem = row.find_elements(By.CSS_SELECTOR,'td')[2]
        try:
            link = row.find_elements(By.CSS_SELECTOR,'td')[0].find_element(By.TAG_NAME, 'a').get_attribute('href')
        except:
            link = ""
        exception=True
        contin = False
        n=0
        while exception:
            exception=False
            try:
                actions = ActionChains(driver)
                actions.move_to_element(elem)
                actions.click()
                actions.perform()
                string = "votes"+str(docid)
                table = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.ID, string))
                )
            except:
                exception=True
                print("#exc, ",n)
                n+=1
                time.sleep(n)
                if n>5:
                    exception=False
                    contin = True
        if contin:
            print("AUCH")
            continue
        
        save_list(table, "table_drop_down_menu.csv", link, name, title, nametext, typetext)
        string2 = "$('tr#votes" + str(docid) + "').slideUp();"
        driver.execute_script(string2)

chrome_options = Options()
chrome_options.binary_location = "/home/seb300/local/src/chrome/opt/google/chrome/chrome"
chrome_options.add_argument("--remote-debugging-port=9222") 
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_experimental_option('prefs',  {
    "download.default_directory": "/home/serena/Desktop/CBMMtutorials/project/Computational Aesthetics/pdfs/",
    "download.prompt_for_download": False,
    "download.directory_upgrade": False,
    "plugins.always_open_pdf_externally": False
    }
)

driver=webdriver.Chrome("/home/seb300/chromedriver/chromedriver", options=chrome_options)
URL = "https://www.sixfold.org/login"
authenticate(driver, URL)
DATAURL = "https://www.sixfold.org/issues.html"
driver.get(DATAURL)
issueslink = [element.find_element(By.TAG_NAME, 'a').get_attribute('href') for element in driver.find_elements(By.ID, "issues")]
issuelinkcopy = issueslink.copy()

for issuelink in issuelinkcopy:
    driver.get(issuelink)
    flag = True
    while(flag):
        try:
            driver.find_element(By.XPATH, "// a[contains(text(),\'Next')]").click()
            issueslink.append(driver.current_url)
            print(driver.current_url)
        except:
            flag = False


bios = list()
names = list()
pdfs = list()
pdfTitles = list()

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
    table = driver.find_element(By.ID, "bigresults")
    save_drop_menu_tables(table, nametext[0], typetext)