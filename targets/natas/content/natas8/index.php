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

$result = "";
if (isset($_POST["secret"])) {
    if (encodeSecret($_POST["secret"]) === $encodedSecret) {
        $result = "<p>Access granted. The password for natas9 is <tt>W0608Rh6bUNF6M9776QvSAsSgS2abV0M</tt></p>";
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
