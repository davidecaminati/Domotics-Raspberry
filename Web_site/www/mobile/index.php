<html>
        <head>
                <META HTTP-EQUIV="refresh" CONTENT="15">
        </head>
        <body>
<style type="text/css">
body {background-color:black;}
p {color:white;font-family:verdana;font-size:16px}
b {color:white;}
h3 {color:white}
</style>

                <div id=grafico>
                        <!--<h3>Temperature Monitoring</h3>-->
                        <p><b>Time <?=date("h:i")?> of <?=date("d/m/Y")?></b></p>
                        <script language=javascript>
                                <?
                                        $start=-1;
                                        $end=-1;
                                        $redis = new Redis();
                                        $redis->connect('127.0.0.1', 6379);
                                        $redis->setOption(Redis::OPT_SERIALIZER, Redis::SERIALIZER_NONE);

                                        $lettura      = $redis->lRange('lettura', $start, $end);
                                        $timestamp    = $redis->lRange('timestamp', $start, $end);
                                        $current_temp_ext     = $redis->lRange('current_temp_ext', $start, $end);
                                        $current_ico_ext     = $redis->lRange('current_ico_ext', $start, $end);
                                        $current_condition_ext     = $redis->lRange('current_condition_ext', $start, $end);
                                        
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
                                        echo "current_temp_ext='$current_temp_ext[0]';\t";
                                        echo "current_ico_ext='$current_ico_ext[0]';\t";
                                        echo "current_condition_ext='$current_condition_ext[0]';\t";
                                ?>
                                document.write ("<p><b>my_room_1 " + my_room_1 + "</b></p>");
                                document.write ("<p><b>my_room_2 " + my_room_2 + "</b></p>");
                                document.write ("<p><b>Temp " + current_temp_ext + " <img src=" + current_ico_ext + " style=float:left;margin:0 5px 0 0; /></br></b>");
                                document.write ("<b>Condition " + current_condition_ext + "</br></b>");
                                document.write ("<b>Door/window" + windows_doors_switch + "</b></p>");
                        </script>
                </div>
        </body>
</html>
