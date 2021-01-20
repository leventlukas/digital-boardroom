<?php 
error_reporting(E_ALL);
$P_array = array($_POST['ms1'], $_POST['ms2'], $_POST['ms3'], $_POST['ms4']);
$S_array = array(" "," "," "," ");


$db = mysqli_connect("localhost", "janlevent", "DigitalBoardroom2021", "realtimebi");
if(!$db)
{
  exit("Verbindungsfehler: ".mysqli_connect_error());
}

for ($i = 0; $i <= 3; $i++) {
if($P_array[$i] == 0){
$S_array[$i] = "Kaputt";
}else if($P_array[$i] == 100){
$S_array[$i] = "Normal";
}else{
$S_array[$i] = "Warnung";
}	
}

for ($i = 1; $i <= 4; $i++) {
	$j = $i-1;
	$aendern = "UPDATE Maschine Set Produktivitaet = $P_array[$j], Status = '$S_array[$j]' WHERE MaschinenID = $i";
	$eintragen = mysqli_query($db, $aendern);
}

?>

<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <title>Maschinen Status aktualisiert</title>
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
	<div class="alert alert-success" role="alert">Maschinenstatus wurde erfolgreich aktualisiert.</div>
    </div>
	<button class=" btn btn-outline-primary" type="submit">Zurück</button>
	<hr>
  <p class="fw-light">&copy; by Levent Lukas & Jan Warwas</p>
  </form>
</main>


    
  </body>
</html>

