#!/usr/bin/python

import subprocess
from bottle import route, static_file, debug, run, get, redirect
from bottle import post, request, template, response
import os, inspect, json, time

from threading import Thread, Lock

#enable bottle debug
debug(True)

# WebApp route path
# get directory of WebApp (bottleJQuery.py's dir)
rootPath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


wifis = []
wifis_mutex = Lock()

debug_msg=False

def get_wifi_networks(): 
    print "scanning networks...",
    p=subprocess.Popen(["/usr/bin/connmanctl","scan","wifi"],stdout=subprocess.PIPE)
    if debug_msg: print p.communicate()[0]
    
    print "getting devices...",
    p=subprocess.Popen(["/usr/bin/connmanctl","services"],stdout=subprocess.PIPE)
    output=p.communicate()[0]
    print "done"
    
    networks = {}
    for line in output.split('\n'):
        wifi_id=line[line.rfind(' ')+1:]
        wifi_name=line[4:line.rfind(' ')].rstrip()
        wifi_type=wifi_id[wifi_id.rfind('_managed')+1:]
        if(len(wifi_name)):
            networks[wifi_name]={ 'id': wifi_id, 'type': wifi_type, 'name': wifi_name }
            if debug_msg: print networks[wifi_name]
    
    return networks

def wifi_update_thread():
  while True:
    time.sleep(10)
    if debug_msg: print "** scanning networks **"
    tmp_wifis=get_wifi_networks()
    wifis_mutex.acquire()
    global wifis
    wifis=tmp_wifis
    wifis_mutex.release()
##    for w in wifis:
##      print w 

@route('/')
def rootHome():
    return redirect('/setup')

@route('/<filename:re:.*>')
def html_file(filename):
    return static_file(filename, root=rootPath)

@route('/setup')
def setup():
    wifis_mutex.acquire()
    r=template('setup', wifis=wifis)
    wifis_mutex.release()
    return r

@route('/wifis')
def setup():
    response.content_type = 'application/json'
    return json.dumps(wifis)

@post('/api/v1/setup')
def testJsonPost():
    print "POST Header : \n %s" % dict(request.headers) #for debug header
    data = request.json
    print "data : %s" % data 
    if data == None:
        return "Connecting failed. please try again..."
    else:
        try:
          print "Writing connman configuration...",
          f=open("/var/lib/connman/wifi.config","w")
          f.write('['+data['network']+']\n')
          f.write('Type = wifi\n')
          f.write('Name = '+data['network']+'\n')
          if len(data['password']):
            f.write('Passphrase = '+data['password']+"\n")
          f.close()
          print "DONE"
          print "connmanctl connect "+data['id']
          p=subprocess.Popen(["/usr/bin/connmanctl","connect",data['id']],stdout=subprocess.PIPE)
          out=p.communicate()[0]

          if out.startswith('Connected') or out.rstrip().find('Already connected')!=-1:
            p=subprocess.Popen(["/sbin/ifconfig","wlan0"],stdout=subprocess.PIPE)
            out=p.communicate()[0]
            pos=out.find("inet addr:")
            ip='?.?.?.?'
            if(pos>=0):
              ip=out[pos+10:].split(' ')[0]
  
            print "Connected to "+data['network']+', IP: '+ip
            return "Connected to "+data['network']+', IP: '+ip
          else:
            print "Error, could not connect to "+data['network']+" - please try again!"
            return "Error, could not connect to "+data['network']+" - please try again!"
        except:
          return "Connecting failed. please try again..."

#wifis=get_wifi_networks()
thread = Thread(target=wifi_update_thread)
thread.start()

run(host='0.0.0.0', port=80, reloader=True)
