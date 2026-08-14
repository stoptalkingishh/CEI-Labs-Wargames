<?php
require '/etc/cei-labs/natas-runtime/natas15.php';
$probe = isset($_POST['probe']) ? $_POST['probe'] : '';
$valid = preg_match('/^account=operator; prefix=([A-Za-z0-9_-]{0,128})$/', $probe, $match)
    && strpos($natas16_secret, $match[1]) === 0;
?>
<!doctype html><html><head><title>Natas 15</title></head><body>
<h1>Directory validation console</h1>
<p>Submit a constrained account predicate. The console reports only whether a record exists.</p>
<form method="post"><label>Probe <input name="probe" maxlength="160"></label><button>Validate</button></form>
<?php if ($_SERVER['REQUEST_METHOD'] === 'POST'): ?><p><?php echo $valid ? 'Record exists.' : 'No matching record.'; ?></p><?php endif; ?>
</body></html>
