<?php
$db = mysqli_connect("localhost", "janlevent", "DigitalBoardroom2021", "realtimebi");
if(!$db)
{
  exit("Verbindungsfehler: ".mysqli_connect_error());
}

$avg = 0;
$data = [];
	$abfrage = "SELECT TIME_TO_SEC(Ausgang) - TIME_TO_SEC(Eingang) AS Differenz FROM Bestellung WHERE Ausgang IS NOT NULL Order BY Ausgang DESC LIMIT 20";
	$ergebnis = mysqli_query($db, $abfrage);
	while($row = mysqli_fetch_object($ergebnis))
	{
  	$diff = $row->Differenz;
	$avg = $avg + $diff;
	}

	$avg = $avg/20;
	$diff_array = secondsToTime($avg);
	array_push($data, ["d" => $diff_array['d'], "h" => $diff_array['h'], "m" => $diff_array['m'], "s" => $diff_array['s']]);



	

function secondsToTime($inputSeconds) {

    $secondsInAMinute = 60;
    $secondsInAnHour  = 60 * $secondsInAMinute;
    $secondsInADay    = 24 * $secondsInAnHour;

    // extract days
    $days = floor($inputSeconds / $secondsInADay);

    // extract hours
    $hourSeconds = $inputSeconds % $secondsInADay;
    $hours = floor($hourSeconds / $secondsInAnHour);

    // extract minutes
    $minuteSeconds = $hourSeconds % $secondsInAnHour;
    $minutes = floor($minuteSeconds / $secondsInAMinute);

    // extract the remaining seconds
    $remainingSeconds = $minuteSeconds % $secondsInAMinute;
    $seconds = ceil($remainingSeconds);

    // return the final array
    $obj = array(
        'd' => (int) $days,
        'h' => (int) $hours,
        'm' => (int) $minutes,
        's' => (int) $seconds,
    );
    return $obj;
}



header('Content-Type: application/json');
echo json_encode($data);

?>