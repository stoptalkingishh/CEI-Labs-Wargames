<?php
require '/etc/cei-labs/natas-runtime/natas24.php';
$model = array('role' => 'viewer', 'region' => 'local');
$access = isset($_POST['access']) ? $_POST['access'] : '';
if (is_string($access)) {
    $model['role'] = 'viewer';
} elseif (is_array($access) && count($access) <= 2) {
    foreach ($access as $key => $value) {
        if (($key === 'role' || $key === 'region') && is_string($value) && strlen($value) <= 16) $model[$key] = $value;
    }
}
$operator = $model['role'] === 'operator' && $model['region'] === 'local';
?>
<!doctype html><html><head><title>Natas 24</title></head><body><h1>Local request model</h1><p>The service accepts a compact access request.</p>
<form method="post"><label>Access <input name="access" maxlength="16"></label><button>Apply</button></form>
<?php if ($operator): ?><p>Local handoff: <?php echo htmlspecialchars($natas25_secret, ENT_QUOTES, 'UTF-8'); ?></p><?php else: ?><p>Viewer model active.</p><?php endif; ?>
</body></html>
