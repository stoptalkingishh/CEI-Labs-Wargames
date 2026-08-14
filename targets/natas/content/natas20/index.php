<?php
require '/etc/cei-labs/natas-runtime/natas20.php';
$state_path = '/var/lib/cei-labs/natas-batch-b/record-' . $natas_team . '.txt';
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['note']) && is_string($_POST['note']) && strlen($_POST['note']) <= 96) {
    file_put_contents($state_path, 'id=guest|role=viewer|note=' . $_POST['note'], LOCK_EX);
}
$record = @file_get_contents($state_path);
$fields = array();
foreach (explode('|', is_string($record) ? $record : '') as $piece) {
    $pair = explode('=', $piece, 2);
    if (count($pair) === 2 && preg_match('/^[a-z]+$/', $pair[0])) $fields[$pair[0]] = $pair[1];
}
$operator = isset($fields['role']) && $fields['role'] === 'operator';
?>
<!doctype html><html><head><title>Natas 20</title></head><body>
<h1>Profile note desk</h1><p>Your note is kept in a compact local profile record.</p>
<form method="post"><label>Note <input name="note" maxlength="96"></label><button>Save note</button></form>
<?php if ($operator): ?><p>Supervisor handoff: <?php echo htmlspecialchars($natas21_secret, ENT_QUOTES, 'UTF-8'); ?></p><?php else: ?><p>Viewer profile active.</p><?php endif; ?>
</body></html>
