from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

driver = webdriver.Chrome()
driver.get("https://en.wikipedia.org/wiki/UEFA_European_Championship#Results")
time.sleep(3)

tables = driver.find_elements(By.CSS_SELECTOR,"table.wikitable")
table_index = 0
if table_index >= len(tables):
    print(f"Table index {table_index} is out of range. Found {len(tables)} tables.")
table = tables[table_index]

with open(r"C:\Users\user\PycharmProjects\Python\Web_scrapin\data.csv",'w',encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["Host","Year","Home","Away","Score","Stage"])
    writer.writeheader
    rows = table.find_elements(By.XPATH, ".//tr")
    year_element = table.find_elements(By.XPATH, "//tr/td[1]/a[translate(text(), '0123456789', '') = '']")
    for row,year in zip(rows,year_element):
            y = year.text
            year.click()
            table_host = driver.find_element(By.CSS_SELECTOR,"table.infobox.vcalendar")        
            if table_host:
                hosts = table_host.find_element(By.XPATH,"//th[contains(text(),'Host countries') or contains(text(),'Host country')]//following::td[1]")
                host = ' '.join((hosts.text).splitlines())
                WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.footballbox")))
                matchs = driver.find_elements(By.CSS_SELECTOR,"div.footballbox")
                if matchs:
                    for match in matchs:
                        home = match.find_element(By.CSS_SELECTOR, "th.fhome").text 
                        away = match.find_element(By.CSS_SELECTOR, "th.faway").text
                        score = match.find_element(By.CSS_SELECTOR, "th.fscore").text
                        stage = match.find_element(By.XPATH, "./preceding::h3[1]").text
                        writer.writerow({"Host":host,"Year":y,"Home":home,"Away":away,"Score":score,"Stage":stage})
                else:
                    print("No Matches in this Tournaments")
            driver.back()

        
driver.quit()