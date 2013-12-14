<?
$redis = new Redis();
$redis->connect('127.0.0.1', 6379);
$redis->setOption(Redis::OPT_SERIALIZER, Redis::SERIALIZER_NONE);
?>
<html>
<head>
<script src=../lib/html5slider.js>
</script>
<link href='../css/style.css' rel='stylesheet' type='text/css' />
</head>
<?include("../include/header.php")?>
<div align="center" style="width: 100%">
<h2>Weekly program</h2>
<form name=uno action=salva_prog.php method=post>
<table border=2 cellpadding=0 cellspacing=0 width=100%>
<tr><td></td>
<?
$giorni=array("void","mon","tue","wed","thu","fri","sat","sun");
for ($ora=0 ; $ora<=23 ; $ora++) {
?>
<th width="4%"><?=$ora?></th>
<?}?>
</tr>
<?
for ($giorno=1 ; $giorno<=7 ; $giorno++) {
?>
<tr>
<td width="4%"><?=$giorni[$giorno]?></td>
<?
for ($ora=0 ; $ora<=23 ; $ora++) {
if ($ora==0)  {
$redis->of($giorni[$giorno]);
}
?>
<td class=compatta>
<?=$_POST[$giorno."_".$ora]?>
<?$redis->rPush($giorni[$giorno],$_POST[$giorno."_".$ora]);?>
</td>
<?
}
?>
</tr>
<?
}
?>
<tr><td colspan=25>
<a href=prog_settimana.php>Torna alla pagina di programmazione</a> - <a href=../>Torna alla home page</a>
</td></tr>
</table>
</form>
</div>
</body>
</html>
