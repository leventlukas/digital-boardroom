<?php
$pdo = new PDO('mysql:host=localhost;dbname=realtimebi', 'janlevent', 'DigitalBoardroom2021');


$data = [];
array_push($data, ["Status" => "Ungeplant", "Anzahl" => 0]);
array_push($data, ["Status" => "Eingeplant", "Anzahl" => 0]);
array_push($data, ["Status" => "In Produktion", "Anzahl" => 0]);
array_push($data, ["Status" => "Lagernd", "Anzahl" => 0]);

$count = 0;
$statement = $pdo->prepare("SELECT Status, COUNT(Bestellung_ID) FROM Bestellung LEFT JOIN Auto ON Bestellung.Auto_ID = Auto.Auto_ID GROUP BY Status");
    $statement->execute();  

while($row = $statement->fetch()) {
	if(is_null($row['Status'])){
	$data[0]['Anzahl'] = $row['COUNT(Bestellung_ID)'];
	}
	if($row['Status'] == 0 && !is_null($row['Status'])){
	$data[1]['Anzahl'] = $row['COUNT(Bestellung_ID)'];
	}
	if($row['Status'] == 1){
	$count = $count + $row['COUNT(Bestellung_ID)'];
	}
	if($row['Status'] == 2){
		$count = $count + $row['COUNT(Bestellung_ID)'];
	}
	if($row['Status'] == 3){
		$count = $count + $row['COUNT(Bestellung_ID)'];
	}
	if($row['Status'] == 4){
		$count = $count + $row['COUNT(Bestellung_ID)'];
	}
	if($row['Status'] == 5){
	$data[3]['Anzahl'] = $row['COUNT(Bestellung_ID)'];
	}
}

	$data[2]['Anzahl'] = $count;
header('Content-Type: application/json');
echo json_encode($data);

?>