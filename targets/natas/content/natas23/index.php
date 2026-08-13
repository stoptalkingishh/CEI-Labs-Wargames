<?php
require '/etc/cei-labs/natas-runtime/natas23.php';
function toy_numeric_prefix_equal($value, $expected) {
    if (!is_string($value) || !preg_match('/^[0-9]+/', $value, $match)) return false;
    return (int)$match[0] === (int)$expected;
}
$token = isset($_POST['token']) && is_string($_POST['token']) ? $_POST['token'] : '';
$loose = toy_numeric_prefix_equal($token, '7');
$strict = $token === '7';
?>
<!doctype html><html><head><title>Natas 23</title></head><body><h1>Comparison training console</h1><p>A toy compatibility check is paired with a strict control.</p>
<form method="post"><label>Token <input name="token" maxlength="32"></label><button>Compare</button></form>
<?php if ($_SERVER['REQUEST_METHOD'] === 'POST'): ?><?php if ($loose): ?><p>Compatibility result: <?php echo htmlspecialchars($natas24_secret, ENT_QUOTES, 'UTF-8'); ?></p><?php else: ?><p>Compatibility result: denied.</p><?php endif; ?><p>Strict control: <?php echo $strict ? 'accepted.' : 'denied.'; ?></p><?php endif; ?>
</body></html>
