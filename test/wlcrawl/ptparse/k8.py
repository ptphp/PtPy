
from ptpy import PtCurl
import urllib
import pprint
import json

url = "http://www.kanairlines.com/ebooking/index.php?c=service&m=execute&ctl=flight-booking"

curl = PtCurl(debug = True,proxy = "127.0.0.1:8888")

query = {
         "xaction":"readDepart",
         "rows":'{"departDate":"27/04/2014","routeFrom":"CNX","routeTo":"NNT","seat":1}'
         }

data = urllib.urlencode(query)
res = curl.post(url, data)

print res
pprint.pprint(json.loads(res))