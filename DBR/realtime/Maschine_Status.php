<?php
$db = mysqli_connect("localhost", "janlevent", "DigitalBoardroom2021", "realtimebi");
if(!$db)
{
  exit("Verbindungsfehler: ".mysqli_connect_error());
}

$avg = 0;
$data = [];
	$abfrage = "SELECT MaschinenID, Produktivitaet FROM Maschine";
	$ergebnis = mysqli_query($db, $abfrage);
	while($row = mysqli_fetch_object($ergebnis))
	{
  $MID = $row->MaschinenID;
  $PROD = $row ->Produktivitaet;
  array_push($data, ["mid" => $MID, "prod" => $PROD]);
	}



header('Content-Type: application/json');
echo json_encode($data);

?>