<?php
$pdo = new PDO('mysql:host=localhost;dbname=realtimebi', 'janlevent', 'DigitalBoardroom2021');

$data = [];

	array_push($data, ["Kategorie" => 'Rohstoffe', "Menge" => 0, "Wert" => 0]);
	array_push($data, ["Kategorie" => 'Unfertig', "Menge" => 0, "Wert" => 0]);
	array_push($data, ["Kategorie" => 'Fertig', "Menge" => 0, "Wert" => 0]);


$statement = $pdo->prepare("SELECT SUM(Preis) AS Wert, COUNT(KompID) AS Menge FROM Komponente WHERE Einbau IS NULL");
    $statement->execute();  

while($row = $statement->fetch()) {
	$data[0]['Menge'] = $row['Menge'];
	
	$data[0]['Wert'] = 	$preis_form = number_format($row['Wert'], 0, ',', '.');
}

$statement = $pdo->prepare("SELECT SUM(Wert) AS Wert, COUNT(Auto_ID) AS Menge FROM Auto WHERE Status <= 4");
    $statement->execute();  

while($row = $statement->fetch()) {
	$data[1]['Menge'] = $row['Menge'];
	$data[1]['Wert'] = 	$preis_form = number_format($row['Wert'], 0, ',', '.');
}

$statement = $pdo->prepare("SELECT SUM(Wert) AS Wert, COUNT(Auto_ID) AS Menge FROM Auto WHERE Status = 5");
    $statement->execute();  

while($row = $statement->fetch()) {
	$data[2]['Menge'] = $row['Menge'];
	$data[2]['Wert'] = 	$preis_form = number_format($row['Wert'], 0, ',', '.');
}

header('Content-Type: application/json');
echo json_encode($data);

?>