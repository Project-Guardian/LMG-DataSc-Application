import os
import json
import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup

InitURL = "https://www.newegg.ca/p/pl?N=100007708%20601357282"

DirName = "NewEgg"
FileName = "NewEgg"
SaveTo = DirName + '/'
main_list_of_links = []
LinksCounter = 0

def VisitFirstLink(SomeLink, SomeList, SomeCounter):
    #print("VisitFirstLink called")
    session = HTMLSession()
    page = requests.get(SomeLink, allow_redirects=True)
    #page = session.get(SomeLink, allow_redirects=True)    
    print(page)
    data = page.text
    print(data)
    soup = BeautifulSoup(data, "html5lib")
    print(soup)

    print("CreateListOfLinks called")
    for link in soup.find_all(class_="item-title"):
        ProductPageLink = link.get('href')
        responseN = CreateListOfLinks(ProductPageLink, SomeList)
        SomeCounter = SomeCounter + responseN
    
    print("Total number of non-duplicate links so far: ", SomeCounter)
    print("\n")

    return
    

def CreateListOfLinks(SomeLinkToAddToList, SomeList):
    if SomeLinkToAddToList in SomeList:
        n = 0
    if SomeLinkToAddToList not in SomeList:
        SomeList.append(SomeLinkToAddToList)
        n = 1
    return n
       
       
def ScrapeProductPage(SomeList, SomeFile, SomePath):
    #print("ScrapeProductPage called")
    Dict = PageDetails(SomeList)
    print("\n")
    StoreJSONResultsLocally(Dict, SomeFile, SomePath)
    
    
def PageDetails(SomeList):
    #print("PageDetails called")
    DictNonAuction = {}
    n = 0
    
    for link in SomeList: 
        n = n + 1
        print("Scraping link", n )
        unique_id = link.split('/')[5]
        
        page = requests.get(link, allow_redirects=True)
        data = page.text
        soup = BeautifulSoup(data, "html5lib")
    
        MANU = BRAND = MEM = GPU = UPC = PRICE = "NA"
        
        PRICEMAIN = soup.find(class_="price-current-label")
        PRICE = PRICEMAIN.find_next_sibling("strong").text.replace(',', '') + PRICEMAIN.find_next_sibling("sup").text

        print("\n")
        for cat in soup.find_all("th"):
            ########### Brand
            if (cat.text.strip() == "Brand"):
                BRAND = cat.find_next_sibling().text.strip()
            ########### Chipset Manufacturer    
            if (cat.text.strip() == 'Chipset Manufacturer'):
                MANU = cat.find_next_sibling().text.strip() 
            ########### Memory Size
            if (cat.text.strip() == 'Memory Size'):
                MEM = cat.find_next_sibling().text.strip()
                MEM = MEM.replace(" ", "")
                if "GB" not in MEM:
                    MEM = MEM + "GB"
            ########### Chipset/GPU Model
            if (cat.text.strip() == 'GPU'):
                GPU = (cat.find_next_sibling().text.strip()).lower()
                GPU = GPU.lstrip("nvidia geforce rtx")
                GPU = GPU.lstrip("geforce rtx")
            ########### UPC
            if (cat.text.strip() == 'Model'):
                UPC = cat.find_next_sibling().text.strip()

            Data = {"Chipset/GPU Model" : GPU, "auction" : "False", "price" : { "amount" : PRICE , "currency" : "CAD" },"manufacturer" : MANU, "brand" : BRAND, "memory" : MEM, "upc" : UPC, "link number" : str(n), "link" : link, "vendor" : "NewEgg"}
            DictNonAuction[unique_id] = Data
    
    print("\n")
    #print(json.dumps(DictNonAuction, indent=4))
    return DictNonAuction
    

def CreateDir(SomeDirName):
    #print("CreateDir called")
    try:
        os.mkdir(SomeDirName)
        print("Directory " , SomeDirName,  " Created ") 
    except FileExistsError:
        print("Directory " , SomeDirName,  " Already Exists")
    print("\n")


def StoreLinksResultsLocally(SomeList, SomeFile, SomePath):
    #print("StoreLinksResultsLocally called")
    print("Saving Links")
    n = 0
    SomeCounter = len(SomeList)
    outT = open(SomePath + SomeFile + ".txt", 'w')
    
    outT.write("The link count is: ") 
    outT.write(str(SomeCounter))
    outT.write("\n")
    
    for i in SomeList:
        n = n + 1
        outT.write("\n")
        outT.write(str(n).zfill(4) + " - " + i)
    outT.close()
    print("Saving Links Finished")
    print("\n")
    
    
def StoreJSONResultsLocally(SomeDICTData, SomeFile, SomePath):
    #print("StoreJSONResultsLocally called")
    print("Saving JSON for: " + SomeFile)
        
    with open(SomePath + SomeFile + ".json", 'w') as JSONDump:
        json.dump(SomeDICTData, JSONDump, indent=4)
    print("Saving JSON Finished for: " + SomeFile)
    print("\n")

print("------------------------------------------------------------------------------------------------------------")
CreateDir(DirName)
VisitFirstLink(InitURL, main_list_of_links, LinksCounter)
StoreLinksResultsLocally(main_list_of_links, FileName, SaveTo)
ScrapeProductPage(main_list_of_links, FileName, SaveTo)