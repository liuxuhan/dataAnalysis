import scrapy
import json
import csv
import math

class CitySpider(scrapy.Spider):
    
    name = "citySpider"
    allowed_domians = ["carwale.com"]
    handle_httpstatus_list = [404, 403, 401]
    url = "https://www.carwale.com/webapi/classified/stockfilters/?car=17&pn=1"
    count = 0
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
        yield scrapy.Request(self.url,headers=default_header, callback=self.parse)
            
    def parse(self,response):
        resultData = json.loads(response.body_as_unicode())['FiltersData']['city']
        resultDataFile = open('cityCount.csv', 'w')
        csvwriter = csv.writer(resultDataFile)
        for result in resultData:
            if result['CityId'] == 9999:
                continue
            if self.count == 0:
                header = result.keys()
                csvwriter.writerow(header)
            csvwriter.writerow(result.values())
            self.count += 1
        resultDataFile.close()

        
   
            