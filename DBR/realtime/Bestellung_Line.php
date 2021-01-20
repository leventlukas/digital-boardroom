<?php

date_default_timezone_set('Europe/Berlin');

$pdo = new PDO('mysql:host=localhost;dbname=realtimebi', 'janlevent', 'DigitalBoardroom2021');


$akHour = date("G")-1;
$akMin = date("i");

$akDay = date("j");


$data = [];
for ($i = 0; $i <= 60; $i++) {

if($akMin <= 59){
    $statement = $pdo->prepare("SELECT COUNT(*) AS anzahl FROM Bestellung WHERE DAY(Eingang) = $akDay AND HOUR(Eingang) = $akHour AND MINUTE(Eingang) = $akMin");
    $statement->execute();  
    $row = $statement->fetch();
    $zeitBestellung = $row['anzahl'];
    array_push($data, ["stunde" => $akHour, "minute" => $akMin, "count" => $zeitBestellung]);
    $akMin = $akMin + 1;

}elseif($akMin == 60){
    $akMin = 0;
    $akHour = $akHour+1;
    $statement = $pdo->prepare("SELECT COUNT(*) AS anzahl FROM Bestellung WHERE DAY(Eingang) = $akDay AND HOUR(Eingang) = $akHour AND MINUTE(Eingang) = $akMin");
    $statement->execute();  
    $row = $statement->fetch();
    $zeitBestellung = $row['anzahl'];
    array_push($data, ["stunde" => $akHour, "minute" => $akMin, "count" => $zeitBestellung]);
    $akMin = $akMin + 1;
}

}



header('Content-Type: application/json');
echo json_encode($data);

?>