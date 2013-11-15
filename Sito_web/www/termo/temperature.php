<html>
<head>
<script src=../lib/html5slider.js>
</script>
<link href='../css/style.css' rel='stylesheet' type='text/css' />
</head>
<script type="text/javascript">
onload = function() {
  document.getElementById('one').onchange = function() {
      document.getElementById('uno').innerHTML = this.value;
  };
  document.getElementById('one').onchange();
  document.getElementById('two').onchange = function() {
      document.getElementById('dos').innerHTML = this.value;
      document.getElementById('dos').value = this.value;
  };
  document.getElementById('two').onchange();
/*  document.getElementById('mm1').innerHTML =
    ['min: ' + document.getElementById('two').min,
     'max: ' + document.getElementById('two').max,
     'step: ' + document.getElementById('two').step].join(', ');
*/
};
</script>
<?include("../include/header.php")?>
<?
$redis = new Redis();
$redis->connect('127.0.0.1', 6379);
$redis->setOption(Redis::OPT_SERIALIZER, Redis::SERIALIZER_NONE);
$t_min_notte=$redis->get('t_min_notte');
$t_max_notte=$redis->get('t_max_notte');
$t_min_giorno=$redis->get('t_min_giorno');
$t_max_giorno=$redis->get('t_max_giorno');
?>
<body style="text-align: center">
<div align=center style="width: 100%">
<h2>Regolazione temperature termostato</h2>
<form name=primo action=imposta_temperature.php>
<table style="width: 80%; border: 1px solid" >
<tr>
<td rowspan=2 style="text-align:center; vertical-align: middle">
<img src=termometro.png>
</td>
<td>
<h3>Temperatura della notte</h3>
Impostazioni attuali:
<div>min: <?=$t_min_notte?>, max: <?=$t_max_notte?>, media: <?=(($t_min_notte+$t_max_notte)/2)?></div>
<input id="one" type="range" min="18" max="23" step=".25" style="text-align:center; vertical-align: middle" name="t_notte" value="<?=(($t_min_notte+$t_max_notte)/2)?>" /> 
<div id="uno" style="font-size: 36px; font-weight: bold; color: blue; ">Temperatura notte</div>
</td></tr>
<tr><td>
<h3>Temperatura del giorno</h3>
<div>min: <?=$t_min_giorno?>, max: <?=$t_max_giorno?>, media: <?=(($t_min_giorno+$t_max_giorno)/2)?></div>
<input id="two" type="range" min="18" max="23" step=".25" style="text-align:center; vertical-align: middle" name="t_giorno" value="<?=(($t_min_giorno+$t_max_giorno)/2)?>" /> 
<div id="dos" style="font-size: 36px; font-weight: bold; color: red; ">Temperatura giorno</div>
</td>
</tr>
<tr>
<td colspan=2>
<input type=submit value=Imposta>
</td>
</tr>
</table>
</div>
<br>
</form>
</body>
