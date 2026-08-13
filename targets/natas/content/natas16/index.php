<?php
require '/etc/cei-labs/natas-runtime/natas16.php';
if (isset($_GET['source'])) {
    highlight_file(__FILE__);
    exit;
}
$needle = isset($_GET['needle']) ? $_GET['needle'] : '';
$blocked = preg_match('/[;&|`$\\\\]/', $needle);
$result = '';
if ($needle !== '' && !$blocked) {
    // This bounded emulator models a legacy expansion step; it never executes input.
    $references = array('handoff' => 'sealed-record');
    $catalog = array(
        'catalog' => 'catalog: cedar, juniper, maple',
        'sealed-record' => 'training credential: ' . $natas17_secret,
    );
    if ($needle === 'catalog') $result = 'catalog: cedar, juniper, maple';
    if (preg_match('/^search \{\{ref:([a-z]{3,16})\}\}$/', $needle, $match)
        && isset($references[$match[1]])) {
        $result = $catalog[$references[$match[1]]];
    }
}
?>
<!doctype html><html><head><title>Natas 16</title></head><body>
<h1>Archive search</h1><p>The legacy search adapter rejects command punctuation before evaluating its small training catalog.</p><p><a href="?source">View source</a></p>
<form><label>Search <input name="needle" maxlength="80"></label><button>Search</button></form>
<?php if ($needle !== ''): ?><pre><?php echo htmlspecialchars($blocked ? 'Input rejected.' : ($result ?: 'No records.'), ENT_QUOTES, 'UTF-8'); ?></pre><?php endif; ?>
</body></html>
