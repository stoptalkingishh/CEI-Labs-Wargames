<?php
// Expected referer is deliberately the NEXT level's own vhost (one port
// higher than whatever port THIS request actually arrived on -- port-
// relative rather than a hardcoded absolute port, since the port a
// player's browser sees may be remapped, e.g. under local Docker
// testing), a URL a real browser can never arrive at naturally on the
// way here -- the only way in is to forge the header.
$host_parts = explode(':', $_SERVER['HTTP_HOST']);
$this_host = $host_parts[0];
$this_port = isset($host_parts[1]) ? (int)$host_parts[1] : 80;
$expected = 'http://' . $this_host . ':' . ($this_port + 1) . '/';
$referer = isset($_SERVER['HTTP_REFERER']) ? $_SERVER['HTTP_REFERER'] : '';
?>
<html>
<head><title>natas4</title></head>
<body>
<h3>natas4</h3>
<?php
if ($referer === $expected) {
    echo "<p>Access granted. The password for natas5 is <tt>__NATAS5_SECRET__</tt></p>";
} else {
    echo "<p>Access disallowed. You are visiting from \"" . htmlspecialchars($referer) . "\" while authorized users should come only from \"" . htmlspecialchars($expected) . "\"</p>";
}
?>
</body>
</html>
