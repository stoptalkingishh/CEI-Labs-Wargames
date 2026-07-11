<?php
if (isset($_GET['source'])) {
    highlight_file(__FILE__);
    exit;
}
include "includes/secret.inc";
// $next_password is written fresh per team by entrypoint.sh, in a
// separate file NOT shown by the highlight_file() view-source above --
// keeping it out of THIS file means ?source can never reveal it
// regardless of whether $_POST["secret"] matches.
require __DIR__ . "/next_password.php";

$result = "";
if (isset($_POST["secret"])) {
    if ($_POST["secret"] === $secret) {
        $result = "<p>Access granted. The password for natas7 is <tt>" . htmlspecialchars($next_password) . "</tt></p>";
    } else {
        $result = "<p>Wrong secret</p>";
    }
}
?>
<html>
<head><title>natas6</title></head>
<body>
<h3>natas6</h3>
<p><a href="?source">View sourcecode</a></p>
<form method="post">
<input type="text" name="secret">
<input type="submit" value="Submit">
</form>
<?php echo $result; ?>
</body>
</html>
