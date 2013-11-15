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
$redis->set('t_min_notte',$_GET["t_notte"]-0.25);
$redis->set('t_max_notte',$_GET["t_notte"]+0.25);
$redis->set('t_min_giorno',$_GET["t_giorno"]-0.25);
$redis->set('t_max_giorno',$_GET["t_giorno"]+0.25);
$t_min_notte=$redis->get('t_min_notte');
$t_max_notte=$redis->get('t_max_notte');
$t_min_giorno=$redis->get('t_min_giorno');
$t_max_giorno=$redis->get('t_max_giorno');
?>
<body style="text-align: center">
<div align=center style="width: 100%">
<h2>Regolazione temperature termostato</h2>
<table style="width: 80%; border: 1px solid" >
<tr>
<td rowspan=2 style="text-align:center; vertical-align: middle">
<img src=termometro.png>
</td>
<td>
<h3>Temperatura della notte</h3>
Impostazioni attuali:
<div>min: <?=$t_min_notte?>, max: <?=$t_max_notte?>, media: <?=(($t_min_notte+$t_max_notte)/2)?></div>
<div id="uno" style="font-size: 36px; font-weight: bold; color: blue; "><?=(($t_min_notte+$t_max_notte)/2)?></div>
</td></tr>
<tr><td>
<h3>Temperatura del giorno</h3>
<div>min: <?=$t_min_giorno?>, max: <?=$t_max_giorno?>, media: <?=(($t_min_giorno+$t_max_giorno)/2)?></div>
<div id="dos" style="font-size: 36px; font-weight: bold; color: red; "><?=(($t_min_giorno+$t_max_giorno)/2)?></div>
</td>
</tr>
</table>
</div>
<br>
</body>
