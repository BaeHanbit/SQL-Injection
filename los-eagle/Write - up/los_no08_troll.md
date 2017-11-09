# Lord of SQL Injection No. 8 - Troll
## 문제 출제 의도
1. ereg함수의 취약점의 이해 여부 확인.
## 소스 코드
~~~
<?php  
    include "./config.php"; 
    login_chk(); 
    dbconnect(); 
    if(preg_match('/\'/i', $_GET[id])) exit("No Hack ~_~");
    if(@ereg("admin",$_GET[id])) exit("HeHe");
    $query = "select id from prob_troll where id='{$_GET[id]}'";
    echo "<hr>query : <strong>{$query}</strong><hr><br>";
    $result = @mysql_fetch_array(mysql_query($query));
    if($result['id'] == 'admin') solve("troll");
    highlight_file(__FILE__);
?>
~~~
## 소스 코드 분석
1. ereg()
    - ereg 함수는 다음과 같은 형식을 취한다.
    ~~~
    ereg("찾고자 하는 문자", "대상 문자열")
    ~~~
    - ereg함수는 대소문자 구별을 한다.
    - eregi함수는 대소문자 구별을 하지 않는다.
    - ereg 함수에 대해 잘 모르겠다면 다음 링크를 참고하자  
     <a href="http://se2.php.net/manual/kr/function.ereg.php">PHP: ereg - Manual</a>
## 분석 결론
+ 금지 문자, 문자열
    - GET방식으로 입력받은 id값에 '(single quote)가 있다면 "No Hack ~_~"이 출력되고 문제 풀이에 실패한다.
    - GET방식으로 받은 id값에 'admin'이 있다면 "HeHe"가 출력되고 문제풀이에 실패한다.
+ 풀이 성공 조건
    - 데이터베이스에서 받아온 id 값이 'admin'이면 문제 풀이에 성공한다.
## 문제 해결
1. Query문 추가
    - 다음과 유사한 방법으로 문제를 해결 할 수 있다.
    ~~~
    ?id=Admin
    ~~~
    - 이는 PHP에서는 대소문자가 구별되지만  
    MySQL에서는 구별되지 않아 문제가 해결된다.
    - 즉 한문자 이상이 대문자가 되면 문제 해결이 가능하다.