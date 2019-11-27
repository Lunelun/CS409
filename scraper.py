from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import csv
from time import sleep

url = "http://www.aqmthai.com/public_report.php"

driver = webdriver.Firefox()
driver.implicitly_wait(30)
driver.get(url)

table_bt = driver.find_element_by_name("bt_show_table")

lp_select = Select(driver.find_element_by_id("stationId"))
lp_select.select_by_value('37t')


param_select = Select(driver.find_element_by_id("parameterSelected"))
param_select.select_by_value("PM2.5")
param_select.select_by_value("WS")      #Wind Speed
param_select.select_by_value("WD")      #Wind Direction
param_select.select_by_value("RH")      #Reletive Humidity
param_select.select_by_value("BP")      #Barometric Pressure
param_select.select_by_value("RAIN")    #Rain Volume
param_select.select_by_value("TEMP")    #Temperature

table_bt.click()

sleep(2)

next_bt = driver.find_element_by_name("bt_next_page")

header_presented = False

with open('train_data.csv', mode='w', newline='') as train_file:
    writer = csv.writer(train_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for i in range(7): 
        soup = BeautifulSoup(driver.page_source, "lxml")
        table = soup.find("div", attrs={"id": "table_mn_div"})
        rows = table.find_all("tr")
        for tr in rows:
            datas = tr.find_all("td")

            line = []
            for td in datas:
                inp = td.find("input")
                line.append(inp['value'])

            if not line:
                continue
            elif "Date Time" in line and header_presented == False:
                writer.writerow(line)
                header_presented = True                
            elif "Date Time" in line and header_presented == True:
                continue
            elif "-" in line:
                continue
            else:
                writer.writerow(line)
        next_bt.click()
        sleep(10)
        next_bt = driver.find_element_by_name("bt_next_page")

driver.quit()
    # row = [i.get_text() for i in td]
    # print(row)


# table = soup.findAll("tr" , {"class" : "ui-mas-table-tr2" })
# table = soup.find_all('tr', {'class' : 'ui-mas-table-tr2' })
# tr = driver.find_element_by_tag_name("table")

# f2 = [tbl for tbl in soup.find_all('table') ]
# print(tr)
