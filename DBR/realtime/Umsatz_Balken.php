<?php

date_default_timezone_set('Europe/Berlin');

$pdo = new PDO('mysql:host=localhost;dbname=realtimebi', 'janlevent', 'DigitalBoardroom2021');


$akDay = date("j");
$akMonth = date("n");

$data = [];

$statement = $pdo->prepare("SELECT COUNT(*) AS anzahl FROM Bestellung WHERE DAY(Eingang) = $akDay AND MONTH(Eingang) = $akMonth");
$statement->execute();  
$row = $statement->fetch();
$anzahl = $row['anzahl'];

$statement = $pdo->prepare("SELECT SUM(PREIS) AS umsatz FROM Bestellung WHERE DAY(Eingang) = $akDay AND MONTH(Eingang) = $akMonth");
$statement->execute();  
$row = $statement->fetch();
$umsatz = $row['umsatz'];
if(!isset($umsatz)){
$umsatz = 0;
}

array_push($data, ["Datum" => "Heute", "Anzahl" => $anzahl, "Umsatz" => $umsatz]);

for ($i = 0; $i <= 4; $i++) {
	$akDay = $akDay - 1;
	$datum = str_pad($akDay, 2, 0, STR_PAD_LEFT) . "." . str_pad($akMonth, 2, 0, STR_PAD_LEFT);
	
	$statement = $pdo->prepare("SELECT COUNT(*) AS anzahl FROM Bestellung WHERE DAY(Eingang) = $akDay AND MONTH(Eingang) = $akMonth");
	$statement->execute();  
	$row = $statement->fetch();
	$anzahl = $row['anzahl'];
	
	$statement = $pdo->prepare("SELECT SUM(PREIS) AS umsatz FROM Bestellung WHERE DAY(Eingang) = $akDay AND MONTH(Eingang) = $akMonth");
	$statement->execute();  
	$row = $statement->fetch();
	$umsatz = $row['umsatz'];
	if(!isset($umsatz)){
	$umsatz = 0;
	}

	array_push($data, ["Datum" => $datum, "Anzahl" => $anzahl, "Umsatz" => $umsatz]);
	
}


header('Content-Type: application/json');
echo json_encode($data);

?>