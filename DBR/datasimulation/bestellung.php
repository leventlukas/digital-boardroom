<?php 

$db = mysqli_connect("localhost", "janlevent", "DigitalBoardroom2021", "realtimebi");
if(!$db)
{
  exit("Verbindungsfehler: ".mysqli_connect_error());
}

date_default_timezone_set('Europe/Berlin');
$timestamp = date("Y-m-d H:i:s");

$marktpreise = array(25000*1.5,11000*1.5,28000*1.5,2500*1.5,5000*1.5,11500*1.5,31500*1.5,500*1.5,1000*1.5,1000*1.5,1000*1.5, 1200*1.5, 2000*1.5, 3000*1.5);

$data = [
    ["id" => 1, "typ" => 'Typ', "ausfuehrung" => 'Model S',"menge" => $_POST['modell1'],"preis" => $marktpreise[0]],
	["id" => 2, "typ" => 'Typ', "ausfuehrung" => 'Model 3',"menge" => $_POST['modell2'],"preis" => $marktpreise[1]],
	["id" => 3, "typ" => 'Typ', "ausfuehrung" => 'Model X',"menge" => $_POST['modell3'],"preis" => $marktpreise[2]],
	["id" => 4, "typ" => 'Batterie', "ausfuehrung" => 'Standard',"menge" => $_POST['batterie1'],"preis" => $marktpreise[3]],
	["id" => 5, "typ" => 'Batterie', "ausfuehrung" => 'Maximale Reichweite',"menge" => $_POST['batterie2'],"preis" => $marktpreise[4]],
    ["id" => 6, "typ" => 'Batterie', "ausfuehrung" => 'Performance',"menge" => $_POST['batterie3'],"preis" => $marktpreise[5]],
	["id" => 7, "typ" => 'Batterie', "ausfuehrung" => 'Plaid',"menge" => $_POST['batterie4'],"preis" => $marktpreise[6]],
	["id" => 8, "typ" => 'Farbe', "ausfuehrung" => 'Pearl White Multi-Coat',"menge" => $_POST['farbe1'],"preis" => $marktpreise[7]],
	["id" => 9, "typ" => 'Farbe', "ausfuehrung" => 'Solid Black',"menge" => $_POST['farbe2'],"preis" => $marktpreise[8]],
	["id" => 10, "typ" => 'Farbe', "ausfuehrung" => 'Midnight Silver Metallic',"menge" => $_POST['farbe3'],"preis" => $marktpreise[9]],
    ["id" => 11, "typ" => 'Farbe', "ausfuehrung" => 'Deep Blue Metallic',"menge" => $_POST['farbe4'],"preis" => $marktpreise[10]],
	["id" => 12, "typ" => 'Farbe', "ausfuehrung" => 'Red Multi-Coat',"menge" => $_POST['farbe5'],"preis" => $marktpreise[11]],
	["id" => 13, "typ" => 'Innenraum', "ausfuehrung" => 'schwarz',"menge" => $_POST['leder1'],"preis" => $marktpreise[12]],
	["id" => 14, "typ" => 'Innenraum', "ausfuehrung" => 'weiss',"menge" => $_POST['leder2'],"preis" => $marktpreise[13]]
];



for ($i = 0; $i <= 14; $i++) {
	if($data[$i]['menge'] > 0){
	$itt = $data[$i]['menge'];
		for($j = 0; $j < $itt; $j++){
			$typtmp = $data[$i]['typ'];
			$ausfuehrungtmp = $data[$i]['ausfuehrung'];
			$preistmp = $data[$i]['preis'];
			$eintrag = "INSERT INTO Komponente (Typ, Ausfuehrung, Preis, Eingang, LagerID) VALUES ('$typtmp', '$ausfuehrungtmp', '$preistmp', '$timestamp', '1')";
			$eintragen = mysqli_query($db, $eintrag);
		}
		
	}
	
}
?>
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <title>Bestellung erfolgreich</title>
	<link rel="shortcut icon" type="image/x-icon" href="../assets/img/logo_rot.png">
    

    <!-- Bootstrap core CSS -->
<link href="../assets/dist/css/bootstrap.min.css" rel="stylesheet">

    <style>
      .bd-placeholder-img {
        font-size: 1.125rem;
        text-anchor: middle;
        -webkit-user-select: none;
        -moz-user-select: none;
        user-select: none;
      }

      @media (min-width: 768px) {
        .bd-placeholder-img-lg {
          font-size: 3.5rem;
		}
		body {
  height: 100%;
}

body {
  display: flex;
  align-items: center;
  padding-top: 40px;
  padding-bottom: 40px;
  background-color: #f5f5f5;
}
.form-signin {
  width: 100%;
  max-width: 500px;
  padding: 15px;
  margin: auto;
}
.form-signin .checkbox {
  font-weight: 400;
}
.form-signin .form-control {
  position: relative;
  box-sizing: border-box;
  height: auto;
  padding: 10px;
  font-size: 16px;
}
.form-signin .form-control:focus {
  z-index: 2;
}

      }
    </style>

  </head>
  <body class="text-center">
    
<main class="form-signin">
  <form action="http://realtime-bi.tk/DBR/datasimulation/" method="POST">
    <img class="mb-4" src="../assets/img/logo_rot.png" width = 80px alt="">
	<div class="alert alert-success" role="alert">Komponenten wurden erfolgreich bestellt.</div>
    </div>
	<button class=" btn btn-outline-primary" type="submit">Zurück</button>
	<hr>
  <p class="fw-light">&copy; by Levent Lukas & Jan Warwas</p>
  </form>
</main>


    
  </body>
</html>
