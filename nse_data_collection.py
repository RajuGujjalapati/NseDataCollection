from datetime import date, timedelta
import urllib.request
from urllib.parse import urlparse
from pathlib import Path
from zipfile import ZipFile
import os
import pandas as pd
import glob

current_date = date.today() 
days_before = (date.today()-timedelta(days=30))

for x in range(30):
    #Enter the required number of days.
    days_before = (date.today()-timedelta(days=x+1))
    print(x+1," day(s) before current date: ",days_before)
    print("Day in Number :", days_before.day, end=" ")
    print("Day in Name :", days_before.strftime("%A"), end=" ")
    print("Month in Number :", days_before.month, end=" ")
    print("Month in Name :", days_before.strftime("%b"), end=" ")
    print("Year :", days_before.year, end=" ")

    dayName = days_before.strftime("%A")
    nseDate = days_before.day
    nseMonth = days_before.strftime("%b").upper()
    nseYear = days_before.year
    
    #nse_Data(dayName, nseDate, nseMonth, nseYear)
    #extract(acb, xyz)

    if dayName=='Saturday' or dayName=='Sunday':
       continue

    fileName = str(nseDate)+str(nseMonth)+str(nseYear)
    
    URLString = "https://archives.nseindia.com/content/historical/EQUITIES/"+str(nseYear)+"/"+str(nseMonth)+"/cm"+fileName+"bhav.csv.zip"

    fileURL = urlparse(URLString).geturl()
    print("URL Type : ",type(fileURL))
    
    print("URL To be downloaded : " + fileURL)
 
    ZIPFileDir = "NSEZipFiles"
    Path(ZIPFileDir).mkdir(parents=True, exist_ok=True)
    try:
        nseFile = urllib.request.urlretrieve(fileURL,ZIPFileDir+"/"+fileName+".zip")
    except:
        print("No File Found For :",fileName)


ZIPFileDir = "NSEZipFiles"
UnZipFileDir = "NSECSVFiles"
#unzipping folder

Path(UnZipFileDir).mkdir(parents=True, exist_ok=True)

for subdir,dir,files in os.walk(ZIPFileDir):
    for csvFile in files :
        fileDir = f=os.path.join(subdir, csvFile)
        with ZipFile(fileDir, 'r') as zip:
            zip.extractall(UnZipFileDir)

path = UnZipFileDir
allCSVFiles = glob.glob(path + "/*.csv")

li = []
colNames = ["SYMBOL","SERIES","OPEN","HIGH","LOW","CLOSE","LAST","TOTTRDQTY","TIMESTAMP"]
for eachFile in allCSVFiles:

    df = pd.read_csv(eachFile,index_col=None, header=0,usecols=colNames)
    df = df
    li.append(df)
    frame = pd.concat(li,axis=0,ignore_index=True)
    sortedFrame = frame.sort_values(["SYMBOL","TIMESTAMP"])
    sortedFrame.to_csv("FinalCSV.csv",index=None)



