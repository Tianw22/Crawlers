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

driver = webdriver.Chrome()
driver.maximize_window()

NTT = "https://asrank.caida.org/orgs/NTTAM-1-ARIN"
PCCW = "https://asrank.caida.org/orgs/BNA-42-ARIN"
SINGTEL = "https://asrank.caida.org/orgs/ORG-SOPL2-AP-APNIC"
TELSTRA = "https://asrank.caida.org/orgs/ORG-TIL3-AP-APNIC"

Title = "/html[1]/body[1]/div[3]/div[3]/table[1]/tbody[1]/tr[4]/td[1]/a[1]"

def getlist(link):
            
    asrank = []
    asnum = []
    numlink = []
    asname = []
    title = []

    j=1
    countvert = 1 

    while countvert > 0:
        
        pagelink = link + '?page_number=%i&page_size=40&sort=rank'%j
        #print(pagelink)
        j = j+1
        driver.get(pagelink)
        try:
            wait = WebDriverWait(driver, 20).until(ec.visibility_of_element_located((By.XPATH, "//div[@id='org_members_table']//tr[5]//td[2]")))
        except TimeoutException:
            break
        countvert = len(driver.find_elements_by_xpath("//div[@id='org_members_table']//tr//td[1][@class='center-align']"))
        TI = driver.find_element_by_xpath(Title).text
        if countvert==0:
            break

        for i in range(5,int(countvert)+5):

            title.append(TI)

            try:
                rank = driver.find_element_by_xpath("//div[@id='org_members_table']//tr[%i]//td[1]"%i).text
                asrank.append(rank)
            except NoSuchElementException:
                rank = "unknown"
                asrank.append(rank)

            try:    
                num = driver.find_element_by_xpath("//div[@id='org_members_table']//tr[%i]//td[2]"%i).text
                asnum.append(num)
            except NoSuchElementException:
                num = "unknown" 
                asnum.append(num)

            try:
                link = driver.find_element_by_xpath("//div[@id='org_members_table']//tr[%i]//td[2]/a[@href]"%i).get_attribute("href")
                numlink.append(link)
            except NoSuchElementException:
                link = "unknown"
                numlink.append(link)

            try:
                name = driver.find_element_by_xpath("/html[1]/body[1]/div[3]/div[3]/table[1]/tbody[1]/tr[%i]/td[3]"%i).text
                asname.append(name)
            except NoSuchElementException:
                name = "unknown"
                asname.append(name)

    dic = {"Title": title, "AS Rank" : asrank, "AS Number" : asnum, "Num Link" : numlink, "AS Name" : asname}
    df = pd.DataFrame(dic)
    df.to_csv('List-%s.csv'%TI)
    return df
    
NTTDF = getlist(NTT)
PCCWDF = getlist(PCCW)
SINGTELDF = getlist(SINGTEL)
TELSTRADF = getlist(TELSTRA)

NTTDF = pd.read_csv("List-NTT America, Inc..csv")
TELSTRADF = pd.read_csv("List-Telstra International Limited.csv")
SINGTELDF = pd.read_csv("List-SingTel Optus Pty Ltd.csv")
PCCWDF = pd.read_csv("List-PCCW Global, Inc..csv")

frames = [NTTDF, TELSTRADF, SINGTELDF, PCCWDF]
result = pd.concat(frames)
resultdf = pd.DataFrame(result)

resultnew = resultdf.reset_index(drop=True)

def subpage(link,asn,asnum):
    
    asrank = []
    asneig = []
    orgname = []
    nation = []
    ascuscone = []
    numpath = []
    relation = []
    title=[]
    astitle = []
    asnumall = []
   
    j=1
    countvert = 1 
    
    while countvert > 0:
        
        pagelink = link + '?page_number=%i&page_size=40&sort=rank'%j
        #print(link)
        #print(pagelink)
        j = j+1
        driver.get(pagelink)
        try:
            wait = WebDriverWait(driver, 20).until(ec.visibility_of_element_located((By.XPATH, "//tr[2]//td[@class='center-align'][1]")))
        except TimeoutException:
            break
        countvert = len(driver.find_elements_by_xpath("//tr//td[@class='center-align'][1]"))
        TI = driver.find_element_by_xpath("/html[1]/body[1]/div[3]/div[2]/div[2]/table[1]/tbody[1]/tr[3]/td[1]/a[1]").text
        
        if countvert==0:
            break
        
        for i in range(2,countvert+2):
            
            title.append(TI)
            astitle.append(asn)
            asnumall.append(asnum)
            
            try:
                rank = driver.find_element_by_xpath("//div[@id='asn_neighbors_table']//tr[%i]//td[1]"%i).text
                asrank.append(rank)
            except NoSuchElementException:
                rank = "unknown"
                asrank.append(rank)
                
            try:
                nei = driver.find_element_by_xpath("/html[1]/body[1]/div[3]/div[3]/table[1]/tbody[1]/tr[%i]/td[2]/a[1]"%i).text
                asneig.append(nei)
            except NoSuchElementException:
                nei = "unknown"
                asneig.append(nei)

            try:
                name = driver.find_element_by_xpath("/html[1]/body[1]/div[3]/div[3]/table[1]/tbody[1]/tr[%i]/td[3]/a[1]"%i).text
                orgname.append(name)
            except NoSuchElementException:
                name = "unknown"
                orgname.append(name)

            try:
                nat = driver.find_element_by_xpath("//tr[%i]//td[4]//span[@class]"%i).get_attribute("class")
                nation.append(nat) 
            except NoSuchElementException:
                nat = "unknown"
                nation.append(nat) 

            try:
                cone = driver.find_element_by_xpath("/html[1]/body[1]/div[3]/div[3]/table[1]/tbody[1]/tr[%i]/td[5]"%i).text
                ascuscone.append(cone) 
            except NoSuchElementException:
                cone = "unknown"
                ascuscone.append(cone)          
                
            try:
                path = driver.find_element_by_xpath("/html[1]/body[1]/div[3]/div[3]/table[1]/tbody[1]/tr[%i]/td[6]"%i).text
                numpath.append(path)
            except NoSuchElementException:
                path = "unknown"
                numpath.append(path)
            
            try:
                rela = driver.find_element_by_xpath("//tr[%i]//td[7]"%i).text
                relation.append(rela)
            except NoSuchElementException:
                rela = "unknown"
                relation.append(rela)
                

            
        dic = {"AS Rank" : asrank, "AS Neighbors" : asneig, 
               "Org Name" : orgname,"AS Customer Cone" : ascuscone, 
               "Number of Paths" : numpath, "Relationship" : relation,
               "Organization" : title, "Nation" : nation, 
               "AS Name" :asn, "AS Number" : asnumall}
        df = pd.DataFrame(dic)
        #df.to_csv('NeighborList.csv',mode = 'a')
    return df, TI  
    
for i in range(0,len(resultnew['Num Link'])):
    #print(str(resultnew['Num Link'][i]))
    df, TI = subpage(str(resultnew['Num Link'][i]),resultnew['AS Name'][i],resultnew['AS Number'][i])
    df.to_csv('NeighborListNew.csv',mode = 'a')
    
resultnew.to_excel("asoffour.xlsx")
