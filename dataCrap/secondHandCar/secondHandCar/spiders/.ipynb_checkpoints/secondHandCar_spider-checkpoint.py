import scrapy
import json
import csv
import math
import sys
import collections

def generateCityUrls(prefix,n):            
    # init the first url
    urls = [prefix+"1"]
    if n == 1:
        return urls

    for i in range(2,n+1):
        # those are parameters
        pn = str(i)
        lcr = str(20*(i-1))
        ldr = str(4*(i-1))
        new_url = prefix + pn + "&lcr=" + lcr + "&ldr=" + ldr + "&lir=0"
        #print("new url",new_url)
        urls.append(new_url)
    return urls
   
class SecondHandCarSpider(scrapy.Spider):
        
    name = "secondHandCar"
    allowed_domians = ["carwale.com"]
    handle_httpstatus_list = [404, 403, 401]
    count = 0
    start_urls = []
    large_city = []
    lastJsonString = ""
    with open('cityCount.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if int(row['CityCount']) >240:
                large_city.append(row['CityId'])
            else:
                cityId = row['CityId']
                prefix = "https://www.carwale.com/webapi/classified/stockfilters/?city="+cityId+"&pc="+cityId+"&car=17&pn="
                n = math.ceil(int(row['CityCount'])/24)
                start_urls += generateCityUrls(prefix,n)
            
    print("Larget city",large_city)
        
    if len(large_city) > 0 :
        for id in large_city:
            for color in range(13):
                colorStr = str(color+1)
                prefix = "https://www.carwale.com/webapi/classified/stockfilters/?color="+colorStr+"&city="+id+"&pc="+id+"&car=17&pn="
                start_urls += generateCityUrls(prefix,10)
     
    unique = set(start_urls)  
    for each in unique:  
        count = start_urls.count(each)  
        if count > 1:  
            print ('There are duplicates in this list')
    print ('There are no duplicates in this list') 
    
    
    sys.exit()
    
    def start_requests(self):
        default_header = {
            'Accept': 'text/plain, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-GB,en-US;q=0.8,en;q=0.6',
            'Connection':'keep-alive',
            'Cookie':'DesktopDetected=1; _abtest=54; _CustCityIdMaster=-1; _CustCityMaster=Select City; _CustAreaId=-1; _CustAreaName=Select Area; _CustZoneIdMaster=; _CustZoneMaster=Select Zone; UsedCarsCoachmark1=search|; UsedCarsVisitedCookie=Yes; __gads=ID=300af0cce669b221:T=1509118080:S=ALNI_MbDQg5hN9VT4cTMx3dDQlgyEfRjtA; __sonar=444744188529387198; AMP_TOKEN=%24NOT_FOUND; _gat_UA-337359-1=1; _ceg.s=oyhn7n; _ceg.u=oyhn7n; _tac=false~self|not-available; _ta=in~2~883b0730c9aff671d3164a84785f6825; _tas=9tp0rjab754; _ga=GA1.2.2016137387.1509118089; _gid=GA1.2.752781046.1509118089; CWC=WC7mOlYncFuZCKbxEpfdoyyXy; _cwv=WC7mOlYncFuZCKbxEpfdoyyXy.FN1D7HFE7L.1509118077.1509118382.1509118409.1; _cwutmz=utmcsr=(direct)|utmgclid=|utmccn=(direct)|utmcmd=(none); _uetsid=_uet19e45d2c',
            'Host':'www.carwale.com',
            'Referer':'https://www.carwale.com/used/cars-for-sale/',
            'sourceid':'1',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
            }
        for url in self.start_urls:
            yield scrapy.Request(url,headers=default_header, callback=self.parse)
            
    def parse(self,response):
        jsonString = response.body_as_unicode()
        if jsonString != self.lastJsonString :
            self.lastJsonString = jsonString 
            if jsonString.strip() != "":
                resultData = json.loads(jsonString)['ResultsData']
                if self.count == 0:
                    resultDataFile = open('rawData.csv', 'w')
                else:
                    resultDataFile = open('rawData.csv', 'a')

                csvwriter = csv.writer(resultDataFile)
                for result in resultData:
                    if self.count == 0:
                        header = result.keys()
                        csvwriter.writerow(header)
                    csvwriter.writerow(result.values())
                    self.count += 1
                resultDataFile.close()
                print('count',self.count)
            else:
                print("this url is wrong: "+response.url)


            