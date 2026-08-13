<?php
require '/etc/cei-labs/natas-runtime/natas19.php';
$token = isset($_COOKIE['CEI19']) ? $_COOKIE['CEI19'] : 'aWQ9MTtyb2xlPXZpc2l0b3I';
$wire = strtr($token, '-_', '+/');
$decoded = base64_decode($wire . str_repeat('=', (4 - strlen($wire) % 4) % 4), true);
$fields = array();
if ($decoded !== false && preg_match('/^id=([1-9][0-9]?);role=(visitor|operator)$/', $decoded, $match)) {
    $fields = array('id' => $match[1], 'role' => $match[2]);
}
if (!$fields) $fields = array('id' => '1', 'role' => 'visitor');
setcookie('CEI19', rtrim(strtr(base64_encode('id='.$fields['id'].';role='.$fields['role']), '+/', '-_'), '='), 0, '/', '', false, true);
?>
<!doctype html><html><head><title>Natas 19</title></head><body>
<h1>Ticket portal</h1><p>Session ticket accepted for visitor <?php echo htmlspecialchars($fields['id'], ENT_QUOTES, 'UTF-8'); ?>.</p>
<?php if ($fields['role'] === 'operator'): ?><p>Operator handoff: <?php echo htmlspecialchars($natas20_secret, ENT_QUOTES, 'UTF-8'); ?></p><?php else: ?><p>Operator handoff is restricted.</p><?php endif; ?>
</body></html>
