# Lord of SQL Injection No.24 - Evil_Wizard
## 문제 출제 의도
1. 공짜문제 버전 2
## 소스 코드 분석
+ 소스코드
~~~
    <?php
    include "./config.php"; 
    login_chk(); 
    dbconnect(); 
    if(preg_match('/_|\.|\(\)/i', $_GET[limit])) exit("No Hack ~_~");
    echo "<h1>Sorry, this challenge is broken! (Thanks to <i>@dohyeokkim</i>)</h1>";
    solve("evil_wizard");
    highlight_file(__FILE__);
    ?>
~~~

+ 소스 코드 분석
    - 방심을 다시 한번 유도하여 계속해서 고민하게 만든다.
    - 사실 그냥 들어간 순간 문제가 또 해결되었다.
## 문제 해결
- 공짜문제 정말 좋아요