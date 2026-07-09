<?php
if (isset($_GET['source'])) {
    highlight_file(__FILE__);
    exit;
}

$result = "";
if (array_key_exists("needle", $_REQUEST)) {
    $key = $_REQUEST['needle'];
    if (preg_match('/[;|&`]/', $key)) {
        $result = "...Sorry, we detected an attack attempt...";
    } else {
        ob_start();
        passthru("grep -i $key dictionary.txt");
        $result = ob_get_clean();
    }
}
?>
<html>
<head><title>natas10</title></head>
<body>
<h3>natas10</h3>
<p><a href="?source">View sourcecode</a></p>
<form method="get">
<input type="text" name="needle">
<input type="submit" value="Search">
</form>
<pre><?php echo htmlspecialchars($result); ?></pre>
</body>
</html>
