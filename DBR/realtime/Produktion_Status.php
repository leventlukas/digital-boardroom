<?php
$pdo = new PDO('mysql:host=localhost;dbname=realtimebi', 'janlevent', 'DigitalBoardroom2021');


$data = [];
array_push($data, ["Status" => "Eingeplant", "Anzahl" => 0]);
array_push($data, ["Status" => "Karroserie", "Anzahl" => 0]);
array_push($data, ["Status" => "Farbe", "Anzahl" => 0]);
array_push($data, ["Status" => "Batterie", "Anzahl" => 0]);
array_push($data, ["Status" => "Innenraum", "Anzahl" => 0]);
array_push($data, ["Status" => "Lager", "Anzahl" => 0]);


$statement = $pdo->prepare("SELECT Status, COUNT(Status) FROM Auto WHERE NOT Status = 6 GROUP BY Status");
    $statement->execute();  

while($row = $statement->fetch()) {
	if($row['Status'] == 0){
	$data[0]['Anzahl'] = $row['COUNT(Status)'];
	}
	if($row['Status'] == 1){
	$data[1]['Anzahl'] = $row['COUNT(Status)'];
	}
	if($row['Status'] == 2){
	$data[2]['Anzahl'] = $row['COUNT(Status)'];
	}
	if($row['Status'] == 3){
	$data[3]['Anzahl'] = $row['COUNT(Status)'];
	}
	if($row['Status'] == 4){
	$data[4]['Anzahl'] = $row['COUNT(Status)'];
	}
	if($row['Status'] == 5){
	$data[5]['Anzahl'] = $row['COUNT(Status)'];
	}
}

header('Content-Type: application/json');
echo json_encode($data);

?>