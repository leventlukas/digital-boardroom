
<?php

$dbname =   "realtimebi";
$dbhost =   "realtime-bi.tk";
$dbuser =   "janlevent";
$dbpass =   "DigitalBoardroom2021";


$data = [];
$mysqli = new mysqli($dbhost,$dbuser,$dbpass,$dbname);

if ($mysqli->connect_errno) {
    echo "Failed to connect to MySQL: (" . $mysqli->connect_errno . ") " . $mysqli->connect_error;
}

$result = $mysqli->query("SELECT Eingang, Typ, Batterie, Innenraum, Farbe, Preis, Eingang FROM Bestellung ORDER BY Bestellung_ID DESC LIMIT 10");
    while ($row = mysqli_fetch_assoc($result)) {
	$eingang = $row['Eingang'];
	$date = date_create($eingang);
	$eingang_form = date_format($date, 'd.m.Y H:i:s');
	
	$preis_form = number_format($row['Preis'], 0, ',', '.');
    array_push($data, ["Eingang" => $eingang_form, "Typ" => $row['Typ'], "Batterie" => $row['Batterie'], "Farbe" => $row['Farbe'], "Leder" => $row['Innenraum'], "Preis" => $preis_form]);		
    }

//$data = $result->fetch_all(MYSQLI_ASSOC);
header('Content-Type: application/json');
echo json_encode($data);

?>