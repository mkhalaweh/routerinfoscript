import time
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from threading import Timer
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

#automation program to retrieve data from router network manager (HG8245Q2)

username = "root"
password = "hmh5102000"

url = "http://192.122.186.1/" #change this to your router IP
url2 = "http://192.122.186.1/html/bbsp/userdevinfo/userdevinfo.asp"

driver = webdriver.Chrome("D:\chromedriver_win32\chromedriver")

driver.get(url)

driver.find_element(By.ID, "txt_Username").send_keys(username) #sends username to username field in login page
driver.find_element(By.ID, "txt_Password").send_keys(password) #sends password to password field in login page
driver.find_element(By.ID, "button").click() #sends click to submit button on login page

index_page = driver.get(url2) #gets the url that has all the user devices on the network

time.sleep(3) #sleep to load the page before retreiving data

devices = driver.find_elements(By.XPATH, "//tbody/tr/td[1]") #finding all fields using XPATH
portid = driver.find_elements(By.XPATH, "//tbody/tr/td[2]")
ipaddress = driver.find_elements(By.XPATH, "//tbody/tr/td[4]")
macaddress = driver.find_elements(By.XPATH, "//tbody/tr/td[5]")
devicestatus = driver.find_elements(By.XPATH, "//tbody/tr/td[6]")

data = []

for i in range(1, len(devices)-1):
        temporary_data = {'Device Name': devices[i].text,
                        'Port ID': portid[i].text,
                        'IP Address': ipaddress[i].text,
                        'MAC Address':macaddress[i].text,
                        'Device Status': devicestatus[i].text}
        data.append(temporary_data)

numofpages = 4 #change this to the number of pages of users

for y in range (1, numofpages):
    driver.find_element(By.ID, "next").click()
    time.sleep(3)
    devices = driver.find_elements(By.XPATH, "//tbody/tr/td[1]") #finding all fields using XPATH
    portid = driver.find_elements(By.XPATH, "//tbody/tr/td[2]")
    ipaddress = driver.find_elements(By.XPATH, "//tbody/tr/td[4]")
    macaddress = driver.find_elements(By.XPATH, "//tbody/tr/td[5]")
    devicestatus = driver.find_elements(By.XPATH, "//tbody/tr/td[6]")
    for i in range(1, len(devices)-1):
        temporary_data = {'Device Name': devices[i].text,
                        'Port ID': portid[i].text,
                        'IP Address': ipaddress[i].text,
                        'MAC Address':macaddress[i].text,
                        'Device Status': devicestatus[i].text}
        data.append(temporary_data)

    # driver.find_element(By.ID, "next").click()
    # time.sleep(3)

df_data=pd.DataFrame(data)
print(df_data)

print("\nNumber of total devices:")
print(len(data))

print("\nNumber of devices with no name:")
nodwnn=0
for i in data:
    if i['Device Name']=='--':
        nodwnn=nodwnn+1

print(nodwnn)

print("\nNumber of online devices:")
nood=0
for i in data:
    if i['Device Status']=='Online':
        nood=nood+1

print(nood)

print("\nNumber of offline devices:")
nood2=0
for i in data:
    if i['Device Status']=='Offline':
        nood2=nood2+1

print(nood2)


