<?php
require '/etc/cei-labs/natas-runtime/natas18.php';
$cookie = isset($_COOKIE['CEI18']) ? $_COOKIE['CEI18'] : '1';
$id = ctype_digit($cookie) ? (int)$cookie : 1;
$state_path = '/var/lib/cei-labs/natas-batch-a/sessions-' . $natas_team . '.json';
$sessions = json_decode(@file_get_contents($state_path), true);
$privileged = $id >= 1 && $id <= 64 && isset($sessions[(string)$id]) && $sessions[(string)$id]['role'] === 'operator';
setcookie('CEI18', (string)$id, 0, '/', '', false, true);
?>
<!doctype html><html><head><title>Natas 18</title></head><body>
<h1>Service desk</h1><p>Your numeric service session is <?php echo htmlspecialchars((string)$id, ENT_QUOTES, 'UTF-8'); ?>.</p>
<?php if ($privileged): ?><p>Operator note: <?php echo htmlspecialchars($natas19_secret, ENT_QUOTES, 'UTF-8'); ?></p><?php else: ?><p>Standard session. Operator notes require an operator session.</p><?php endif; ?>
</body></html>
