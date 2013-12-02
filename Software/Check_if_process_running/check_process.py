import re
import subprocess
import time

#def is_running(process):
#variable
process = "rele_board_control.py"

while True:

    running = False
    
    s = subprocess.Popen(["ps", "axw"],stdout=subprocess.PIPE)
    for x in s.stdout:
    
        if re.search(process, x):
            running = true
            print "run"
    if running == False:
        print "not run"
	time.sleep(1)
    #- See more at: http://www.bloggerpolis.com/2011/05/how-to-check-if-a-process-is-running-using-python/#sthash.6CQPQvf6.dpuf#