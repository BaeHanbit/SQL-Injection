# Lord of SQL Injection No. 9 - vampire
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
    - 금지 문자, 문자열
        * Get 방식으로 받은 문자열에 'prob _ . ( )중 하나라도 있다면 "No Hack~_~"이 출력되고 문제 풀이에 실패한다.
    - str_replace()함수
        * str_replace함수는 다음과 같은 형식을 취한다.
        ~~~
        mixed str_replace ( mixed $search , mixed $replace , mixed $subject)
        ~~~
        * subject에서 발견한 모든 search를 주어진 replace 값으로 치환한 문자열이나 배열을 반환합니다.
## 문제 해결
+ str_replace함수
    - MySQL은 기본적으로 대소문자 구별을 하지 않는다. 
    - PHP는 문법을 제외하고 대소문자를 구별한다.
    - 따라서 다음고 같이 값이 입력될 경우...
    ~~~
    str_replace("admin","","Admin")
    ~~~
    - Admin을 반환하게 된다.
+ SQL Injection
    - 따라서 다음과 같은 문자열을 URL뒤에 추가하여 문제 해결이 가능하다.
    ~~~
    ?id=Admin
    ~~~
    - 즉 admin중에 한 문자 이상이 대문자가 되면 문제 해결이 가능하다.
