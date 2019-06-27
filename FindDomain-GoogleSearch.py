#pip install unidecode
#pip install fake_useragent
#pip install git+https://github.com/abenassi/Google-Search-API
#pip install git+https://github.com/abenassi/Google-Search-API

#Import packages
from google import google
import pandas as pd
import datetime
import re

today = datetime.date.today()
#Search the elements in cdnlist-name.csv one by one in Google.com.
#Save the searching results in Google.com (Links and descriptions) 
#在Google中搜索表格中所有元素，并存储Google查询结果的第一页中的链接以及链接的描述。
df = pd.read_excel('xxxxxxxxx.xlsx')
df = pd.DataFrame(df)
num_page = 1
des = []
lin = []
n = []
a = 1
for i in df['Company']:
    search_results = google.search("%s"%i, num_page)
    name = str(i)
    for result in search_results:
        de = result.description
        de = str(de)
        li = result.link
        li = str(li)
        des.append(de)
        lin.append(li)
        n.append(name)
    #print("This is the %i record"%a)
    a = a+1
Total = {"Description":des,"Links":lin, "Name":n}
df = pd.DataFrame(Total)
#df.to_csv('list-%s.csv'%today,header = True, index = False)

dfcopy = df.copy()
droplist = ['linkedin','bloomberg','glassdoor','crunchbase','wikipedia','facebook','twitter','buzzfile','instagram','wiki','dictionary','owler','zoominfo','indeed','None']
for item in droplist:
    dfcopy = dfcopy[~dfcopy.Links.str.contains(item)]
    
dffirst = dfcopy.drop_duplicates(['Name'])
dffirst = dffirst.reset_index()
sep = '.com/'
for i in range(0,len(dffirst['Links'])):
    dffirst['Links'][i] = re.sub(r'.com/*', '.com// ', dffirst['Links'][i])
dffirst['Links'] = dffirst['Links'].str.split('/ ').str[0]

namel = dffirst['Name']
for i in range(0,len(namel)):
    namel[i] = namel[i].replace(" ","")
    namel[i] = namel[i].replace(".","")
    namel[i] = namel[i].lower()
namel = namel.str.split('(').str[0]

Good = []
ind = []
dffirstcopy = dffirst.copy()
for item in namel:
    for i in range(0,len(dffirst['Links'])):
        result = item in dffirst['Links'][i]
        if result is True:
            Good.append(dffirst.iloc[i])
            ind.append(i)
            dffirstcopy = dffirstcopy[~dffirstcopy['Name'].str.contains(item)]

pd.DataFrame(Good).to_excel('Goodtogo.xlsx', header=True, index=False)
dffirstcopy.to_excel('Needcheck.xlsx', header=True, index=False)

