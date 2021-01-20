<?php
$pdo = new PDO('mysql:host=localhost;dbname=realtimebi', 'janlevent', 'DigitalBoardroom2021');


$data = [];


$statement = $pdo->prepare("SELECT Bestellung.Typ, m1.Status, m1.Typ, SUM(m1.Materialkosten) AS Materialkosten, SUM(Bestellung.Preis) AS Umsatz, ((SUM(Bestellung.Preis) - SUM(m1.Materialkosten)) / SUM(Bestellung.Preis)) AS MargeSM, AVG(m1.Materialkosten) AS MaterialkostenAVG, AVG(Bestellung.Preis) AS UmsatzAVG, ((AVG(Bestellung.Preis) - AVG(m1.Materialkosten)) / AVG(Bestellung.Preis)) AS MargeAVG FROM Bestellung NATURAL JOIN (SELECT Auto.Auto_ID, Auto.Typ, Auto.Status, Auto.Wert AS VerbauterWert, SUM(Komponente.Preis) AS Materialkosten FROM Auto JOIN Komponente ON Auto.Auto_ID = Komponente.Auto_ID GROUP BY Auto.Auto_ID) AS m1 WHERE m1.Status <=4 GROUP BY Bestellung.Typ");
    $statement->execute();  

while($row = $statement->fetch()) {
	$marge = $row['MargeAVG'] *100;
	$marge = floor($marge);
	array_push($data, ["Typ" => $row['Typ'], "Marge" => $marge]);
}

header('Content-Type: application/json');
echo json_encode($data);

?>