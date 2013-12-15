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
      document.getElementById('uno').value = this.value;
  };
  document.getElementById('one').onchange();
  
  document.getElementById('two').onchange = function() {
      document.getElementById('dos').innerHTML = this.value;
      document.getElementById('dos').value = this.value;
  };
  document.getElementById('two').onchange();
  
  document.getElementById('three').onchange = function() {
      document.getElementById('tre').innerHTML = this.value;
      document.getElementById('tre').value = this.value;
  };
  document.getElementById('three').onchange();
/*  document.getElementById('mm1').innerHTML =
    ['min: ' + document.getElementById('two').min,
     'max: ' + document.getElementById('two').max,
     'step: ' + document.getElementById('two').step].join(', ');
*/
};
</script>
<?include("../include/header.php")?>
<?
/*$redis = new Redis();
$redis->connect('127.0.0.1', 6379);
$redis->setOption(Redis::OPT_SERIALIZER, Redis::SERIALIZER_NONE);
$t_min_notte=$redis->get('t_min_notte');
$t_max_notte=$redis->get('t_max_notte');
$t_min_giorno=$redis->get('t_min_giorno');
$t_max_giorno=$redis->get('t_max_giorno');
*/?>
<body style="text-align: center">
<div align=center style="width: 100%">
<h2>Settings color</h2>
<form name=primo action=192.168.0.100/>
<table style="width: 80%; border: 1px solid" >
<tr>
<td rowspan=2 style="text-align:center; vertical-align: middle">
<img src=termometro.png>
</td>
<td>
Actual settings:
<h3>RED</h3>
<input id="one" type="range" min="1" max="399" step="1" style="text-align:center; vertical-align: middle" name="c_red" value="<?=(($c_min_red+$c_max_red)/2)?>" /> 
<div id="uno" style="font-size: 36px; font-weight: bold; color: red; ">Red Color</div>
</td></tr>

<tr><td>
<h3>GREEN</h3>
<input id="two" type="range" min="1" max="399" step="1" style="text-align:center; vertical-align: middle" name="c_green" value="<?=(($t_min_giorno+$t_max_giorno)/2)?>" /> 
<div id="dos" style="font-size: 36px; font-weight: bold; color: green; ">Green Color</div>
</td>
</tr>
<tr><td>
<h3>BLUE</h3>
<input id="three" type="range" min="1" max="399" step="1" style="text-align:center; vertical-align: middle" name="c_blue" value="<?=(($t_min_giorno+$t_max_giorno)/2)?>" /> 
<div id="tre" style="font-size: 36px; font-weight: bold; color: blue; ">Blue Color</div>
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
