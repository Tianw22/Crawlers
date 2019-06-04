#安装！！！
#pip install git+https://github.com/abenassi/Google-Search-API
from google import google
import pandas as pd

#Search the elements in cdnlist-name.csv one by one in Google.com.
#Save the searching results in Google.com (Links and descriptions) 
#在Google中搜索表格中所有元素，并存储Google查询结果的第一页中的链接以及链接的描述。
df = pd.read_csv('cdnlist-name.csv')
df = pd.DataFrame(df)
num_page = 1
des = []
lin = []
a = 1
for i in df['Name']:
    search_results = google.search("%s"%i, num_page)
    for result in search_results:
        de = result.description
        de = str(i + str(de))
        li = result.link
        li = str(li)
        des.append(de)
        lin.append(li)
    print("This is the %i record"%a)
    a = a+1
Total = {"Description":des,"Links":lin}
df = pd.DataFrame(Total)
df.to_csv('searchresults.csv')
