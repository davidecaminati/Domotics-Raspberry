import re
import subprocess
import time

#def is_running(process):
#variable
process = "rele_board_control.py"
#my_script = ['/home/pi/Domotics-Raspberry/Software/Socket_to_MCP27013_con_i2c/read_pulse.py', '/home/pi/Domotics-Raspberry/Software/Socket_to_MCP27013_con_i2c/rele_board_control.py']
running = False

while True:

    
    s = subprocess.Popen(["ps", "axw"],stdout=subprocess.PIPE)
#for script in my_script:
    for x in s.stdout:
       if re.search(process, x):
           running = True
           print "%s run" % process
    if running == False:
        print "%s not run" % process
    running = False
    time.sleep(3)
    


# launch async calls:
#procs = [subprocess.Popen(['/usr/bin/python', my_script]) for my_script in scripts]
# wait.
#for proc in procs:
#    proc.wait()
## check for results:
#if any(proc.returncode != 0 for proc in procs):
#    print 'Something failed'