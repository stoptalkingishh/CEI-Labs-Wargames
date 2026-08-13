<?php
require '/etc/cei-labs/natas-runtime/natas5.php';
if (!isset($_COOKIE["loggedin"])) {
    setcookie("loggedin", "0", 0, "/");
}
?>
<html>
<head><title>natas5</title></head>
<body>
<h3>natas5</h3>
<?php
if (isset($_COOKIE["loggedin"]) && $_COOKIE["loggedin"] == "1") {
    echo "<p>You are logged in. The password for natas6 is <tt>" . htmlspecialchars($natas6_secret, ENT_QUOTES, 'UTF-8') . "</tt></p>";
} else {
    echo "<p>You are not logged in. Log in to see the password for the next level.</p>";
}
?>
</body>
</html>
