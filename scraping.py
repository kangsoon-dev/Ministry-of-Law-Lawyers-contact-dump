import csv
import pandas as pd
import ctypes
from string import ascii_uppercase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def clickAlpha(c):
    driver.execute_script("return arguments[0].scrollIntoView(true);", driver.find_element_by_id('SearchText'))
    for e in driver.find_elements_by_tag_name('a'):
        if e.text == c:
            e.click()
            completeSearch()
            break

def populatePageList():
    pageList = []
    for e in driver.find_elements_by_tag_name('a'):
        try:
            if e.text != "" and int(e.text) > 1:
                pageList = pageList + [e]
        except ValueError:
            continue
    return pageList

def completeSearch():
    while True:
        try:
            WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, '//*[@id="lsra-msg-content"]')))
        except TimeoutException:
            break

def getRangePages():
    countValue = driver.find_element_by_xpath('//*[@id="recordAmount"]').get_attribute('value')
    iterList = list(range(int(int(countValue)/50)+1))
    iterList = [x+1 for x in iterList]
    return iterList

def addEntry(j,lawyers):
    lawyerEntry = driver.find_elements_by_xpath('//*[@id="Tbl_Search"]/tbody/tr['+str(j)+']/td/table')
    for listItem in lawyerEntry:
        entryFields = listItem.find_elements_by_tag_name('td')
        LName = entryFields[1].text
        LRegType = entryFields[2].text
        LTitle = entryFields[3].text
        LDateAdmission = entryFields[4].text
        LPracArea = entryFields[5].text
        LNameLawPrac = entryFields[7].text
        LTypeLawPrac = entryFields[8].text
        LEmail = entryFields[9].text
        LWebsite = entryFields[10].text
        LTelNo = entryFields[11].text
        LAddr = entryFields[13].text
        df = pd.DataFrame([[LName,LRegType,LTitle,LDateAdmission,LPracArea,LNameLawPrac,LTypeLawPrac,LEmail,LWebsite,LTelNo,LAddr]],columns=columns)
        lawyers = pd.concat([lawyers,df],axis = 0).reset_index(drop=True)
    return lawyers

if __name__ == '__main__':
    columns = [ 'Name',
                'Registration Type',
                'Job Title',
                'Date of Admission (Singapore Bar)',
                'Key Practice Area(s)',
                'Name of Law Practice',
                'Type of Law Practice',
                'Email',
                'Website',
                'Tel No.',
                'Address']
    lawyers = pd.DataFrame(columns=columns)
    driver = webdriver.Chrome('../chromedriver.exe')  # chromedriver path
    driver.get('https://www.mlaw.gov.sg/eservices/lsra/search-lawyer-or-law-firm/');
    # element = WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.Id, 'id')))
    ctypes.windll.user32.MessageBoxW(0, "Complete CAPTCHA then click OK", "CAPTCHA", 0)
    driver.find_element_by_xpath('//*[@id="btnSearch"]').click()
    completeSearch()
    driver.find_element_by_xpath('//*[@id="PageSize"]/option[text()="50"]').click()
    completeSearch()
    start = 1 # 1
    end = 29 # 29

    for c in ascii_uppercase[start-1:end-1]:
        clickAlpha(c)
        iterList = getRangePages()
        for i in iterList: # page level
            pageList = populatePageList()
            for page in pageList:
                if int(page.text) > 1 and int(page.text) == i:
                    page.click()
                    completeSearch()
            for j in list(range(51))[1:]:
                print("processing '" + c + "' page " + str(i) + " entry " + str(j))
                lawyers = addEntry(j,lawyers)

    directory = "lawyers.csv"
    # for first output
    lawyers.to_csv(directory)
    # for subsequent output
    # with open(directory,"a") as f:
    #     lawyers.to_csv(f,header=False)

    driver.quit()
    ctypes.windll.user32.MessageBoxW(0, "output saved as " + directory, "Done!", 0)