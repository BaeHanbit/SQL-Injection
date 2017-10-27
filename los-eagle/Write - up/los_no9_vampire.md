# Lord of SQL Injection No. 8- troll
## 문제 출제 의도
str_replace 함수를 이해하고 있는지 확인한다.
## 소스 코드 분석
+ 소스 코드
vampire의 소스 코드는 다음과 같다.
    ~~~
    <?php 
    include "./config.php"; 
    login_chk(); 
    dbconnect(); 
    if(preg_match('/\'/i', $_GET[id])) exit("No Hack ~_~"); 
    $_GET[id] = str_replace("admin","",$_GET[id]); 
    $query = "select id from prob_vampire where id='{$_GET[id]}'";
    echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
    $result = @mysql_fetch_array(mysql_query($query)); 
    if($result['id'] == 'admin') solve("vampire"); 
    highlight_file(__FILE__); 
    ?>
    ~~~
+ 소스 코드 분석
    - Get 방식으로 받은 문자열에 'prob _ . ( )중 하나라도 있다면 "No Hack~_~"이 출력되고 문제 풀이에 실패한다.
    - str_replace()함수
    ~~~
    str_replace("찾을문자열","치환할문자열","대상문자열");
    ~~~
## 문제 해결
+ GET 방식으로 받은 문자열이 MySql에서 'admin'과 비교했을 때 달라야 한다.
+ GET 방식으로 받은 문자열이 php에서 'admin'과 비교했을때 동일해야 한다.
+ 따라서 대문자를 섞어서 id로 주면 문제가 해결된다.
~~~
?id=Admin
~~~