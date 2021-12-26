import os
import json
import requests
import time
from requests_html import HTMLSession
from requests_html import AsyncHTMLSession
from bs4 import BeautifulSoup

InitURL="https://www.ebay.ca/sch/i.html?_from=R40&_nkw=%28%22rtx+3060%22%2C+%22rtx+3060+ti%22%2C+%22rtx+3070%22%2C+%22rtx+3070+ti%22%2C+%22rtx+3080%22%2C+%22rtx+3090%22%29+-bezel+-2060+-gtx+-2070+-2080+-PC+-workstation+-laptop+-NVlink+-link+-bridge+-quadro+-block+-backplate+-motherboard+-fan+-mounts+-mount+-watercooler+-kit+-fans+-adapter+-cable+-magazine+-T-shirt+-baffle+-bracket&_sacat=27386&LH_TitleDesc=0&_pgn=1&_ipg=200"
DirName = "eBay"
FileName = "eBay"
SaveTo = DirName + '/'
main_list_of_links = []
LinksCounter = 0
CurrentTime = time.localtime()
CurrentTimeString = time.strftime('%Y-%m-%d %I-%M-%S %p', CurrentTime)



def VisitFirstLink(SomeLink, SomeList, SomeFile, SomePath, SomeCounter):
    print("VisitFirstLink called")
    
    #HTMLSession not working
    session = HTMLSession()
    page = requests.get(SomeLink, allow_redirects=True)    
    data = page.text
    soup = BeautifulSoup(data, "html5lib")
       

    print("CreateListOfLinks called")
    for link in soup.find_all(class_="s-item__link"):
        ProductPageLink = link.get('href')
        responseN = CreateListOfLinks(ProductPageLink, SomeList)
        SomeCounter = SomeCounter + responseN
    
    print("Total number of non-duplicate links so far: ", SomeCounter)
    print("\n")

    try:
        NextPageClass = soup.find(class_="pagination__next")
        print("looking for next page")
        NextPageLink = NextPageClass.get('href')
        NextPageTrue = NextPageClass.get('aria-disabled')
    except:
        NextPageTrue = True
        
    if NextPageTrue == None:
        print("visting...")
        VisitFirstLink(NextPageLink, SomeList, SomeFile, SomePath, SomeCounter)
    else:
        print("returning")
        return

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
    
    Auction, NonAuction, ErrorCount = PageDetails(SomeList, "CAD")
    print("\n")
    StoreJSONResultsLocally(Auction, SomeFile + "-CAD-AUCTION", SomePath)
    StoreJSONResultsLocally(NonAuction, SomeFile + "-CAD-NON-AUCTION", SomePath)
    
    Auction, NonAuction, ErrorCount = PageDetails(SomeList, "USD")
    print("\n")
    StoreJSONResultsLocally(Auction, SomeFile + "-USD-AUCTION", SomePath)
    StoreJSONResultsLocally(NonAuction, SomeFile + "-USD-NON-AUCTION", SomePath)
    
    print(ErrorCount, " links were skipped due to price/ currency error")
    
def PageDetails(SomeList, SomeCurrency):
    #print("PageDetails called")
    DictAuction = {}
    DictNonAuction = {}
    n = 0
    ErrorCount = 0
    
    for link in SomeList: 
        n = n + 1
        print("Scraping link and checking for: " + SomeCurrency + " in link ", n )
        unique_id_pre = link.split('?')[0]
        unique_id = unique_id_pre.split('/')[5]
    
        page = requests.get(link, allow_redirects=True)
        data = page.text
        soup = BeautifulSoup(data, "html5lib")
    
        MANU = BRAND = MEM = GPU = GPU1 = UPC = "NA"
        try:
            try:
                PRICE = soup.find(id='prcIsum')['content']
                Auction = False
            except:
                PRICE = soup.find(id='prcIsum_bidPrice')['content']
                Auction = True
        except:
            PRICE = "NA"
            ErrorCount = ErrorCount + 1
            print("price error in: ", n)
        
        try:
            PRICECUR = soup.find(itemprop='priceCurrency')['content']
        except:
            PRICECUR = "NA"
            ErrorCount = ErrorCount + 1
            print("price currency error in: ", n)
        
        if PRICECUR == SomeCurrency:
            for cat in soup.find_all('td', class_='attrLabels'):
                ########### Chipset Manufacturer
                if (cat.text.strip() == 'Chipset Manufacturer:'):
                    MANU = cat.find_next_sibling().text.strip() 
                ########### Brand
                if (cat.text.strip() == 'Brand:'):
                    BRAND = cat.find_next_sibling().text.strip()
                ########### Memory Size
                if (cat.text.strip() == 'Memory Size:'):
                    MEM = cat.find_next_sibling().text.strip()
                    MEM = MEM.replace(" ", "")
                    if "GB" not in MEM:
                        MEM = MEM + "GB"
                ########### Chipset/GPU Model
                if (cat.text.strip() == 'Chipset/GPU Model:'):
                    GPU = (cat.find_next_sibling().text.strip()).lower()
                    gpusplit = GPU.split()
                    ti = ""
                    for x in gpusplit:
                        if x == "ti":
                            ti = " " + x
                        if x == "3060":
                            GPU1 = x
                        if x == "3070":
                            GPU1 = x
                        if x == "3080":
                            GPU1 = x
                        if x == "3090":
                            GPU1 = x
                    GPU = GPU1 + ti
                ########### UPC
                if (cat.text.strip() == 'UPC:'):
                    UPC = cat.find_next_sibling().text.strip()
                
                Data = {"Chipset/GPU Model" : GPU, "auction" : str(Auction), "price" : { "amount" : PRICE , "currency" : PRICECUR },"manufacturer" : MANU, "brand" : BRAND, "memory" : MEM, "upc" : UPC, "link number" : str(n), "link" : link, "vendor" : "Ebay"}
                if Auction == False:
                    DictNonAuction[unique_id] = Data
                if Auction == True:
                    DictAuction[unique_id] = Data      
    print("\n")
    return DictAuction, DictNonAuction, ErrorCount
    

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
    outT = open(SomePath + SomeFile + CurrentTimeString + ".txt", 'w')
    
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
        
    with open(SomePath + SomeFile + CurrentTimeString + ".json", 'w') as JSONDump:
        json.dump(SomeDICTData, JSONDump, indent=4)
    print("Saving JSON Finished for: " + SomeFile)
    print("\n")

print("------------------------------------------------------------------------------------------------------------")
CreateDir(DirName)
VisitFirstLink(InitURL, main_list_of_links, FileName, SaveTo, LinksCounter)
StoreLinksResultsLocally(main_list_of_links, FileName, SaveTo)
ScrapeProductPage(main_list_of_links, FileName, SaveTo)