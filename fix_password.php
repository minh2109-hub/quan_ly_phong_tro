<?php
require_once "config/database.php";
$hashAdmin = password_hash("Admin@123", PASSWORD_DEFAULT);
$hashUser  = password_hash("User@123", PASSWORD_DEFAULT);

$pdo->prepare("UPDATE users SET password=? WHERE username=?")->execute([$hashAdmin, "admin"]);
$pdo->prepare("UPDATE users SET password=? WHERE username=?")->execute([$hashUser, "nguyen.van.a"]);
$pdo->prepare("UPDATE users SET password=? WHERE username=?")->execute([$hashUser, "tran.thi.b"]);
$pdo->prepare("UPDATE users SET password=? WHERE username=?")->execute([$hashUser, "le.van.c"]);

echo "OK: Da cap nhat mat khau thanh cong!\n";
echo "admin / Admin@123 -> hash: " . $hashAdmin . "\n";
echo "nguyen.van.a / User@123 -> hash: " . $hashUser . "\n";

// Xac nhan
$u = $pdo->query("SELECT username,password FROM users")->fetchAll();
foreach($u as $row) {
    $test = "";
    if($row["username"] === "admin") $test = password_verify("Admin@123", $row["password"]) ? "DUNG" : "SAI";
    else $test = password_verify("User@123", $row["password"]) ? "DUNG" : "SAI";
    echo $row["username"] . ": " . $test . "\n";
}
?>