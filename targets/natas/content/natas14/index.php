<?php
if (isset($_GET['source'])) {
    highlight_file(__FILE__);
    exit;
}

$msg = "";
if (array_key_exists("username", $_REQUEST) && array_key_exists("password", $_REQUEST)) {
    $link = mysql_connect('127.0.0.1', 'natas14', 'natas14dbP4ss');
    mysql_select_db('natas14', $link);

    // Raw string concatenation into the query -- the entire lesson, and
    // exactly why this level needs the legacy mysql_* extension (this
    // pattern doesn't exist in mysqli/PDO's default usage).
    $query = "SELECT * from users where username=\"" . $_REQUEST["username"] . "\" and password=\"" . $_REQUEST["password"] . "\"";

    $res = mysql_query($query, $link);
    if ($res !== false && mysql_num_rows($res) > 0) {
        $msg = "Successful login! The FINAL Natas flag is <tt>A0608Rh6bUNF6M9776QvSAsSgS2abV0M</tt>";
    } else {
        $msg = "Access denied!";
    }
    mysql_close($link);
}
?>
<html>
<head><title>natas14</title></head>
<body>
<h3>natas14</h3>
<form method="post">
Username: <input type="text" name="username"><br>
Password: <input type="password" name="password"><br>
<input type="submit" value="Login">
</form>
<?php echo $msg; ?>
<p><a href="?source">View sourcecode</a></p>
</body>
</html>
