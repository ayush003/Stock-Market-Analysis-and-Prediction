import csv  # file operations
from bs4 import BeautifulSoup  # lib for pulling data from html/xmlsites
from urllib.request import urlopen

for i in range(1,2): # lib for sending and rec info over http
    Url = 'http://www.moneycontrol.com/stocks/hist_stock_result.php?sc_id=UTI10&pno='+str(i)+'2&hdn=daily&fdt=2015-01-01&todt=2019-01-01'
    pageHtml = urlopen(Url)
    soup = BeautifulSoup(pageHtml,"html.parser")
    table = soup.find_all("table", { "class" : "tblchart" })
    with open('hdfc.csv', 'a',newline='') as csvfile:
        f = csv.writer(csvfile)
        f.writerow(['Date','Open','High','Low','Close','Volume','Spread'])  # headers
        for x in table:
            rows = x.find_all('tr') #find all tr tag
            print(rows)
            for tr in rows:
                data=[]
                cols = tr.find_all('td') #find all td tags
                for td in cols:
                    data.append(td.text.strip()) 
                f.writerow(data)
        csvfile.close()
