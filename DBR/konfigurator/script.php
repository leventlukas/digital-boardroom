
<?php 
error_reporting(E_ALL);

$db = mysqli_connect("localhost", "janlevent", "DigitalBoardroom2021", "realtimebi");
if(!$db)
{
  exit("Verbindungsfehler: ".mysqli_connect_error());
}


$rohstring = $_POST['orderjson'];
$roharray = str_split($rohstring);

$modellI = (int)$roharray[0];
$artI = (int)$roharray[1];
$farbeI = (int)$roharray[2];
$innenFarbeI = (int)$roharray[3];
$autopilotI = (int)$roharray[4];


$modellS = '';
$artS = '';
$farbeS = '';
$innenFarbeS = '';
$autopilotS = '';
$preisS = $_POST['orderjsonpreis'];

$modelleA = array("Model S", "Model 3", "Model X");
$modellS = $modelleA[$modellI];

if($modellI == 0){
	if($artI == 0){
	$artS = 'Maximale Reichweite';
	}else if ($artI == 1){
	$artS = 'Performance';
	}else if($artI == 2){
	$artS = 'Plaid';
	}
}else if ($modellI == 1){
	if($artI == 0){
	$artS = 'Standard Plus';
	}else if ($artI == 1){
	$artS = 'Maximale Reichweite';
	}else if($artI == 2){
	$artS = 'Performance';
	}
}else if($modellI == 2){
	if($artI == 0){
	$artS = 'Maximale Reichweite';
	}else if ($artI == 1){
	$artS = 'Performance';
	}
}

$farbenA = array("Pearl White Multi-Coat", "Solid Black", "Midnight Silver Metallic", "Deep Blue Metallic", "Red Multi-Coat");
$farbeS = $farbenA[$farbeI];


if($innenFarbeI == 0){
$innenFarbeS = 'schwarz';
}else{
$innenFarbeS = 'weiss';
}


if($autopilotI == 0){
$autopilotS = 'no';
}else{
$autopilotS = 'yes';
}

date_default_timezone_set('Europe/Berlin');
$timestamp = date("Y-m-d H:i:s");

$eintrag = "INSERT INTO Bestellung (Typ, Batterie, Innenraum, Farbe, AutoFahren, Eingang, Preis) VALUES ('$modellS', '$artS', '$innenFarbeS', '$farbeS', '$autopilotS', '$timestamp', '$preisS')";
$eintragen = mysqli_query($db, $eintrag);
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
  <form action="http://realtime-bi.tk/DBR/konfigurator" method="POST">
    <img class="mb-4" src="../assets/img/logo_rot.png" width = 80px alt="">
	<div class="alert alert-success" role="alert">Vielen Dank! Deine Bestellung <b>#<?php echo rand(10000, 99999); ?></b> war erfolgreich. Dein Fahrzeug wird jetzt produziert.</div>
    </div>
	<button class=" btn btn-outline-primary" type="submit">Zurück</button>
	<hr>
  <p class="fw-light">&copy; by Levent Lukas & Jan Warwas</p>
  </form>
</main>


    
  </body>
</html>









