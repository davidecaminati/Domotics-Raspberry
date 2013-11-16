progetto prartito prendendo spunto da :
http://www.raspibo.org/wiki/index.php?title=Termostato

per installare PhpRedis
1) Preparation
1
	
sudo apt-get install php5-dev

php5-dev provides the dev library as well as the phpize command which is required for the compiling step
2) Get phpredis source code, should be pretty easy by running
git clone git://github.com/nicolasff/phpredis.git

3) Compile and install
cd phpredis
phpize
./configure
make
sudo -s make install

4) Enable the phpredis extension
sudo -s
echo "extension=redis.so">/etc/php5/conf.d/redis.ini
exit

5) Write a simple php script to test (running on cli would be fine if php5-cli is installed)
<?php
        // phpredis_set.php
        $redis=new Redis() or die("Can'f load redis module.");
        $redis->connect('127.0.0.1');
        $redis->set('set_testkey', 1);

6) to test
php -r"var_dump(get_class_methods(Redis));"
