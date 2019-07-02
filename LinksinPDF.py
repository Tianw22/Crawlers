import PyPDF2
import pandas as pd
import re

pdfFileObj = open('xxxxxxx.pdf', 'rb') 
pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 

# Read the PDF from page 32 to 158.
for i in range(32,158):   
    pageObj = pdfReader.getPage(i) 
    detail = pageObj.extractText() 
    outF = open("addout.txt", "a")
    try:
        outF.write(detail)
        outF.write("\n")
    except UnicodeEncodeError:
        pass
outF.close()
pdfFileObj.close()

l = []
with open('addout.txt') as f:
    datafile = f.readlines()
    for line in datafile:
        if 'www' in line:
            l.append(line)
ldf = pd.DataFrame(l)

# Clean data. 
p1 = re.compile(r'[(](.*)', re.S) 
nam = []
for i in range(0,len(ldf[0])):
    item = re.sub(r'www*', '(www', ldf[0][i])
    pp = re.findall(p1, str(item))
    nam.append(pp)
comnam = pd.DataFrame(nam)
comnam[0] = comnam[0].str.split('\n').str[0]

companylist = pd.read_excel('newfile.xlsx') #Excel from TablefromPDF.py 
links = []
cll = companylist['NameLo']
cll = cll.str.split('international').str[0]
cll = cll.str.split('telecom').str[0]
linklist = list(comnam[0])
for i in range(0,len(cll)):
    ele = str(cll[i])
    if any(ele in s for s in linklist):
        matching = [s for s in linklist if ele in s]
        links.append(matching)
    else:
        links.append('null')
        
pd.DataFrame(links).to_excel('PDFlinks.xlsx') # Links match the excel.
pd.DataFrame(comnam).to_excel('PDFalllinks.xlsx') # All the links in the PDF.
