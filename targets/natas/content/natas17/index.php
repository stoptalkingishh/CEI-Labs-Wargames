<?php
require '/etc/cei-labs/natas-runtime/natas17.php';
$prefix = isset($_POST['prefix']) ? $_POST['prefix'] : '';
$accepted = preg_match('/^[A-Za-z0-9_-]{0,128}$/', $prefix) && strpos($natas18_secret, $prefix) === 0;
if ($_SERVER['REQUEST_METHOD'] === 'POST') usleep($accepted ? 140000 : 10000);
?>
<!doctype html><html><head><title>Natas 17</title></head><body>
<h1>Credential verifier</h1><p>The verifier returns one uniform response while its application work differs for a matching prefix.</p>
<form method="post"><label>Candidate prefix <input name="prefix" maxlength="128"></label><button>Verify</button></form>
<?php if ($_SERVER['REQUEST_METHOD'] === 'POST'): ?><p>Verification complete.</p><?php endif; ?>
</body></html>
