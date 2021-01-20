<?php

$dbname =   "realtimebi";
$dbhost =   "realtime-bi.tk";
$dbuser =   "janlevent";
$dbpass =   "DigitalBoardroom2021";



$mysqli = new mysqli($dbhost,$dbuser,$dbpass,$dbname);

if ($mysqli->connect_errno) {
    echo "Failed to connect to MySQL: (" . $mysqli->connect_errno . ") " . $mysqli->connect_error;
}

$result = $mysqli->query("SELECT Typ, COUNT(*) AS Anzahl FROM Bestellung GROUP BY Typ");


$data = $result->fetch_all(MYSQLI_ASSOC);
header('Content-Type: application/json');
echo json_encode($data);

?>