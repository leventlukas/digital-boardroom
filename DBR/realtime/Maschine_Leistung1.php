<?php

date_default_timezone_set('Europe/Berlin');

$pdo = new PDO('mysql:host=localhost;dbname=realtimebi', 'janlevent', 'DigitalBoardroom2021');


$data = [];

$akHour = date("G")-1;
$akMin = date("i");
$akDay = date("j");
for ($i = 0; $i <= 60; $i++) {

if($akMin <= 59){
    $statement = $pdo->prepare("SELECT AVG(Produktivitaet) AS Produktivitaet FROM ProduktivitaetVerlauf_Maschine WHERE DAY(Timestmp) = $akDay AND HOUR(Timestmp) = $akHour AND MINUTE(Timestmp) = $akMin AND MaschinenID = 1");
    $statement->execute();  
    $row = $statement->fetch();
    $zeitProduktivitaet = $row['Produktivitaet'];
	if(is_null($zeitProduktivitaet)){
	$zeitProduktivitaet = 0;
	}else{
	$zeitProduktivitaet = floor($zeitProduktivitaet);
	}
    array_push($data, ["Maschine" => 1, "stunde" => $akHour, "minute" => $akMin, "Produktivitaet" => $zeitProduktivitaet]);
    $akMin = $akMin + 1;

}elseif($akMin == 60){
    $akMin = 0;
    $akHour = $akHour+1;
    $statement = $pdo->prepare("SELECT AVG(Produktivitaet) AS Produktivitaet FROM ProduktivitaetVerlauf_Maschine WHERE DAY(Timestmp) = $akDay AND HOUR(Timestmp) = $akHour AND MINUTE(Timestmp) = $akMin AND MaschinenID = 1");
    $statement->execute();  
    $row = $statement->fetch();
    $zeitProduktivitaet = $row['Produktivitaet'];
		if(is_null($zeitProduktivitaet)){
	$zeitProduktivitaet = 0;
	}else{
	$zeitProduktivitaet = floor($zeitProduktivitaet);
	}
    array_push($data, ["Maschine" => 1, "stunde" => $akHour, "minute" => $akMin, "Produktivitaet" => $zeitProduktivitaet]);
    $akMin = $akMin + 1;
}
}


array_pop($data);
header('Content-Type: application/json');
echo json_encode($data);

?>