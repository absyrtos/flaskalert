import os
from datetime import datetime

now = datetime.now()
dt_string = now.strftime("%d-%m-%Y_%H:%M:%S")
os.system('nmap -iL /home/absy/proje/differ/differ/ip_addreses/iplist.txt -p 80 -Pn -oX /home/absy/proje/differ/differ/scans/scan_'+dt_string+'.xml > /dev/null 2>&1')

