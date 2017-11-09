## Lord of SQL Injection No. 14 - Giant
## 문제 출제 의도
1. strlen 함수를 이해 여부를 확인.
2. 아스키 코드의 이해 여부를 확인.
## 소스 코드 
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
## 소스 코드 분석
+ strlen
    - strlen 함수는 다음과 같은 형식을 취한다.
    ~~~
    int strlen ( string $string )
    ~~~
    - 주어진 string의 길이를 반환한다.
    - strlen함수에 대해 잘 모르겠다면 다음 사이트를 참고하자.  
    <a href="http://php.net/manual/kr/function.strlen.php">PHP: strlen - Manual</a>
## 분석 결론
+ 금지 문자, 문자열
    - Get 방식으로 받은 shit값에  ' '공백, '\n'개행, '\r', '\t'(탭)중 하나라도 있다면 "HeHe"이 출력되고 문제 풀이에 실패한다.
    - GET방식으로 받은 shit값의 크기가 2이상이라면 "No Hack ~_~"을 출력하고 문제 풀이에 실패한다.
+ 풀이 성공 조건
    - 입력한 shit에 값이 있다면 문제 풀이에 성공한다.
## 문제 해결
1. ASCII 
    - carrage return
        * 이는 공백을 우회 가능하다.
        * 따라서 다음과 유사한 방법으로 문제 풀이에 성공 할 수 있다.
        ~~~
        ?shit=%0b
        ~~~
    - Form Feed
        * 이는 공백을 우회 가능하다.
        * 따라서 다음과 유사한 방법으로 문제 풀이에 성공 할 수 있다.
        ~~~
        ?shit=%0c
        ~~~