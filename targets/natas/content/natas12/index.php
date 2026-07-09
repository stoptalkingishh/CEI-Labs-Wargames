<?php
if (isset($_GET['source'])) {
    highlight_file(__FILE__);
    exit;
}

$uploaddir = "uploads/";
$msg = "";
if (isset($_POST['submit']) && isset($_FILES['uploadedfile'])) {
    // No validation at all beyond a basename() strip -- whatever
    // filename and content you send is trusted and saved as-is, then
    // served directly out of uploads/. That is the entire lesson.
    $filename = basename($_FILES['uploadedfile']['name']);
    $target = $uploaddir . $filename;
    if (move_uploaded_file($_FILES['uploadedfile']['tmp_name'], $target)) {
        $msg = "File uploaded: <a href=\"" . htmlspecialchars($target) . "\">" . htmlspecialchars($target) . "</a>";
    } else {
        $msg = "Upload failed";
    }
}
?>
<html>
<head><title>natas12</title></head>
<body>
<h3>natas12</h3>
<form enctype="multipart/form-data" method="post">
<input type="hidden" name="MAX_FILE_SIZE" value="1000000">
Choose a JPEG to upload (max 1000KB): <input name="uploadedfile" type="file"><br>
<input type="submit" name="submit" value="Upload File">
</form>
<?php echo $msg; ?>
<p><a href="?source">View sourcecode</a></p>
</body>
</html>
