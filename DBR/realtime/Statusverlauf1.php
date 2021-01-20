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
/*
$data_time = [];
$startStd = $data[0]['stunde'];
$endStd = 0;
$startMin = $data[0]['minute'];
$endMin = 0;
$statusTmp = $data[0]['Produktivitaet'];
$noChange = false;

for ($i = 0; $i <= 60; $i++) {
	
	if($data[$i]['Produktivitaet'] !== $statusTmp){
	
		$noChange = false;
		$endStd = $data[$i]['stunde'];
	$endMin = $data[$i]['minute'];
	
	array_push($data_time, ["Maschine" => 1, "startStd" => $startStd, "startMin" => $startMin, "endStd" => $endStd,"endMin" => $endMin, "Status" => $statusTmp]);
	
		$startStd = $data[$i]['stunde'];	
		$startMin = $data[$i]['minute'];
		
		$statusTmp = $data[$i]['Produktivitaet'];
	}
}
	if($endStd !== $data[60]['stunde'] && $endMin !== $data[60]['minute']){
	
	array_push($data_time, ["Maschine" => 1, "startStd" => $startStd, "startMin" => $startMin, "endStd" => $data[60]['stunde'],"endMin" => $data[60]['minute'], "Status" => $statusTmp]);
	
	}
if($noChange){
	array_push($data_time, ["Maschine" => 1, "startStd" => $data[0]['stunde'], "startMin" => $data[0]['minute'], "endStd" => $data[60]['stunde'],"endMin" => $data[60]['minute'], "Status" => $statusTmp]);
}
*/
header('Content-Type: application/json');
echo json_encode($data);

?>