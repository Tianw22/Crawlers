import SeleniumLibrary
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException
import pandas as pd

page2016 = "https://techfieldday.com/attendee/delegates/2016-delegates/"
page2017 = "https://techfieldday.com/attendee/delegates/2017-delegates/"
page2018 = "https://techfieldday.com/attendee/delegates/2018-delegates/"
page2019 = "https://techfieldday.com/attendee/delegates/2019-delegates/"

website = "//td[contains(text(),'Web site:')]//ul//li"
twitter = "//td[contains(text(),'Twitter:')]/ul/li/a"
linkedin = "//tr[4]/td[1]/ul[1]/li[1]/a[1]"
descri = "/html[1]/body[1]/div[1]/div[3]/div[1]/div[1]/div[2]/div[1]/p[1]"
evatta = "//table[@class='fourcol']//tbody"

driver = webdriver.Chrome()
driver.maximize_window()

def getnamelist(pagelink):
    driver.get(pagelink)
    countvert = len(driver.find_elements_by_xpath("//tr"))
    namelist = []
    weblist = []
    for i in range(1,int(countvert)+1):
        counthori = len(driver.find_elements_by_xpath("//tr[%i]/td"%i))
        for j in range(1,int(counthori)+1):
            name = driver.find_element_by_xpath("//tr[%i]/td[%i]"%(i,j)).text
            namelist.append(name)
            elems = driver.find_elements_by_xpath("//tr[%i]/td[%i]/a[@href]"%(i,j))
            for elem in elems:
                web = elem.get_attribute("href")
                weblist.append(web)    
    return namelist,weblist
    
nl1,wl1 = getnamelist(page2016)
nl2,wl2 = getnamelist(page2017)
nl3,wl3 = getnamelist(page2018)
nl4,wl4 = getnamelist(page2019)

def getpersonpage(pagelinklist):
    
    websitelist = []
    twitternamelist = []
    twitterlinklist = []
    linkedinlist = []
    descriplist = []
    eventattlist = []

    for pagelink in pagelinklist:
        driver.get(pagelink)
        try:
            ws = driver.find_element_by_xpath(website).text
            websitelist.append(ws)
        except NoSuchElementException:
            websitelist.append(" ")
        try:        
            tn = driver.find_element_by_xpath(twitter).text
            twitternamelist.append(tn)
        except NoSuchElementException:
            twitternamelist.append(" ")
        try:
            tl = driver.find_element_by_xpath(twitter).get_attribute("href")
            twitterlinklist.append(tl)
        except NoSuchElementException:
            twitterlinklist.append(" ")
        try:
            ll = driver.find_element_by_xpath(linkedin).text
            linkedinlist.append(ll)
        except NoSuchElementException:
            linkedinlist.append(" ")
        try:
            des = driver.find_element_by_xpath(descri).text
            descriplist.append(des)
        except NoSuchElementException:
            descriplist.append(" ")
        try:
            ea = driver.find_element_by_xpath(evatta).text
            eventattlist.append(ea)
        except NoSuchElementException:
            eventattlist.append(" ")
    return websitelist,twitternamelist,twitterlinklist,linkedinlist,descriplist,eventattlist
    
w1,t1,t12,l1,d1,e1 = getpersonpage(wl1)
w2,t2,t22,l2,d2,e2 = getpersonpage(wl2)
w3,t3,t32,l3,d3,e3 = getpersonpage(wl3)
w4,t4,t42,l4,d4,e4 = getpersonpage(wl4)

df2016 = {"Name" : nl1, "PersonalPage" : wl1, "Website" : w1, "TwitterName" : t1, "TwitterLink" : t12 , "LinkedIn" : l1, "Description" : d1,"EventAttend" : e1}
df2017 = {"Name" : nl2, "PersonalPage" : wl2, "Website" : w2, "TwitterName" : t2, "TwitterLink" : t22 , "LinkedIn" : l2, "Description" : d2,"EventAttend" : e2}
df2018 = {"Name" : nl3, "PersonalPage" : wl3, "Website" : w3, "TwitterName" : t3, "TwitterLink" : t32 , "LinkedIn" : l3, "Description" : d3,"EventAttend" : e3}
df2019 = {"Name" : nl4, "PersonalPage" : wl4, "Website" : w4, "TwitterName" : t4, "TwitterLink" : t42 , "LinkedIn" : l4, "Description" : d4,"EventAttend" : e4}

resultdf2016 = pd.DataFrame(df2016)
resultdf2017 = pd.DataFrame(df2017)
resultdf2018 = pd.DataFrame(df2018)
resultdf2019 = pd.DataFrame(df2019)

resultdf2016.to_excel("TFD2016.xlsx")
resultdf2017.to_excel("TFD2017.xlsx")
resultdf2018.to_excel("TFD2018.xlsx")
resultdf2019.to_excel("TFD2019.xlsx")
