<?php
if (isset($_GET['viewsource'])) {
    highlight_file(__FILE__);
    exit;
}
$page = isset($_GET['page']) ? $_GET['page'] : 'home.php';
?>
<html>
<head><title>natas7</title></head>
<body>
<h3>natas7</h3>
<a href="index.php?page=home.php">Home</a> -
<a href="index.php?page=about.php">About</a> -
<a href="index.php?viewsource">View sourcecode</a>
<!-- hint: the password for natas8 is stored in /etc/natas_webpass/natas8 -->
<hr>
<?php include($page); ?>
</body>
</html>
