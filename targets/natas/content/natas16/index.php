<?php
require '/etc/cei-labs/natas-runtime/natas16.php';
$needle = isset($_GET['needle']) ? $_GET['needle'] : '';
$blocked = preg_match('/[;&|`$\\\\]/', $needle);
$result = '';
if ($needle !== '' && !$blocked) {
    if ($needle === 'catalog') $result = 'catalog: cedar, juniper, maple';
    if ($needle === 'catalog credential') $result = 'training credential: ' . $natas17_secret;
}
?>
<!doctype html><html><head><title>Natas 16</title></head><body>
<h1>Archive search</h1><p>The legacy search adapter rejects command punctuation before evaluating its small training catalog.</p>
<form><label>Search <input name="needle" maxlength="80"></label><button>Search</button></form>
<?php if ($needle !== ''): ?><pre><?php echo htmlspecialchars($blocked ? 'Input rejected.' : ($result ?: 'No records.'), ENT_QUOTES, 'UTF-8'); ?></pre><?php endif; ?>
</body></html>
