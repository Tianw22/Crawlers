#Save tables in pdf into excel.
#把PDF中的表格存为excel.

#Import packages.
import pdfplumber
import pandas as pd
from titlecase import titlecase

#Import PDF file
pdf = pdfplumber.open("xxxxxxxx.pdf")

#Save the 1st column and the 9th column.
def savetable(pagenum):
    p0 = pdf.pages[pagenum]
    table = p0.extract_table()
    df = pd.DataFrame(table)
    l1 = df[0]
    l2 = df[8]
    return l1, l2
    
list1 = []
list2 = []
#Save the tables from page 5 to page 33.
for i in range(5,33):
    try:
        l1,l2 = savetable(i)
        list1.extend(l1)
        list2.extend(l2)
    except (IndexError, KeyError) as e:
        pass
        
dfall = {"Name":list1,"Location":list2}
dfall = pd.DataFrame(dfall).reset_index()

#Save all the rows contains "(cid:126)" in column "Location".
dfnew = dfall[dfall.Location.str.contains("(cid:126)",na=False)]

dfnew = dfnew.reset_index()
for i in range(0,len(dfnew['Name'])):
    dfnew['Name'][i] = titlecase(dfnew['Name'][i])

pd.DataFrame(dfnew['Name']).to_excel("newfile.xlsx")
