<html>
	<head>
		<META HTTP-EQUIV="refresh" CONTENT="1">
	</head>
	<body>
		<div id=grafico>
			<h3>Temperature Monitoring</h3>
			<p>Last update at <?=date("h:i:s")?> of  <?=date("d/m/Y")?></p>
			<script language=javascript>
				<?
					$start=-1;
					$end=-1;
					$redis = new Redis();
					$redis->connect('127.0.0.1', 6379);
					$redis->setOption(Redis::OPT_SERIALIZER, Redis::SERIALIZER_NONE);

					$lettura      = $redis->lRange('lettura', $start, $end);
					$timestamp    = $redis->lRange('timestamp', $start, $end);
					$temp_ext = $redis->lRange('temp_ext', $start, $end);
					$termo        = $redis->lRange('termo', $start, $end);
					$rele         = $redis->lRange('rele', $start, $end);
					$temp_1       = $redis->lRange('camera', $start, $end);
					$temp_2       = $redis->lRange('camerina', $start, $end);
					$temp_3       = $redis->lRange('cucina', $start, $end);
					$min	      	= $redis->lRange('min', $start, $end);
					$max	      	= $redis->lRange('max', $start, $end);
					$windows_doors_switch	= $redis->lRange('windows_doors_switch', $start, $end);

					echo "camera='$temp_1[0]';\t";
					echo "cucina='$temp_3[0]';\t";
					echo "windows_doors_switch='$windows_doors_switch[0]';\t";
					#echo "temp_ext='$temp_ext[0]';\t";
				?>
				document.write ("Camera " + camera);
				document.write ("<br />");
				document.write ("Cucina " + cucina);
				document.write ("<br />");
				document.write ("windows_doors_switch " + windows_doors_switch);
				document.write ("<br />");
				<!-- document.write ("Temp. ext " + temp_ext); -->
			</script>
		</div>
	</body>
</html>