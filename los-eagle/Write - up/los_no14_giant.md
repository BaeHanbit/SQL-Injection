## Lord of SQL Injection No. 14 - Giant
## 문제 출제 의도
1. strlen 함수를 이해하는지 확인.
2. 공백을 우회 가능한지 확인.
## 소스 코드 분석
+ 소스 코드  
Giant소스 코드는 다음과 같다.   
    ~~~ 
    <?php 
    include "./config.php"; 
    login_chk(); 
    dbconnect(); 
    if(strlen($_GET[shit])>1) exit("No Hack ~_~"); 
    if(preg_match('/ |\n|\r|\t/i', $_GET[shit])) exit("HeHe"); 
    $query = "select 1234 from{$_GET[shit]}prob_giant where 1"; 
    echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
    $result = @mysql_fetch_array(mysql_query($query)); 
    if($result[1234]) solve("giant"); 
    highlight_file(__FILE__); 
    ?>
    ~~~
+ 소스 코드 분석
    - 금지 문자, 문자열
        * Get 방식으로 받은 shit값에  ' '공백, '\n'개행, '\r', '\t'(탭)중 하나라도 있다면 "HeHe"이 출력되고 문제 풀이에 실패한다.
        * GET방식으로 받은 shit값의 크기가 2
        - SQL문을 통해 받은 결과 값이 0이 아니라면 문제 풀이에 성공한다.
## 문제 해결
+ carrage return
    - 이는 공백을 대신하지만 preg_match에 걸리지 않음으로 정상적으로 결과값을 데이터베이스에서 가져올 수 있다.
    - 따라서 다음과 같은 추가 문자열을 URL 뒤에 추가하면 문제 풀이에 성공한다.
    ~~~
    ?shit=%0b
    ~~~