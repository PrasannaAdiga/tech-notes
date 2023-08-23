# PHP Data Objects (PDO)

mysqli has both procedural and object orienetd interfaces, which we can use to connect to MySQL DB from PHP.

But if we're going to start using object oriented code to interact with the database, PHP offers an alternative method. With PHP Data Objects or PDO, we can access the database in much the same way we've been doing it using mysqli. 

However PDO does have several advantages over mysqli. First, PDO isn't just limited to MySQL or mariadb, you can connect to all of these database management systems using exactly the same PDO code. So once you know PDO, you can work with pretty much any relational database management system without having to learn more code. 

## Add a Database class and connect to DB using PDO

```
<?php

/**
 * Database
 *
 * A connection to the database
 */
class Database
{
    /**
     * Get the database connection
     *
     * @return PDO object Connection to the database server
     */
    public function getConn()
    {
        $db_host = "localhost";
        $db_name = "cms";
        $db_user = "cms_www";
        $db_pass = "64w6H2rOJ1zwLRyk";

        $dsn = 'mysql:host=' . $db_host . ';dbname=' . $db_name . ';charset=utf8';

        return new PDO($dsn, $db_user, $db_pass);
    }
}
```

## Query a DB using PDO

```
<?php

require 'classes/Database.php';
require 'includes/auth.php';

session_start();

$db = new Database();
$conn = $db->getConn();

$sql = "SELECT *
        FROM article
        ORDER BY published_at;";

$results = $conn->query($sql);

if ($results === false) {
    var_dump($conn->errorInfo());
} else {
    $articles = $results->fetchAll(PDO::FETCH_ASSOC);
}
?>
```

## Run a prepared statement using PDO to fetch all data
```
<?php
	$host = 'localhost';
	$user = 'root';
	$password = '123456';
	$dbname = 'pdotest';

	// Set DSN
	$dsn = 'mysql:host=' . $host . ';dbname=' . $dbname;

	// Create a PDO instance
	$pdo = new PDO($dsn, $user, $password);
	$pdo->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_OBJ);

	$status = 'admin';

	$sql = 'SELECT * FROM users WHERE status = :status';
	$stmt = $pdo->prepare($sql);
	$stmt->execute(['status' => $status]);
	$users = $stmt->fetchAll();

	foreach($users as $user){
	 	echo $user->name.'<br>';
	}
```

## Insert data using PDO
```
<?php
	$host = 'localhost';
	$user = 'root';
	$password = '123456';
	$dbname = 'pdotest';

	// Set DSN
	$dsn = 'mysql:host=' . $host . ';dbname=' . $dbname;

	// Create a PDO instance
	$pdo = new PDO($dsn, $user, $password);
	$pdo->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_OBJ);

    $name = 'Karen Williams';
	$email = 'kwills@gmail.com';
	$status = 'guest';

	$sql = 'INSERT INTO users(name, email, status) VALUES(:name, :email, :status)';
	$stmt = $pdo->prepare($sql);
	$stmt->execute(['name'=> $name, 'email' => $email, 'status' => $status]);
	echo 'Added User';
```
