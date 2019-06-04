import re
import requests
from bs4 import BeautifulSoup
from pandas.core.frame import DataFrame

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
driver = "http://www.cdnlist.com"

#Save text as well as the enbeded link associate with the text.
#存储文本和文本对应的链接。
#以第一个为例
#<a href="http://www.akamai.com/html/solutions/sola-solutions.html" target="_blank" xpath="1">Akamai</a>
#each.get('href') => http://www.akamai.com/html/solutions/sola-solutions.html
#each.get_text() => Akamai
def cdnlistfull(driver):
    links = []
    names = []
    req = requests.get(url = driver,headers = headers)
    html = req.text
    div_bf = BeautifulSoup(html,'html.parser')
    div = div_bf.find_all('div', class_ = 'content clearfix notop nobot')
    a_bf = BeautifulSoup(str(div))
    a_no = a_bf.find_all('a', target = '_blank')
    for each in a_no:
        links.append(each.get('href'))
        names.append(each.get_text())
    Total={"Name" : names, "Domain" : links}
    df = DataFrame(Total)
    return df
    
#提取标签及其内标签的文本
#仅提取文本，并清理文本
#<li xpath="1">AAPT – owned by TPG (<a href="http://www.edgecast.com/pr_aapt.htm" target="_blank">reselling EdgeCast</a>)</li>
#each.get_text() => AAPT - owned by TPG (reselling EdgeCast)
def cdnlistname(driver):
    names = []
    req = requests.get(url = driver,headers = headers)
    html = req.text
    div_bf = BeautifulSoup(html,'html.parser')
    li = div_bf.find_all('div', class_ = 'content clearfix notop nobot')
    li_bf = BeautifulSoup(str(li))
    li_no = li_bf.find_all('li')
    for each in li_no:
        name = each.get_text()
        s = str(name)
        #清理（模糊替换）括号以及括号内所有内容
        a = re.sub(u"\\(.*?\\)", "", s)
        names.append(a)
    Total={"Name" : names}
    df = DataFrame(Total)
    return df

dffull = cdnlistfull(driver)
dfname = cdnlistname(driver)
dffull.to_csv('cdnlist-namelink.csv', encoding='utf-8')
dfname.to_csv('cdnlist-name.csv', encoding='utf-8')
