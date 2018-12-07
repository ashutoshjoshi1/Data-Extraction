import requests
from bs4 import BeautifulSoup
import time
import numpy
import pandas as pd

baseURL = "http://www.indianhindunames.com/alphabetical-order-indian-names.htm"

def ExtractWebPage(url):
    r = requests.get(url)
    Page = BeautifulSoup(r.text,"html.parser")
    return Page,r 

def ExtractLinks(baseURL):
    Page,r = ExtractWebPage(baseURL)
    Page =  Page.findAll("div",{"class":"txtcontent"})
    boy_names_links = []
    girl_names_links = []
    itera = 0
    for elements in Page:
        for cat in elements.findAll("ul"):
            links = []
            for link in cat.findAll('a'):
                s = "http://www.indianhindunames.com/" +  link.get("href")
                links.append(s)
            if itera == 0:
                girl_names_links = links[:]
                itera = 1
            else:
                boy_names_links = links[:]
    return girl_names_links, boy_names_links

def ExtractNames(link):
    nameList = []
    Page,r = ExtractWebPage(link)
    time.sleep(1)
    print(link, r)
    l = Page.findAll("div", {"id":"bodyleft", "class": "txtcontent"})
    time.sleep(0.5)
    for each in l:
        f = each.find_all("p")
        for cat in f:
            #print(cat)
            names = cat.text.splitlines()
            names = [i.strip().split("=")[0] for i in names]
            #print(names)
            if len(names) > 1 and set(names).issubset(set(nameList)) == False:
                nameList.extend(names)
            if len(names) == 1 and set(names).issubset(set(nameList)):
                nameList.remove(names[0])
    list_to_remove = ['', '(adsbygoogle ',]
    nameList= list(set(nameList).difference(set(list_to_remove)))
    return nameList


girl_names_links, boy_names_links = ExtractLinks(baseURL)
nameListGirl = []
for link in girl_names_links:
    nameListGirl.extend(ExtractNames(link))
print(nameListGirl)

nameListBoy = []
for link in boy_names_links:
    nameListBoy.extend(ExtractNames(link))
print(nameListBoy)


print(len(nameListBoy), len(nameListGirl))

girl = ["girl" for _ in range(2109)]
boy = ["boy" for _ in range(2299)]

labels = numpy.array(girl[:] + boy[:])
names = numpy.array(nameListGirl + nameListBoy)

d = {'names': names, 'labels': labels}

df = pd.DataFrame(data=d)
df.to_csv("data"+".csv", index=False, header=True)