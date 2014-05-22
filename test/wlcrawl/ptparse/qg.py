from ptpy import PtCurl
import urllib
import pprint
import pycurl
import json

url = "http://book.citilink.co.id/Search.aspx"

curl = PtCurl(debug = False,proxy = "127.0.0.1:8888")

data = "__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE=%2FwEPDwUBMGRkBsrCYiDYbQKCOcoq%2FUTudEf14vk%3D&pageToken=&AvailabilitySearchInputSearchVieworiginStation1=LOP&AvailabilitySearchInputSearchView%24TextBoxMarketOrigin1=LOP&AvailabilitySearchInputSearchViewdestinationStation1=SUB&AvailabilitySearchInputSearchView%24TextBoxMarketDestination1=SUB&AvailabilitySearchInputSearchVieworiginStation2=&AvailabilitySearchInputSearchView%24TextBoxMarketOrigin2=&AvailabilitySearchInputSearchViewdestinationStation2=&AvailabilitySearchInputSearchView%24TextBoxMarketDestination2=&AvailabilitySearchInputSearchView%24DropDownListMarketDay1=11&AvailabilitySearchInputSearchView%24DropDownListMarketMonth1=2014-9&date_picker=2014-9-20&AvailabilitySearchInputSearchView%24DropDownListMarketDay2=07&AvailabilitySearchInputSearchView%24DropDownListMarketMonth2=2014-9&date_picker=2014-9-20&AvailabilitySearchInputSearchView%24RadioButtonMarketStructure=OneWay&AvailabilitySearchInputSearchView%24DropDownListPassengerType_ADT=1&AvailabilitySearchInputSearchView%24DropDownListPassengerType_CHD=0&AvailabilitySearchInputSearchView%24DropDownListPassengerType_INFANT=0&AvailabilitySearchInputSearchView%24DropDownListSearchBy=columnView&AvailabilitySearchInputSearchView%24ButtonSubmit=Find+Flights"
res = curl.post(url, data,{
    pycurl.FOLLOWLOCATION:1
})
print curl.EFFECTIVE_URL
res = curl.get("http://book.citilink.co.id/ScheduleSelect.aspx")
print res
