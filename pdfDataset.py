from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import glob
import os

def generate_dataframe(bios, names):
    df = pd.DataFrame({"names": names, "bios":bios})
    df.to_csv(f'bios[{i}].csv', index=False)

# method to get the downloaded file name
def getDownLoadedFileName(dir):
    downloadspath=dir
    list_of_files = glob.glob(downloadspath+"*.pdf")
    latest_file = max(list_of_files, key=os.path.getctime) 
    return latest_file

def authenticate(driver, authorpath):
    user, password = 'superserena2010@hotmail.com', 'Lorenzo09102000'
    # Github credentials
    username = "superserena2010@hotmail.com"
    password = "Lorenzo09102000"

    driver.get(authorpath)
    driver.find_element("name", "email").send_keys(username)
    driver.find_element("name", "pass").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button").click()

#pip install pdfminer.six
import io

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage


def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    codec = 'utf-8'
    laparams = LAParams()

    with io.StringIO() as retstr:
        with TextConverter(rsrcmgr, retstr, codec=codec,
                           laparams=laparams) as device:
            with open(path, 'rb') as fp:
                interpreter = PDFPageInterpreter(rsrcmgr, device)
                password = ""
                maxpages = 0
                caching = True
                pagenos = set()

                for page in PDFPage.get_pages(fp,
                                              pagenos,
                                              maxpages=maxpages,
                                              password=password,
                                              caching=caching,
                                              check_extractable=True):
                    interpreter.process_page(page)

                return retstr.getvalue()


download_dir = "/home/serena/Desktop/CBMMtutorials/project/Scraping6Fold/pdfs/"
chrome_options = Options()
chrome_options.add_experimental_option('prefs',  {
    "download.default_directory":  download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True
    }
)

driver=webdriver.Chrome("chromedriver", options=chrome_options)
URL = "https://www.sixfold.org/login"
authenticate(driver, URL)
DATAURL = "https://www.sixfold.org/issues.html"
driver.get(DATAURL)

import pandas as pd
import csv
pdfs = pd.read_csv("table.csv")

for url in pdfs["id"]:
    response = driver.get(url)
    #WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "icon")))
    time.sleep(1)
    path = getDownLoadedFileName(download_dir)
    text = convert_pdf_to_txt(path)
    with open("text_dataset.csv", 'a', newline='') as csvfile:
        csv_columns = ["docid", "text"]
        wr = csv.DictWriter(csvfile, fieldnames=csv_columns)
        wr.writerow({"docid": url, "text": text})


driver.quit()