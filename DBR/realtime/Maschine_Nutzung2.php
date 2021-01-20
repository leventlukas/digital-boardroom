<?php

date_default_timezone_set('Europe/Berlin');

$pdo = new PDO('mysql:host=localhost;dbname=realtimebi', 'janlevent', 'DigitalBoardroom2021');


$data = [];
$akHour = date("G")-1;
$akMin = date("i");
$akDay = date("j");
for ($i = 0; $i <= 60; $i++) {

if($akMin <= 59){
    $statement = $pdo->prepare("SELECT AVG(Auslastung) AS Auslastung FROM Auslastung_Maschine WHERE DAY(Timestmp) = $akDay AND HOUR(Timestmp) = $akHour AND MINUTE(Timestmp) = $akMin AND MaschinenID = 2");
    $statement->execute();  
    $row = $statement->fetch();
    $zeitAuslastung = $row['Auslastung'];
	if(is_null($zeitAuslastung)){
	$zeitAuslastung = 0;
	}else{
	$zeitAuslastung = floor($zeitAuslastung*100);
	}
    array_push($data, ["Maschine" => 2, "stunde" => $akHour, "minute" => $akMin, "Auslastung" => $zeitAuslastung]);
    $akMin = $akMin + 1;

}elseif($akMin == 60){
    $akMin = 0;
    $akHour = $akHour+1;
    $statement = $pdo->prepare("SELECT AVG(Auslastung) AS Auslastung FROM Auslastung_Maschine WHERE DAY(Timestmp) = $akDay AND HOUR(Timestmp) = $akHour AND MINUTE(Timestmp) = $akMin AND MaschinenID = 2");
    $statement->execute();  
    $row = $statement->fetch();
    $zeitAuslastung = $row['Auslastung'];
		if(is_null($zeitAuslastung)){
	$zeitAuslastung = 0;
	}else{
	$zeitAuslastung = floor($zeitAuslastung*100);
	}
    array_push($data, ["Maschine" => 2, "stunde" => $akHour, "minute" => $akMin, "Auslastung" => $zeitAuslastung]);
    $akMin = $akMin + 1;
}
}


array_pop($data);
header('Content-Type: application/json');
echo json_encode($data);

?>