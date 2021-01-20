<?php
$db = mysqli_connect("localhost", "janlevent", "DigitalBoardroom2021", "realtimebi");
if(!$db)
{
  exit("Verbindungsfehler: ".mysqli_connect_error());
}
$typen = array('Typ', 'Batterie', 'Farbe', 'Innenraum');

$data = [];
	array_push($data, ["Typ" => 'Karroserie', "Menge" => 0, "Preis" => 0]);
	array_push($data, ["Typ" => 'Batterie', "Menge" => 0, "Preis" => 0]);
	array_push($data, ["Typ" => 'Lack', "Menge" => 0, "Preis" => 0]);
	array_push($data, ["Typ" => 'Leder', "Menge" => 0, "Preis" => 0]);

for ($i = 0; $i < count($typen); $i++) {
	$typSql = $typen[$i];
	$abfrage = "SELECT AVG(Preis) AS preis FROM Komponente WHERE LagerID = 1 AND Typ = '$typSql'";
	$ergebnis = mysqli_query($db, $abfrage);
	while($row = mysqli_fetch_object($ergebnis))
	{
  	$preis = $row->preis;
	}
	$abfrage = "SELECT COUNT(Preis) AS anzahl FROM Komponente WHERE LagerID = 1 AND Typ = '$typSql'";
	$ergebnis = mysqli_query($db, $abfrage);
	while($row = mysqli_fetch_object($ergebnis))
	{
  	$anzahl = $row->anzahl;
	}
	
	$preis = floor($preis);
	$preis_form = number_format($preis, 0, ',', '.');
	$data[$i]['Preis'] = $preis_form;
	$data[$i]['Menge'] = $anzahl;

}



header('Content-Type: application/json');
echo json_encode($data);

?>