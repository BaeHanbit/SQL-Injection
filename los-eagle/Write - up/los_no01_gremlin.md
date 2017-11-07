# Lord of SQL Injection No.1 - Gremlin
## 문제 출제 의도
1. SQL Injection의 이해여부를 확인.
2. 가장 SQL Injection을 실행 가능한지 확인.
## 소스 코드 
~~~
<?php  
    include "./config.php";  
    login_chk();  
    dbconnect();  
    if(preg_match('/prob|_|\.|\(\)/i', $_GET[id])) exit("No Hack ~_~");
    if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~");  
    $query = "select id from prob_gremlin where id='{$_GET[id]}' and pw='{$_GET[pw]}'";  
    echo "<hr>query : <strong>{$query}</strong><hr><br>";
    $result = @mysql_fetch_array(mysql_query($query));
    if($result['id']) solve("gremlin");
    highlight_file(__FILE__);
?>
~~~
## 소스 코드 분석
+ include문
    - include문은 특정 파일을 적용시킨다.
    - php의 include를 모른다면 다음 문서를 참고하자.  
    <a href = "http://php.net/manual/kr/function.include.php">PHP: include - Manual</a>
+ 사용자 정의 함수
    - login_chk();라는 함수는 로그인상태를 확인하는 함수라고 추정 가능하다.  
    - dbconnect();라는 함수는 데이터베이스와 연동하는 함수라고 추정 가능하다. 
+ 라이브러리 함수
    1. preg_match()
        * preg_match 함수는 다음과 같은 형식을 취한다.
        ~~~
            int preg_match ( string $pattern , string $subject [, array &$matches [, int $flags [, int $offset ]]] )
        ~~~
        * preg_match함수는 pattern에 주어진 정규표현식을 subject에서 찾는다.
        * preg_match함수에 대해 잘 모르겠다면 다음 링크를 참고하자.  
        <a href="http://php.net/manual/kr/function.preg-match.php">PHP: preg_match - Manual</a>
        * preg_match함수의 flag 옵션에 대해 잘 모르겠다면 다음 링크를 참고하자.  
        <a href="http://php.net/manual/kr/reference.pcre.pattern.modifiers.php">PHP: Possible modifiers in regex patterns - Manual</a>
    2. mysql_fetch_array()
        * mysql_fetch_array 함수는 다음과 같은 형식을 취한다.
        ~~~
        array mysql_fetch_array ( resource $result [, int $result_type ] )
        ~~~
        * 인출된 행을 배열로 만들어 반환한다.
        * 이때 result type에 따라 배열의 종류가 결정된다.
            1. MYSQL_BOTH(기본값)  
            연관색인, 숫자형색인을 모두 반환한다.
            2. MYSQL_ASSOC(mysql_fetch_assoc())  
            연관색인을 반환한다.
            3. MYSQL_NUM (mysql_fetch_row())   
            숫자형색인을 반환한다.
        * mysql_fetch_array함수에 대해 잘 모르겠다면 다음 사이트를 참고하자.  
        <a href="http://php.net/manual/kr/function.mysql-fetch-array.php">PHP: mysql_fetch_array - Manual</a>
## 분석 결론
+ 금지 문자, 문자열
    - GET방식으로 입력받은 id값에 prob _ . () 중 하나라도 있다면 "No Hack ~_~"이 출력되고 문제 풀이에 실패한다.
    - GET방식으로 입력받은 pw값에 prob _ . () 중 하나라도 있다면 "No Hack ~_~"이 출력되고 문제 풀이에 실패한다.
+ 풀이 성공 조건
    - 만약 데이터베이스에서 받은 값이 0이 아니라면 문제 해결에 성공한다.
## 문제 해결
1. WHERE 조건절 무력화
    - id, pw값을 '(single quote)를 이용하여 조작 가능하다.
    - 다음과 유사한 방법들로 WHERE 조건절을 무력화 시킬 수 있다.
    ~~~
    ?id=' or 1 -- -
    ?pw=' or 1 -- -
    ~~~
    - 이는 무조건 결과 값이 참이 되게 만들어 WHERE 조건절을 무력화시킨다.
2. UNION
    - 서브 쿼리를 이용하여 빈 테이블에 추가 값을 가지고 올 수 있다.
    - 다음과 유사한 방법들로 빈 테이블에 추가 값을 가지고 올 수 있다.
    ~~~
    ?id=' UNION(SELECT 'admin')-- -
    ?pw=' UNION(SELECT 'admin')-- -
    ~~~
    - 원래 SELECT와 FROM은 함께 존재해야 하지만 Mysql에서는 이를 생략 가능하다.