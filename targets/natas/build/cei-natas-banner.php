<?php
/* PHP 5.6-compatible static banner injector; port is server-owned metadata. */
function cei_natas_banner_fragment() {
    $port = isset($_SERVER['SERVER_PORT']) ? (int) $_SERVER['SERVER_PORT'] : 0;
    if ($port < 8000 || $port > 8014) return '';
    $path = '/etc/cei-labs/natas-banners/natas' . ($port - 8000) . '.html';
    return is_readable($path) ? file_get_contents($path) : '';
}

/* Per-level themed background CSS (see build/generate_themes.py). Always
 * returns a <style> block for a valid natas port, regardless of solved
 * state -- which state it renders is decided by cei_natas_theme_state(). */
function cei_natas_theme_style_fragment() {
    $port = isset($_SERVER['SERVER_PORT']) ? (int) $_SERVER['SERVER_PORT'] : 0;
    if ($port < 8000 || $port > 8014) return '';
    $path = '/etc/cei-labs/natas-themes/natas' . ($port - 8000) . '.css';
    if (!is_readable($path)) return '';
    return "<style>\n" . file_get_contents($path) . "\n</style>";
}

/* Natas has NO visibility into CTFd's solve/scoring state -- they are
 * entirely separate systems, confirmed by inspection (no CTFd API calls,
 * webhooks, or shared session/DB anywhere in this target's build).
 * The best locally-observable proxy: level N is "solved" once a request
 * has successfully cleared HTTP Basic Auth on level (N+1)'s vhost, which
 * is only possible if the player already obtained level N's password.
 * cei_natas_mark_previous_level_solved() records that fact; this
 * function reads it back for the CURRENT level being rendered. natas14
 * has no natas15 to observe, so it can never report solved -- documented
 * limitation, not a bug (see generate_themes.py's module docstring). */
function cei_natas_theme_state() {
    $port = isset($_SERVER['SERVER_PORT']) ? (int) $_SERVER['SERVER_PORT'] : 0;
    $level = $port - 8000;
    if ($level < 0 || $level > 14) return 'cei-locked';
    $marker = '/etc/cei-labs/natas-solve-state/natas' . $level . '.solved';
    return is_readable($marker) ? 'cei-solved' : 'cei-locked';
}

/* Called once per request (any content type, not just HTML) as early as
 * possible: reaching PHP execution on level N's vhost at all already
 * proves Apache's Require/AuthUserFile check passed for natasN, which is
 * the only signal we have. Marks level (N-1) solved -- the marker
 * directory is world-writable+sticky (mode 1777, like /tmp) since each
 * level runs as a distinct AssignUserID identity and there is no shared
 * group between them; the sticky bit stops one level's identity from
 * deleting/renaming another's marker, which is all the isolation these
 * empty boolean flag files need. */
function cei_natas_mark_previous_level_solved() {
    $port = isset($_SERVER['SERVER_PORT']) ? (int) $_SERVER['SERVER_PORT'] : 0;
    $level = $port - 8000;
    if ($level < 1 || $level > 14) return;
    $dir = '/etc/cei-labs/natas-solve-state';
    if (!is_dir($dir)) return;
    $marker = $dir . '/natas' . ($level - 1) . '.solved';
    if (!file_exists($marker)) {
        @touch($marker);
        @chmod($marker, 0644);
    }
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
    $banner = cei_natas_banner_fragment();
    $style = cei_natas_theme_style_fragment();
    $state = cei_natas_theme_state();
    if ($banner === '' && $style === '') return $output;
    $done = true;
    /* Inject the theme <style> before </head> (falls back to prepending
     * it) and add the locked/solved class onto <body ...> alongside the
     * existing banner-text fragment. */
    if ($style !== '' && stripos($output, '</head>') !== false) {
        $output = preg_replace('/<\/head>/i', $style . '</head>', $output, 1);
    } elseif ($style !== '') {
        $output = $style . $output;
    }
    if (preg_match('/<body\b([^>]*)>/i', $output, $match, PREG_OFFSET_CAPTURE)) {
        $attrs = $match[1][0];
        if (preg_match('/\bclass\s*=\s*"([^"]*)"/i', $attrs, $cmatch)) {
            $new_attrs = preg_replace('/\bclass\s*=\s*"([^"]*)"/i', 'class="$1 ' . $state . '"', $attrs, 1);
        } else {
            $new_attrs = $attrs . ' class="' . $state . '"';
        }
        $new_tag = '<body' . $new_attrs . '>';
        $tag_start = $match[0][1];
        $tag_len = strlen($match[0][0]);
        $at = $tag_start + $tag_len;
        $output = substr($output, 0, $tag_start) . $new_tag . $banner . substr($output, $at);
        return $output;
    }
    return $banner . $output;
}
cei_natas_mark_previous_level_solved();
ob_start('cei_natas_banner_filter');
?>
