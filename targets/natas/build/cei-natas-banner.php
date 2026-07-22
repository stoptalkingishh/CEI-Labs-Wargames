<?php
/* PHP 5.6-compatible static banner injector; port is server-owned metadata. */
function cei_natas_banner_fragment() {
    $port = isset($_SERVER['SERVER_PORT']) ? (int) $_SERVER['SERVER_PORT'] : 0;
    if ($port < 8000 || $port > 8014) return '';
    $path = '/etc/cei-labs/natas-banners/natas' . ($port - 8000) . '.html';
    return is_readable($path) ? file_get_contents($path) : '';
}
function cei_natas_banner_is_html() {
    $attachment = false; $html = true;
    foreach (headers_list() as $header) {
        if (stripos($header, 'Content-Disposition:') === 0) $attachment = true;
        if (stripos($header, 'Content-Type:') === 0 && stripos($header, 'text/html') === false) $html = false;
    }
    return $html && !$attachment;
}
function cei_natas_banner_filter($output) {
    static $done = false;
    if ($done || !cei_natas_banner_is_html()) return $output;
    $fragment = cei_natas_banner_fragment();
    if ($fragment === '') return $output;
    $done = true;
    if (preg_match('/<body\b[^>]*>/i', $output, $match, PREG_OFFSET_CAPTURE)) {
        $at = $match[0][1] + strlen($match[0][0]);
        return substr($output, 0, $at) . $fragment . substr($output, $at);
    }
    return $fragment . $output;
}
ob_start('cei_natas_banner_filter');
?>
