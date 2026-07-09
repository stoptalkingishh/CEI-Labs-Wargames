<?php
if (isset($_GET['source'])) {
    highlight_file(__FILE__);
    exit;
}

$uploaddir = "uploads/";
$msg = "";
if (isset($_POST['submit']) && isset($_FILES['uploadedfile'])) {
    $tmp = $_FILES['uploadedfile']['tmp_name'];
    $imageinfo = @exif_imagetype($tmp);
    if ($imageinfo != IMAGETYPE_JPEG && $imageinfo != IMAGETYPE_PNG && $imageinfo != IMAGETYPE_GIF) {
        $msg = "File is not an image";
    } else {
        $filename = basename($_FILES['uploadedfile']['name']);
        $target = $uploaddir . $filename;
        if (move_uploaded_file($tmp, $target)) {
            $msg = "File uploaded: <a href=\"" . htmlspecialchars($target) . "\">" . htmlspecialchars($target) . "</a>";
        } else {
            $msg = "Upload failed";
        }
    }
}
?>
<html>
<head><title>natas13</title></head>
<body>
<h3>natas13</h3>
<form enctype="multipart/form-data" method="post">
<input type="hidden" name="MAX_FILE_SIZE" value="1000000">
Choose a JPEG to upload (max 1000KB): <input name="uploadedfile" type="file"><br>
<input type="submit" name="submit" value="Upload File">
</form>
<?php echo $msg; ?>
<p><a href="?source">View sourcecode</a></p>
</body>
</html>
