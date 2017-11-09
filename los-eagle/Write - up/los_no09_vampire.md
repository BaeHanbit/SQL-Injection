# Lord of SQL Injection No. 9 - Vampire
## 문제 출제 의도
1. str_replace 함수를 이해하고 있는지 확인.
## 소스 코드
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
## 소스 코드 분석
+ str_replace()
    * str_replace함수는 다음과 같은 형식을 취한다.
    ~~~
    mixed str_replace ( mixed $search , mixed $replace , mixed $subject)
    ~~~
    * subject에서 발견한 모든 search를 주어진 replace 값으로 치환한 문자열이나 배열을 반환한다.
    * str_repalce함수를 잘 모르겠다면 다음 링크를 참고하자  
    <a href="http://php.net/manual/kr/function.str-replace.php">PHP: str_replace - Manual</a>
## 분석 결론
+ 금지 문자, 문자열
    - GET방식으로 입력받은 id값에 '(single quote)가 있다면 "No Hack ~_~"이 출력되고 문제 풀이에 실패한다.
+ id값
    - 입력 받은 id에 admin이 있다면 빈 문자열로 치환된다.
+ 풀이 성공 조건
    - 데이터베이스에서 받아온 id 값이 'admin'이면 문제 풀이에 성공한다.
## 문제 해결
1. Query문 추가
   - 다음과 유사한 방법으로 문제를 해결 할 수 있다.
   ~~~
   ?id=Admin
   ?id=adadminmin
   ~~~
   - str_replace 함수는 한번만 실행되기 때문에 밑의 값은 admin이 된다.