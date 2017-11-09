# Lord of SQL Injection No.5 - Wolfman
## 문제 출제 의도
1. ' '(공백)없이 쿼리를 조작하여 해결 할 수 있는지 확인.
## 소스 코드  
~~~
<?php 
    include "./config.php"; 
    login_chk(); 
    dbconnect(); 
    if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~"); 
    if(preg_match('/ /i', $_GET[pw])) exit("No whitespace ~_~"); 
    $query = "select id from prob_wolfman where id='guest' and pw='{$_GET[pw]}'"; 
    echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
    $result = @mysql_fetch_array(mysql_query($query)); 
    if($result['id']) echo "<h2>Hello {$result[id]}</h2>"; 
    if($result['id'] == 'admin') solve("wolfman"); 
    highlight_file(__FILE__); 
?>
~~~
##분석 결론
+ 금지 문자, 문자열
    - GET방식으로 입력받은 pw값에 prob _ . () 중 하나라도 있다면 "No Hack ~_~"이 출력되고 문제 풀이에 실패한다.
    - GET방식으로 받은 pw값에 공백이 있으면 "No whitespace ~_~"이 출력되고 문제풀이에 실패한다.
+ 풀이 성공 조건
    - 데이터베이스에서 받아온 id 값이 'admin'이면 문제 풀이에 성공한다.
## 문제 해결
1. Query문 추가
    - 공백을 우회하는 방법으로는 다음과 같은 값들이 있다.
        1. CR(Carriage Return) =  0x0D
        2. LF(Line Feed) = 0x0A
        3. Tab 이용 = 0x09
        4. 주석 이용 = /**/
        5. form feed = 0x0C
    - 따라서 다음과 유사한 방법으로 문제를 해결 할 수 있다.
    ~~~
    ?pw='%0Dor%0Did='admin'--%0D-
    ~~~