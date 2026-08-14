<?php
require '/etc/cei-labs/natas-runtime/natas22.php';
$next = isset($_GET['next']) && is_string($_GET['next']) ? $_GET['next'] : '/receipt';
if (!preg_match('#^/[a-z]+$#', $next)) $next = '/receipt';
$run = isset($_GET['run']) && is_string($_GET['run']) ? $_GET['run'] : 'receipt';
header('Location: ' . $next, true, 302);
header('Cache-Control: no-store');
$marker = $run === 'review' ? 'Review marker: ' . htmlspecialchars($natas23_secret, ENT_QUOTES, 'UTF-8') : 'Receipt marker prepared.';
?>
<!doctype html><html><head><title>Natas 22</title></head><body><h1>Local dispatch</h1><p><?php echo $marker; ?></p></body></html>
