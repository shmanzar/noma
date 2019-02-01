from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
import os, shutil, time

#input month and year from user
month = str(input("Please enter the Month (MM): \n"))
print("\n"+month)
year = str(input("Please enter the Year (YYYY): \n"))
print("\n"+year)

#credentials 
login_url = "http://www.monitoring.punjab.gov.pk/guest"
continue_link = "http://www.monitoring.punjab.gov.pk/evaccs/setting/list_measles_datapack"

user, password = 'evaccs_visitors@pitb.gov.pk', 'evaccs_visitors'

#set download folder on desktop
download_path = os.path.expanduser('~/Desktop/Measles_Datapacks/')

if os.path.exists(download_path) and os.path.isdir(download_path):
    shutil.rmtree(download_path)
    os.mkdir(download_path)

#set browser settings
chrome_options = webdriver.ChromeOptions()
prefs = {'download.default_directory' : os.path.expanduser('~/Desktop/Measles_Datapacks/')}
chrome_options.add_experimental_option('prefs', prefs)

#open browser
browser = webdriver.Chrome(options=chrome_options)
browser.implicitly_wait(10)

#navigate through logins
browser.get(login_url)
emailElem = browser.find_element_by_id('username')
emailElem.send_keys(user)
passwordElem = browser.find_element_by_id('password')
passwordElem.send_keys(password)
signInbutton = browser.find_element_by_class_name('btn')
signInbutton.click()

#open Measles-1 page
browser.get(continue_link)

# Make a list of all the districts available
options = Select(browser.find_element_by_id("filter_district")).options
optionsList = []

for option in options: 
    optionsList.append(option.get_attribute("value"))
    if option.get_attribute("value") == "0":
        optionsList.remove(option.get_attribute("value"))

optionsList = list(map(int, optionsList))

def change_date(m,y):
    date_select = browser.find_element_by_id("monthyear")
    date_select.send_keys(m)
    date_select.click()
    date_select.send_keys(y)
    pass

change_date(month,year)



# for district in optionsList:
#     district_drop = browser.find_element_by_xpath(f'//*[@id="filter_district"]/option[{district+1}]').click()
#     downloader_btn = browser.find_element_by_css_selector("#print > button")
#     downloader_btn.click()
#     browser.implicitly_wait(3)

filter_btn = browser.find_element_by_xpath('/html/body/div/div/section/div/div[1]/div/form/div/div[3]/button')
filter_btn.click()

for district in optionsList:
    district_drop = browser.find_element_by_xpath(f'//*[@id="filter_district"]/option[{district+1}]').click()
    change_date(month,year)
    filter_btn = browser.find_element_by_xpath('/html/body/div/div/section/div/div[1]/div/form/div/div[3]/button')
    filter_btn.click()
    downloader_btn = browser.find_element_by_css_selector("#example1_wrapper > div.dt-buttons > a.dt-button.buttons-pdf.buttons-html5")
    downloader_btn.click()
    # time.sleep(4)

print(optionsList)
