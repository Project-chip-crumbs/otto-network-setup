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

def get_wifi_networks(): 
    r=[]
    print "scanning networks...",
    p=subprocess.Popen(["/usr/bin/connmanctl","scan","wifi"],stdout=subprocess.PIPE)
    print p.communicate()[0]
    
    print "getting devices...",
    p=subprocess.Popen(["/usr/bin/connmanctl","services"],stdout=subprocess.PIPE)
    output=p.communicate()[0]
    
    print "done"
    
    networks = {}
    for line in output.split('\n'):
        tmp=line[4:].split(' ')[0]
        if(len(tmp)):
            networks[tmp]=1	
    
    for k in networks:
        r.append(k)
    
    return r

def wifi_update_thread():
  while True:
    time.sleep(10)
    tmp_wifis=get_wifi_networks()
    wifis_mutex.acquire()
    global wifis
    wifis=tmp_wifis
    wifis_mutex.release()
    for w in wifis:
      print w 

@route('/')
def rootHome():
    return redirect('/index.html')

@route('/<filename:re:.*\.html>')
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
        return json.dumps({'result':"Failed!"})
    else:
        return json.dumps({'result':"Connecting to network "+data['network']})

#wifis=get_wifi_networks()
thread = Thread(target=wifi_update_thread)
thread.start()
run(host='192.168.1.105', port=8080, reloader=True)
