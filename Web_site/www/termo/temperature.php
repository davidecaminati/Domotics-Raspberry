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
$temp_min_night=$redis->get('temp_min_night');
$temp_max_night=$redis->get('temp_max_night');
$temp_min_day=$redis->get('temp_min_day');
$temp_max_day=$redis->get('temp_max_day');
?>
<body style="text-align: center">
<div align=center style="width: 100%">
<h2>Settings Temp</h2>
<form name=primo action=imposta_temperature.php>
<table style="width: 80%; border: 1px solid" >
<tr>
<td rowspan=2 style="text-align:center; vertical-align: middle">
<img src=termometro.png>
</td>
<td>
Actual settings:
<h3>Night Temp</h3>
<div>min: <?=$temp_min_night?>, max: <?=$temp_max_night?>, average: <?=(($temp_min_night+$temp_max_night)/2)?></div>
<input id="one" type="range" min="18" max="23" step=".25" style="text-align:center; vertical-align: middle" name="t_notte" value="<?=(($temp_min_night+$temp_max_night)/2)?>" /> 
<div id="uno" style="font-size: 36px; font-weight: bold; color: blue; ">Night temp</div>
</td></tr>
<tr><td>
<h3>Day Temp</h3>
<div>min: <?=$temp_min_day?>, max: <?=$temp_max_day?>, average: <?=(($temp_min_day+$temp_max_day)/2)?></div>
<input id="two" type="range" min="18" max="23" step=".25" style="text-align:center; vertical-align: middle" name="t_giorno" value="<?=(($temp_min_day+$temp_max_day)/2)?>" /> 
<div id="dos" style="font-size: 36px; font-weight: bold; color: red; ">Day temp</div>
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
