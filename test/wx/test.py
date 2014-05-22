from ptpy import PtCurl
import json
curl = PtCurl(debug=True,proxy="127.0.0.1:8888")
APPID = "wxa19b2bb098f2de68"
APPSECRET = "3c75f718d59de9403672304d8b0d94ff"
url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid="+APPID+"&secret="+APPSECRET

res = curl.get(url)
access_token = json.loads(res)['access_token']
print access_token