<?php
require '/etc/cei-labs/natas-runtime/natas25.php';
$path = '/var/lib/cei-labs/natas-batch-c/audit-' . $natas_team . '.json'; $state = json_decode(@file_get_contents($path), true); if (!is_array($state)) $state = array('requests' => 0); $state['requests']++; file_put_contents($path, json_encode($state), LOCK_EX);
$marker = isset($_POST['marker']) && is_string($_POST['marker']) ? $_POST['marker'] : ''; $fixtures = array('audit:handoff' => 'handoff'); $resolved = strlen($marker) <= 64 && preg_match('/^[a-z:-]*$/', $marker) && isset($fixtures[$marker]);
?><!doctype html><html><body><h1>Synthetic audit resolver</h1><p>This resolver reads only an in-memory training fixture.</p><form method="post"><input name="marker" maxlength="64"><button>Resolve</button></form><?php if ($resolved): ?><p>Audit handoff: <?php echo htmlspecialchars($natas26_secret, ENT_QUOTES, 'UTF-8'); ?></p><?php else: ?><p>No handoff marker resolved.</p><?php endif; ?></body></html>
