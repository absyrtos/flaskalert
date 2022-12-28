#/usr/bin/python3
import sys, os, json, requests
from datetime import datetime
from flask import Flask, render_template, send_file

def slack(alert):

   with open("slack.txt","r") as f:
      veri = f.read()

   temp = ("No scan diff detected between scans")

   if temp not in veri:
        web_hook_url = 'https://hooks.slack.com/services/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'
        slack_msg = {'text':alert}
        requests.post(web_hook_url,data=json.dumps(slack_msg))

def main(argv):

   now = datetime.now()
   dt_string = now.strftime("%d-%m-%Y_%H:%M:%S")
   first_file = os.popen('ls -t /home/absy/proje/differ/differ/scans/*.xml | head -1').read()
   os.system('nmap -iL /home/absy/proje/differ/differ/ip_addreses/iplist.txt -p 80 -Pn -oX /home/absy/proje/differ/differ/scans/scan_'+dt_string+'.xml > /dev/null 2>&1')
   out = os.popen('pyndiff -f1 /home/absy/proje/differ/differ/scans/scan_'+dt_string+'.xml -f2 '+first_file+'').read()
   os.system('rm '+first_file+'')

   with open("slack.txt","w") as f:
      f.write(out)
   with open("logs.txt","a") as f:
      f.write(out)
   with open("logs.txt","a") as f:
      f.write("----"*28)
   with open("logs.txt","a") as f:
      f.write("\n\n")
   with open("logs.txt","r") as f:
      alert = f.read()
   slack(out)

app = Flask(__name__)

@app.route('/')
def index():

	return render_template('index.html')

@app.route('/out')
def out():
	with open("logs.txt","r") as f:
        	out = f.read()
	return render_template('out.html',out=out)

@app.route('/download')
def download_file():
        path = "/home/absy/proje/differ/differ/logs.txt"
        return send_file(path, as_attachment=True)

if __name__ == "__main__":
   main(sys.argv[1:])
   app.run()
