<html>
<head>
<script src=../lib/html5slider.js>
</script>
<link href='../css/style.css' rel='stylesheet' type='text/css' />
</head>
<?include("../include/header.php")?>
<?
$redis = new Redis();
$redis->connect('127.0.0.1', 6379);
$redis->setOption(Redis::OPT_SERIALIZER, Redis::SERIALIZER_NONE);
$redis->set('temp_min_night',$_GET["t_notte"]-0.25);
$redis->set('temp_max_night',$_GET["t_notte"]+0.25);
$redis->set('temp_min_day',$_GET["t_giorno"]-0.25);
$redis->set('temp_max_day',$_GET["t_giorno"]+0.25);
$temp_min_night=$redis->get('temp_min_night');
$temp_max_night=$redis->get('temp_max_night');
$temp_min_day=$redis->get('temp_min_day');
$temp_max_day=$redis->get('temp_max_day');
?>
<body style="text-align: center">
<div align=center style="width: 100%">
<h2>Temp settings</h2>
<table style="width: 80%; border: 1px solid" >
<tr>
<td rowspan=2 style="text-align:center; vertical-align: middle">
<img src=termometro.png>
</td>
<td>
<h3>Night temp</h3>
<div>min: <?=$temp_min_night?>, max: <?=$temp_max_night?>, media: <?=(($temp_min_night+$temp_max_night)/2)?></div>
<div id="uno" style="font-size: 36px; font-weight: bold; color: blue; "><?=(($temp_min_night+$temp_max_night)/2)?></div>
</td></tr>
<tr><td>
<h3>Day temp</h3>
<div>min: <?=$temp_min_day?>, max: <?=$temp_max_day?>, media: <?=(($temp_min_day+$temp_max_day)/2)?></div>
<div id="dos" style="font-size: 36px; font-weight: bold; color: red; "><?=(($temp_min_day+$temp_max_day)/2)?></div>
</td>
</tr>
</table>
</div>
<br>
</body>
