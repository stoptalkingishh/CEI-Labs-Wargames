<?php
// Deliberately NOT inlined into index.php: this level's whole point is
// recovering this key via a known-plaintext XOR attack, not reading it.
// highlight_file(__FILE__) in index.php only dumps THAT file's own text,
// never an included file's contents -- same trick already used there for
// $next_password. This file produces no output on its own if requested
// directly (no echo), so a direct GET returns an empty response.
$xor_key = 'qw8J';
