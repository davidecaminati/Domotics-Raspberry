<html>
<head>
<link href='../css/style.css' rel='stylesheet' type='text/css' />
<link rel="stylesheet" type="text/css" href="../Flotr2/css/Flotr2.css">
<script type='text/javascript' src='../Flotr2/flotr2.min.js'></script>
<script type='text/javascript' src='../Flotr2/flotr2_box_plot.js'></script>
<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js"></script>
</head>
<body>
<?include("../include/header.php")?>

<div id=grafico>
<h2>Raspberry Pi - Monitoraggio temperatura</h2>
<p>Dati aggiornati alle ore <?=date("h:i:s")?> del <?=date("d/m/Y")?></p>
<div id='chart' style='height: 400px ; width: 90%'/>

<script type='text/javascript' src='termo.js'></script>
<script language=javascript>

<?
if (!$_REQUEST['start'] && !$_REQUEST['end']) {
	$start=-144;
	$end=-1;
} else {
	$start=$_REQUEST['start'];
	$end=$_REQUEST['end'];
}
$redis = new Redis();
$redis->connect('127.0.0.1', 6379);
$redis->setOption(Redis::OPT_SERIALIZER, Redis::SERIALIZER_NONE);

//$count = $redis->dbSize();

$lettura      = $redis->lRange('lettura', $start, $end);
$timestamp    = $redis->lRange('timestamp', $start, $end);
$temp_esterna = $redis->lRange('temp_esterna', $start, $end);
$termo        = $redis->lRange('termo', $start, $end);
$rele         = $redis->lRange('rele', $start, $end);
$temp_1       = $redis->lRange('temp_1', $start, $end);
$temp_2       = $redis->lRange('temp_2', $start, $end);
$temp_3       = $redis->lRange('temp_3', $start, $end);
$min	      = $redis->lRange('min', $start, $end);
$max	      = $redis->lRange('max', $start, $end);

for ($x=0;$x<=(abs($start)-1);$x++) {
	echo "d0='$lettura[$x]';\t";
	if (is_numeric($temp_esterna[$x])) {
		echo "d1.push([" . $timestamp[$x] . "," . $temp_esterna[$x] . "]);\t";
		$temp_esterna_precedente=$temp_esterna[$x];
	}  else {
		echo "d1.push([" . $timestamp[$x] . "," . $temp_esterna_precedente . "]);\t";
	}
	echo "d2.push([" . $timestamp[$x] . "," . ($termo[$x]+10) . "]);\t";
	echo "d3.push([" . $timestamp[$x] . "," . $temp_1[$x] . "]);\n";
	echo "d4.push([" . $timestamp[$x] . "," . $temp_2[$x] . "]);\n";
	echo "d5.push([" . $timestamp[$x] . "," . $temp_3[$x] . "]);\n";
	echo "d6.push([" . $timestamp[$x] . "," . (($min[$x]+$max[$x])/2) . "]);\n";
	
/*	if (date("H", $timestamp[$x]) > 6 &&  (date("H", $timestamp[$x]) <=23 )) { 
		echo "d6.push([" . $timestamp[$x] . ",21.25]);\n";
	} else {
		echo "d6.push([" . $timestamp[$x] . ",19.75]);\n";
	}
*/
	if (date("H", $timestamp[$x]) > 6 &&  (date("H", $timestamp[$x]) <=23 )) { 
		echo "d7.push([" . $timestamp[$x] . "," . ($rele[$x]+18) .  "]);\n";
	} else {
		echo "d7.push([" . $timestamp[$x] . "," . ($rele[$x]+18) ."]);\n";
	}
}

?>
data = [{data:d1, label: "Temp. esterna"}, {data:d2,label:"Riscaldamento"},{data:d3,label:"Temperatura camera"},{data:d4, label: "Temperatura camerina"},{data:d5, label: "Temperatura cucina"},{data:d6, label: "Temperatura impostata"},{data:d7, label: "Simulazione termostato"}];
//data = [{data:d1, label: "Temp. esterna"}, {data:d2,label:"Riscaldamento"},{data:d3,label:"Temperatura primo piano"},{data:d4, label: "Temperatura 2"},{data:d5, label: "Temperatura 3"},{data:d6, label: "Temperatura impostata"}];
graph = Flotr.draw(
		container,  // Container element
		data,
		options     // Configuration options
		);
</script>
</div>
<div>Download Image</div>
<div>
<form name="image-download" id="image-download" action="" onsubmit="return false">
<label><input name="format" value="png" checked="checked" type="radio"> PNG</label>
<label><input name="format" value="jpeg" type="radio"> JPEG</label>
<button name="to-image" onclick="CurrentExample('to-image')">To Image</button>
<button name="download" onclick="CurrentExample('download')">Download</button>
<button name="reset" onclick="CurrentExample('reset')">Reset</button>
</form>
</div>
</div>
<div>
<pre>
<?
$comando="/root/redis_2_csv.sh " . $start . " " . $end;
$esito=`$comando`;
echo "$esito";
?>
</pre>
</div>
</body>
