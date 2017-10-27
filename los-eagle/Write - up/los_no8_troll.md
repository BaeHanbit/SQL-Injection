# Lord of SQL Injection No. 8- troll
## 문제 출제 의도
정규표현식을 이해하고 있는지 알아본다.
## 소스 코드 분석
+ 소스코드
troll의 소스코드는 다음과 같다.
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
+ 소스 코드 분석
    - Get 방식으로 받은 문자열에 'prob _ . ( )중 하나라도 있다면 "No Hack~_~"이 출력되고 문제 풀이에 실패한다.
    - Get 방식으로 받은 문자열에 'admin'이 있다면 "HeHe"가 출력되고 문제 풀이에 실패한다.
    - 문제 풀이에 성공하는 GET방식으로 받은 id값이 'admin'일 때이다.
## 문제 해결
+ ereg 함수
    ~~~
    ereg(string $pattern , string $string [, array &$regs ]) :
    ~~~
    - ereg 함수는 대소문자 구별을 하여 두 문장을 비교하여 같으면 1을 아니면 0을 반환한다.
    - 따라서 이후 Admin을 입력하면 후에 대소문자 구문을 안하는 php구문에 의해 문제가 해결된다.
    - 대문자가 하나 이상 섞여 있으면 문제가 풀린다.