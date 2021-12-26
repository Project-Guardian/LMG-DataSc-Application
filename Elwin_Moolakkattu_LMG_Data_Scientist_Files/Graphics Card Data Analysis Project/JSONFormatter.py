import json
import time
import numpy

CurrentTime = time.localtime()
CurrentTimeString = time.strftime('%Y-%m-%d %I-%M-%S %p', CurrentTime)
DictOfGPU = {}

File1 = "eBay/eBay3-USD-NON-AUCTION.json"
File2 = "eBay/eBay3-USD-AUCTION.json"
File3 = "eBay/eBay3-CAD-NON-AUCTION.json"
File4 = "eBay/eBay3-CAD-AUCTION.json"
File5 = "NewEgg/NewEgg.json"
#File6 = "ManualJSON/ManualConcat.json"


#InputFile = open(File5, 'r')
#MainFile = json.load(InputFile)
MainFile = {}
ListOfFiles = [File1, File2, File3, File4, File5]

for file in ListOfFiles:
    #print("--------------------------------------------------------------------------------------------")
    InputFile = open(file, 'r')
   
    MainInputFile = json.load(InputFile)
    MainFile.update(MainInputFile)



for UniqueID in MainFile:
    GPU = MainFile[UniqueID]["Chipset/GPU Model"]
    DictOfGPU[GPU] = {}
 
if "NA" in DictOfGPU:
    del DictOfGPU["NA"]
 
for GPUs in DictOfGPU:
    DictGPU = GPUs
    DictOfBrand = {}
    PriceList = []
    GPUCount = 0
    
    
    
    for UniqueID1 in MainFile:
        MainFileGPU = MainFile[UniqueID1]["Chipset/GPU Model"].lower()
        if MainFileGPU == DictGPU:  
            GPUCount = GPUCount + 1
            price = MainFile[UniqueID1]["price"]["amount"]
            price = float(price)
            priceCurr = MainFile[UniqueID1]["price"]["currency"]
            if priceCurr == "USD":
                price = price * 1.3
            PriceList.append(price)
    PriceList.sort()
    PriceListMean = numpy.mean(PriceList)
    PriceListMedian = numpy.median(PriceList)
    DictOfGPU[GPUs] = {"Prices" : str(PriceList), "PricesMean" : str(PriceListMean), "PricesMedian" : str(PriceListMedian), "GPUCount" : str(GPUCount)}

InputFile.close()

print("Saving JSON")      
with open("ALL-ConcatResults" + CurrentTimeString + ".json", 'w') as JSONDump:
    json.dump(DictOfGPU, JSONDump, indent=4, sort_keys=True)
print("Saving JSON Finished")
print("\n")