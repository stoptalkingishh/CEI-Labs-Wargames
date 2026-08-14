<?php
require '/etc/cei-labs/natas-runtime/natas21.php';
$route = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
$route = is_string($route) ? $route : '/';
if ($route === '/desk') {
    $badge = isset($_GET['badge']) && is_string($_GET['badge']) ? $_GET['badge'] : 'viewer';
    if (!preg_match('/^(viewer|operator)$/', $badge)) $badge = 'viewer';
    setcookie('CEI21_DESK', 'desk:' . $badge, 0, '/', '', false, true);
    $message = 'Desk badge prepared.';
} elseif ($route === '/reports') {
    $ticket = isset($_COOKIE['CEI21_DESK']) ? $_COOKIE['CEI21_DESK'] : '';
    $operator = $ticket === 'desk:operator';
    $message = $operator ? 'Report handoff: ' . htmlspecialchars($natas22_secret, ENT_QUOTES, 'UTF-8') : 'Reports requires a desk-issued operator badge.';
} elseif ($route === '/') {
    $message = 'Use the local desk or reports route.';
} else {
    http_response_code(404); $message = 'Use the local desk or reports route.';
}
?>
<!doctype html><html><head><title>Natas 21</title></head><body><h1>Internal office routes</h1><p><?php echo $message; ?></p></body></html>
