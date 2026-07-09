<?php
if (isset($_GET['source'])) {
    highlight_file(__FILE__);
    exit;
}
include "includes/secret.inc";

$result = "";
if (isset($_POST["secret"])) {
    if ($_POST["secret"] === $secret) {
        $result = "<p>Access granted. The password for natas7 is <tt>7z3hDeo6i6vF9M9776QvSAsSgS2abV0M</tt></p>";
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
