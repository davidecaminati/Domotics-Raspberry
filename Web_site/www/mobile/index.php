<html>
        <head>
                <META HTTP-EQUIV="refresh" CONTENT="1">
        </head>
        <body>
<style type="text/css">
body {background-color:black;}
p {color:white;font-family:verdana;font-size:16px}
b {color:white;}
h3 {color:white}
</style>

                <div id=grafico>
                        <h3>Temperature Monitoring</h3>
                        <p><b>Time <?=date("h:i:s")?> of <?=date("d/m/Y")?></b></p>
                        <script language=javascript>
                                <?
                                        $start=-1;
                                        $end=-1;
                                        $redis = new Redis();
                                        $redis->connect('127.0.0.1', 6379);
                                        $redis->setOption(Redis::OPT_SERIALIZER, Redis::SERIALIZER_NONE);

                                        $lettura      = $redis->lRange('lettura', $start, $end);
                                        $timestamp    = $redis->lRange('timestamp', $start, $end);
                                        $temp_ext     = $redis->lRange('temp_ext', $start, $end);
                                        $termo        = $redis->lRange('termo', $start, $end);
                                        $rele         = $redis->lRange('rele', $start, $end);
                                        $temp_1       = $redis->lRange('my_room_1', $start, $end);
                                        $temp_2       = $redis->lRange('my_room_2', $start, $end);
                                        $temp_3       = $redis->lRange('my_room_3', $start, $end);
                                        $min          = $redis->lRange('min', $start, $end);
                                        $max          = $redis->lRange('max', $start, $end);
                                        $windows_doors_switch   = $redis->lRange('windows_doors_switch', $start, $end);

                                        echo "my_room_1='$temp_1[0]';\t";
                                        echo "my_room_2='$temp_2[0]';\t";
                                        echo "my_room_3='$temp_3[0]';\t";
                                        echo "windows_doors_switch='$windows_doors_switch[0]';\t";
                                        echo "temp_ext='$temp_ext[0]';\t";
                                ?>
                                document.write ("<p><b>my_room_1 " + my_room_1 + "</b></p>");
                                document.write ("<p><b>my_room_2 " + my_room_2 + "</b></p>");
                                document.write ("<p><b>windows_doors_switch " + windows_doors_switch + "</b></p>");
                                document.write ("<p><b>Temp. ext " + temp_ext + "</b></p>");
                        </script>
                </div>
        </body>
</html>
