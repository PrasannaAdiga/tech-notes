## PHP in HTML

HTML is a language used to tell a browser how to display a document, it is not a programming language.
Html is sent from the server and is interpreted by the web browser, which is sometimes referred to as a client.

Php is a programming language and can be used to create manipulate and output data. Php code runs on the web server, and the results of running a php script are sent to the browser. 

The browser doesn't know that it's php code that has sent it some data. It just receives whatever text php has outputted. This text could of course contain html, but it's important to remember that no php code goes to the browser.

Html on its own is fine if all you have is some static content that you want to display in a web browser.
However, if you want a dynamic website, for example, a blog with new and updated articles are an e-commerce site with dynamic product data and so on that has content that changes automatically, then you need to use a mixture of html and php.

We can write multiple echo statement in a php file, which has multiple html content and then if we call this script from browser, php server will run this script internally and sends back the html output to browser. A file called index.html is served automatically if no file is specified in the browser address. The same is true for files called index.php. If we remove the file name, then we still get the contents of index.php by default.

If we have a file that just has php in it, then you only need the opening tag.  There's also a closing tag in php2 which we use when we're mixing php and html together.

We can insert PHP code inside html content like below:
```
<?php
$name = "Dave";
?>

<!DOCTYPE html>
<html>
<head>
    <title>My website</title>
    <meta charset="utf-8">
</head>
<body>
    <h1>Lorem Ipsum</h1>
    <p>Hello, <?php echo $name; ?>!</p>
</body>
</html>
```
Before the web server sends this file to the browser, it executes this code and replaces it with the results, including the opening and closing tags. All PHP codes are executed in the server before sending the result to browser.

## Use PHP control structure inside HTML
We can separate PHP code from HTML like below:
```
<?php
$hour = 12;
?>
<!DOCTYPE html>
<html>
<head>
    <title>My website</title>
    <meta charset="utf-8">
</head>
<body>
    <h1>Lorem Ipsum</h1>
    <?php if ($hour < 12): ?>    ====> PHP CODE. Replace { by :
        Good morning             ====> HTML CODE
    <?php elseif ($hour < 18): ?>
        Good afternoon
    <?php elseif ($hour < 22): ?>
        Good evening
    <?php else: ?>
        Good night
    <?php endif; ?>               ====> PHP CODE. Replace } by endif
</body>
</html>
```

The same alternative syntax is used for while, for, foreach, switch and so on. We need to end it with endwhile, endfor, endforeach, endswitch and so on.

Also use whitespaces, tabs and comments(<!-- this is a comment -->) to write more readable HTML code.
Use either `//` or `/* */` to write a comment in PHP code.

---
# PHP and MySQL

## Connect to database from PHP, and query the database and get the results

```
<?php

$db_host = "localhost";
$db_name = "cms";
$db_user = "cms_www";
$db_pass = "64w6H2rOJ1zwLRyk";

$conn = mysqli_connect($db_host, $db_user, $db_pass, $db_name);

if (mysqli_connect_error()) {
    echo mysqli_connect_error();
    exit;
}

$sql = "SELECT *
        FROM article
        ORDER BY published_at;";

$results = mysqli_query($conn, $sql); ===> Send the sql query to database

if ($results === false) {
    echo mysqli_error($conn);
} else {
    $articles = mysqli_fetch_all($results, MYSQLI_ASSOC); ===> fetch all the values with their corresponding column details through MYSQLI_ASSOC argument

    var_dump($articles);
}
?>
?>
<!DOCTYPE html>
<html>
<head>
    <title>My blog</title>
    <meta charset="utf-8">
</head>
<body>

    <header>
        <h1>My blog</h1>
    </header>

    <main>
        <?php if (empty($articles)): ?>
            <p>No articles found.</p>
        <?php else: ?>

            <ul>
                <?php foreach ($articles as $article): ?>
                    <li>
                        <article>
                            <h2><?= $article['title']; ?></h2>
                            <p><?= $article['content']; ?></p>
                        </article>
                    </li>
                <?php endforeach; ?>
            </ul>

        <?php endif; ?>
    </main>
</body>
</html>
```

## Get a single data from database
```
<?php

$db_host = "localhost";
$db_name = "cms";
$db_user = "cms_www";
$db_pass = "64w6H2rOJ1zwLRyk";

$conn = mysqli_connect($db_host, $db_user, $db_pass, $db_name);

if (mysqli_connect_error()) {
    echo mysqli_connect_error();
    exit;
}

$sql = "SELECT *
        FROM article
        WHERE id = 1";

$results = mysqli_query($conn, $sql);

if ($results === false) {
    echo mysqli_error($conn);
} else {
    $article = mysqli_fetch_assoc($results); ===> Fetch a single record
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>My blog</title>
    <meta charset="utf-8">
</head>
<body>

    <header>
        <h1>My blog</h1>
    </header>

    <main>
        <?php if ($article === null): ?>
            <p>Article not found.</p>
        <?php else: ?>

            <article>
                <h2><?= $article['title']; ?></h2>
                <p><?= $article['content']; ?></p>
            </article>

        <?php endif; ?>
    </main>
</body>
</html>

```

## Passing data in the URL and access it in PHP

```
index.php
...
...
<main>
    <?php if (empty($articles)): ?>
        <p>No articles found.</p>
    <?php else: ?>

        <ul>
            <?php foreach ($articles as $article): ?>
                <li>
                    <article>
                        <h2><a href="article.php?id=<?= $article['id']; ?>"><?= $article['title']; ?></a></h2>
                        <p><?= $article['content']; ?></p>
                    </article>
                </li>
            <?php endforeach; ?>
        </ul>
    <?php endif; ?>
</main>
```

Create a link to articale.php by paasing its id in a query string as `article.php?id=<?= $article['id'];`

```
articale.php

<?php

$db_host = "localhost";
$db_name = "cms";
$db_user = "cms_www";
$db_pass = "64w6H2rOJ1zwLRyk";

$conn = mysqli_connect($db_host, $db_user, $db_pass, $db_name);

if (mysqli_connect_error()) {
    echo mysqli_connect_error();
    exit;
}

$sql = "SELECT *
        FROM article
        WHERE id = " . $_GET['id'];  ===> Extract query parameter id from $_GET

$results = mysqli_query($conn, $sql);

if ($results === false) {

    echo mysqli_error($conn);

} else {

    $article = mysqli_fetch_assoc($results);

}
```

Extract the query parameter `id` like $_GET['id'];

Before extracting query parameter, we can check whether this query parametr is set and it is numeric like `isset($_GET['id']) && is_numeric($_GET['id'])`

## Include/require another php file in the current one

We can use `include` tag to add another file in the current one.
Create a sepaarte php file for the database connection operations and import it in another file.

```
database.php

<?php

$db_host = "localhost";
$db_name = "cms";
$db_user = "cms_www";
$db_pass = "64w6H2rOJ1zwLRyk";

$conn = mysqli_connect($db_host, $db_user, $db_pass, $db_name);

if (mysqli_connect_error()) {
    echo mysqli_connect_error();
    exit;
}
?>
```

```
articale.php

<?php.php

include `database.php`;

$sql = "SELECT *
        FROM article
        WHERE id = " . $_GET['id'];  ===> Extract query parameter id from $_GET

...
...        
?>

```

We can aslo use `require` tag instead of `include`. But require tag will throw an error and stops the script if it does not find the file which needs to be included, where as include just show some waring messages.

Same way we can create separate php files for the header and footer html tags and import it wherever it is needed.

We can add `.htaccess` file with content as `Deny from all` to access the database.php and other kind of php files directly.

## Forms in PHP
```
form.php

<!DOCTYPE html>
<html>
<head>
    <title>Forms</title>
    <meta charset="utf-8">
</head>
<body>

<form>
    <input name="search" action="process_form.php">  ===> to send to another php file use action
    <button>Send</button>
</form>

</body>
</html>

```

```
process_form.php

<?php
var_dump($_GET);   ===> Use $_GET to get all the incoming field

```

If we do not specify the action tag in the form, then the form will be submitted to itself.

By default, the forms will make GET request, which will send the forms data as query string. But if we specify the request method as POST by using `<form method="POST">`, then it will send the forms data as a request body and to receive these data in other PHP file use `$_POST` instead of `$_GET`.If we do not specify the method, then by default it will have GET method.

We can also have a check for which method is been called by using `if ($_SERVER["REQUEST_METHOD"] == "POST")`

## Submit a form to add new record in MySQL
```
<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    require 'includes/database.php';

    $sql = "INSERT INTO article (title, content, published_at)
            VALUES ('" . $_POST['title'] . "','"
                       . $_POST['content'] . "','"
                       . $_POST['published_at'] . "')";

    $results = mysqli_query($conn, $sql);

    if ($results === false) {
        echo mysqli_error($conn);
    } else {
        $id = mysqli_insert_id($conn); ====> Use mysqli_insert_id to run the given insert query.
        echo "Inserted record with ID: $id";
    }
}

?>
<?php require 'includes/header.php'; ?>
<h2>New article</h2>
<form method="post">

    <div>
        <label for="title">Title</label>
        <input name="title" id="title" placeholder="Article title">
    </div>

    <div>
        <label for="content">Content</label>
        <textarea name="content" rows="4" cols="40" id="content" placeholder="Article content"></textarea>
    </div>

    <div>
        <label for="published_at">Publication date and time</label>
        <input type="datetime-local" name="published_at" id="published_at">
    </div>

    <button>Add</button>

</form>

<?php require 'includes/footer.php'; ?>

```


