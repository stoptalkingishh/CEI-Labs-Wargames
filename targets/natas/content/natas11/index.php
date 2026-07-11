<?php
if (isset($_GET['source'])) {
    highlight_file(__FILE__);
    exit;
}

function xor_encrypt($in) {
    $key = 'qw8J';
    $text = $in;
    $outText = '';
    for ($i = 0; $i < strlen($text); $i++) {
        $outText .= $text[$i] ^ $key[$i % strlen($key)];
    }
    return $outText;
}

function loadData() {
    $mydata = array();
    $mydata['showpassword'] = 'no';
    $mydata['bgcolor'] = '#ffffff';
    if (array_key_exists('data', $_COOKIE)) {
        $tempdata = json_decode(xor_encrypt(base64_decode($_COOKIE['data'])), true);
        if (is_array($tempdata) && array_key_exists('showpassword', $tempdata) && array_key_exists('bgcolor', $tempdata)) {
            $mydata['showpassword'] = $tempdata['showpassword'];
            $mydata['bgcolor'] = $tempdata['bgcolor'];
        }
    }
    return $mydata;
}

$data = loadData();
setcookie('data', base64_encode(xor_encrypt(json_encode($data))), 0, '/');
// $next_password is written fresh per team by entrypoint.sh, in a
// separate file NOT shown by the highlight_file() view-source above.
require __DIR__ . "/next_password.php";
?>
<html>
<head><title>natas11</title></head>
<body style="background-color: <?php echo htmlspecialchars($data['bgcolor']); ?>;">
<h3>natas11</h3>
<?php
if ($data['showpassword'] === 'yes') {
    echo "<p>The password for natas12 is <tt>" . htmlspecialchars($next_password) . "</tt></p>";
} else {
    echo "<p>Cookies are protected with XOR encryption.</p>";
}
?>
<p><a href="?source">View sourcecode</a></p>
</body>
</html>
