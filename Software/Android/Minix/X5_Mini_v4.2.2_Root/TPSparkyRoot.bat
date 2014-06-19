echo off

cls
echo *---* VonDroid.com N101 II Root Tool based on work by sunnydavid *---*
echo --- Plug in your device, make sure debugging is enabled in Developer Options
echo --- This script will now copy files over to your N101 II
echo.
adb shell mv /data/local/tmp /data/local/tmp.bak

adb shell ln -s /data /data/local/tmp
adb reboot
echo --- Reboot 1/3 - Press Space Bar once the device has rebooted
pause

adb shell rm /data/local.prop > nul
adb shell "echo \"ro.kernel.qemu=1\" > /data/local.prop"
adb reboot
echo --- Reboot 2/3 - Press Space Bar once the device has rebooted
pause

adb shell id
echo --- If the ID shows as 0/root then continue, otherwise CTRL+C to cancel and start over

pause

adb remount
adb push su /system/bin/su
adb shell chown root.shell /system/bin/su
adb shell chmod 6755 /system/bin/su
adb push busybox /system/bin/busybox
adb shell chown root.shell /system/bin/busybox
adb shell chmod 0755 /system/bin/busybox
echo --- Installing SuperSU
adb push SuperSU.apk /system/app/SuperSU.apk
adb shell chown root.root /system/app/SuperSU.apk
adb shell chmod 0644 /system/app/SuperSU.apk
adb push RootExplorer.apk /system/app/RootExplorer.apk
adb shell chown root.root /system/app/RootExplorer.apk
adb shell chmod 0644 /system/app/RootExplorer.apk
echo Completing Root

adb shell rm /data/local.prop
adb shell rm /data/local/tmp
adb shell mv /data/local/tmp.bak /data/local/tmp
adb reboot

echo echo --- Reboot 3/3 - Your N101 II should now be rooted
pause

echo on
