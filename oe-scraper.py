import requests
import lxml.html as lh
import pandas as pd


url = 'http://openinsider.com/screener?s=&o=&pl=&ph=&ll=&lh=&fd=730&fdr=&td=1&tdr=&fdlyl=&fdlyh=&daysago=&xs=1&vl=5&vh=&ocl=&och=&sic1=-1&sicl=100&sich=9999&isceo=1&iscfo=1&grp=0&nfl=&nfh=&nil=&nih=&nol=&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=0&cnt=100&page=1'

#Create a handle, page, to handle the contents of the website
page = requests.get(url)

#store the contents of the website under doc
doc = lh.fromstring(page.content)

#parse data that are stored between the rows of html
tr_elements = doc.xpath('//table[@class="tinytable"]//tr')

col=[]
i=0

#for each row, store each first element(header) and an empty list
for elem in tr_elements[0]:
    i+=1
    name=elem.text_content()
    # print(str(i)+' ' + name)   ---- this will print out the header for ea col
    col.append((name, []))

for elem in range(1, len(tr_elements)):
    #T is our index'th row
    T = tr_elements[elem]

    #If row is not of size 17, the //tr data is not from our table
    if len(T) != 17:
        print('breaking because the size is not right')
        break

    #i is the index of our column
    i=0

    #Iterate thorugh each elem of the row
    for t in T.iterchildren():
        data=t.text_content()

        #Check if row is empty
        if i > 0:
            #Convert any numerical value to integers
            try:
                data = int(data)
            except:
                pass

        #Append the data to the empty list of the i'th column
        col[i][1].append(data)
        #Increment i for the next column
        i+=1

Dict = {title:column for (title, column) in col}
df = pd.DataFrame(Dict)
print(df)