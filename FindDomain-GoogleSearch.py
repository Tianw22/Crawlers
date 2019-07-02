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
#df.to_excel('list-%s.xlsx'%today,header = True, index = False)

dfcopy = df.copy()
droplist = ['linkedin','bloomberg','glassdoor','crunchbase','wikipedia','facebook',
            'twitter','buzzfile','instagram','wiki','dictionary','owler','zoominfo',
            'indeed','None','yelp','datacentermap','issuu','dialogic','voip-info',
            'rozee','urdupoint','bbb','cortera','informa','yahoo','reuters',
            'prnewswire','hoovers','ipinfo','ripe','devex','myip','cypress',
            'contactout','vocabulary','macmillandictionary','coresite','youtube',
            'cloudscene','worldvoipproviders','rocketreach','techblog','customercarecontacts',
            'lookup','mvnoblog','cinando','albany','marinetechnologynews','mymediads','yellow-pages',
            'bgpview','ukessays','cloudsecurityalliance','voipproviderslist','yellowpages'
            'whitepages','today','voipfraud','news','.pdf','businessline','mobileworldlive','.edu',
            '/abs','.html','whirlpool','nameberry','peeringdb','dict.']
for item in droplist:
    dfcopy = dfcopy[~dfcopy.Links.str.contains(item)]
    
dffirst = dfcopy.drop_duplicates(['Name'])
dffirst = dffirst.reset_index()
sep = '.com/'
dflin = list(dffirst['Links'])
for i in range(0,len(dflin)):
    dffirst['Links'][i] = re.sub(r'.com/*', '.com// ', dflin[i])
dffirst['Links'] = dffirst['Links'].str.split('/ ').str[0]

dffirst.to_excel('comlist-%s-firstround.xlsx'%today)

namelist = dffirst['Name']
descrip = dffirst['Description']
namelist = namelist.str.split('(').str[0]
namel = list(namelist)
for i in range(0,len(namel)):
    namel[i] = namel[i].replace(" ","")
    namel[i] = namel[i].replace(".","")
    namel[i] = namel[i].replace("-","")
    namel[i] = namel[i].replace(",","")
    namel[i] = namel[i].lower()
    namel[i] = namel[i].replace("telecom","")
    namel[i] = namel[i].replace("communications","")
    namel[i] = namel[i].replace("international","")
    namel[i] = namel[i].replace("networks","")   
    namel[i] = namel[i].replace("inc","")
   
dffirstcopy = dffirst.copy()
linkori = list(dffirstcopy['Links'])
linkl = list(dffirstcopy['Links'])
for i in range(0,len(linkl)):
    linkl[i] = linkl[i].replace("http://","")
    linkl[i] = linkl[i].replace("https://","")
    linkl[i] = linkl[i].replace("www.","")
linkldf = pd.DataFrame(linkl)

newlist = linkldf[0].str.split('.').str[0]

Gnlist = []
GInd = []
Good = []
Gdes = []
for i in range(0,len(newlist)):
    for j in range(0,len(namel)):
        if namel[j] in newlist[i]:
            GInd.append(j)
            Gnlist.append(namelist[j])
            Gdes.append(descrip[i])
            Good.append(linkori[i])
Goodlist = {"Name":Gnlist,"Link":Good,"Des":Gdes}
Gooddf = pd.DataFrame(Goodlist)

Gooddfout = Gooddf.drop_duplicates(keep=False,subset='Link')
Gooddfout.to_excel('GoodLinks%s.xlsx'%today)


Alllist = {"Name":namelist,"Link":linkori,"Des":descrip}
Alllist = pd.DataFrame(Alllist)
Newlist = Alllist.append(Gooddfout, ignore_index = True)
NClist = Newlist.drop_duplicates(keep=False)
NClist.to_excel('Needcheck%s.xlsx'%today, header=True, index=False)
