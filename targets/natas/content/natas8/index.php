<?php
if (isset($_GET['source'])) {
    highlight_file(__FILE__);
    exit;
}

function encodeSecret($secret) {
    return bin2hex(strrev(base64_encode($secret)));
}

// Encoded once, offline, from a secret nobody sees in plaintext here --
// reverse the chain (hex-decode, un-reverse the string, base64-decode)
// to recover it.
$encodedSecret = "3d3d77594d523151485a445330306d5344526d594e74455779556b4e5942545a43685751";
// $next_password is written fresh per team by entrypoint.sh, in a
// separate file NOT shown by the highlight_file() view-source above.
require __DIR__ . "/next_password.php";

$result = "";
if (isset($_POST["secret"])) {
    if (encodeSecret($_POST["secret"]) === $encodedSecret) {
        $result = "<p>Access granted. The password for natas9 is <tt>" . htmlspecialchars($next_password) . "</tt></p>";
    } else {
        $result = "<p>Wrong secret</p>";
    }
}
?>
<html>
<head><title>natas8</title></head>
<body>
<h3>natas8</h3>
<p><a href="?source">View sourcecode</a></p>
<p>Encoded secret: <tt><?php echo $encodedSecret; ?></tt></p>
<form method="post">
<input type="text" name="secret">
<input type="submit" value="Submit">
</form>
<?php echo $result; ?>
</body>
</html>
