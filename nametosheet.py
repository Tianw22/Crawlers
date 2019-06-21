import os  
import time
import pandas as pd
import numpy as np
from selenium import webdriver  
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.by import By

website = 'https://www.xxxxxxxxxxxxxxxxxx'

chrome_options = Options()  
chrome_options.add_argument("--headless")
driver = webdriver.Chrome()#options=chrome_options)
driver.maximize_window()
driver.get(website)

#Count the number of elements by xpath
count = len(driver.find_elements_by_xpath('//section[1]//p[1]//strong[1]//a'))

#Append all the texts in this xpath into a list
name = []
for i in range(1,count+1):
    listname = '//section[1]//p[1]//strong[1]//a[%i]'%i
    name.append(driver.find_element_by_xpath(listname).text)
    
#Save list in different sheets in the same output.xlsx.
writer = pd.ExcelWriter('output.xlsx')
for i in range(2,count+2):
    c = len(driver.find_elements_by_xpath('/html[1]/body[1]/div[1]/main[1]/div[2]/div[1]/div[1]/div[1]/section[%i]/ul[1]/li'%i))
    b=[]
    for j in range(1,c+1):
        com = '/html[1]/body[1]/div[1]/main[1]/div[2]/div[1]/div[1]/div[1]/section[%i]/ul[1]/li[%i]'%(i,j)
        t = driver.find_element_by_xpath(com)
        b.append(t.text)
    item = name[i-2]
    pd.DataFrame(b).to_excel(writer,'%s'%item)
writer.save()

#OR save all the records in one list in one sheet.
# b = []
# for i in range(2,count+2):
#     c = len(driver.find_elements_by_xpath('/html[1]/body[1]/div[1]/main[1]/div[2]/div[1]/div[1]/div[1]/section[%i]/ul[1]/li'%i))
#     for j in range(1,c+1):
#         com = '/html[1]/body[1]/div[1]/main[1]/div[2]/div[1]/div[1]/div[1]/section[%i]/ul[1]/li[%i]'%(i,j)
#         t = driver.find_element_by_xpath(com)
#         b.append(t.text)

#Deduplicate
# def spacer(text):
#     return re.sub(r'([0-9])([a-zA-Z])',r"\1 \2",text,re.MULTILINE).strip()
# for i in range(0,len(b)):
#     b[i] = b[i].replace(". ",'.')
#     b[i] = spacer(b[i])
#     b[i] = titlecase(b[i])
# b = b.drop_duplicates(keep='first', inplace=False)
# b = b.reset_index(drop=True)
# pd.DataFrame(b).to_excel('outputall.xlsx', header=False, index=False)
