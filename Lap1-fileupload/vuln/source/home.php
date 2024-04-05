<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);
session_start();
$db = new SQLite3('database.db');
if (!isset($_SESSION['user_id'])) {
    header("Location: index.php");
    exit();
}
function getInformation($db, $id) {
    $stmt = $db->prepare("SELECT * FROM users WHERE id = ?");
    $stmt->bindValue(1, $id, SQLITE3_TEXT);
    $result = $stmt->execute();
    return $result->fetchArray(SQLITE3_ASSOC);
}
$userDetail = null;
if (isset($_SESSION['user_id'])) {
    $id = $_SESSION['user_id'];
    $userDetail = getInformation($db, $id);
}
include 'home.html';
?>
