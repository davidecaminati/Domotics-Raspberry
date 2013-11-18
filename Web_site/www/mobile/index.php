<html>
	<head>
		<META HTTP-EQUIV="refresh" CONTENT="1">
	</head>
	<body>
		<div id=grafico>
			<h3>Monitoraggio temperatura</h3>
			<p>Dati aggiornati alle ore <?=date("h:i:s")?> del  <?=date("d/m/Y")?></p>
			<script language=javascript>
				<?
					$start=-1;
					$end=-1;
					$redis = new Redis();
					$redis->connect('192.168.0.205', 6379);
					$redis->setOption(Redis::OPT_SERIALIZER, Redis::SERIALIZER_NONE);

					$lettura      = $redis->lRange('lettura', $start, $end);
					$timestamp    = $redis->lRange('timestamp', $start, $end);
					$temp_esterna = $redis->lRange('temp_esterna', $start, $end);
					$termo        = $redis->lRange('termo', $start, $end);
					$rele         = $redis->lRange('rele', $start, $end);
					$temp_1       = $redis->lRange('camera', $start, $end);
					$temp_2       = $redis->lRange('camerina', $start, $end);
					$temp_3       = $redis->lRange('cucina', $start, $end);
					$min	      	= $redis->lRange('min', $start, $end);
					$max	      	= $redis->lRange('max', $start, $end);
					$finestre	= $redis->lRange('finestre', $start, $end);

					echo "camera='$temp_1[0]';\t";
					echo "cucina='$temp_3[0]';\t";
					echo "finestre='$finestre[0]';\t";
					echo "temp_esterna='$temp_esterna[0]';\t";
				?>
				document.write ("Camera " + camera);
				document.write ("<br />");
				document.write ("Cucina " + cucina);
				document.write ("<br />");
				document.write ("Finestre aperte " + finestre);
				document.write ("<br />");
				document.write ("Temp. esterna " + temp_esterna);
			</script>
		</div>
	</body>
</html>