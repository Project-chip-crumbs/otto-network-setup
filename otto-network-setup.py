#!/usr/bin/python

import subprocess
import bottle
from bottle import route, static_file, debug, run, get, redirect
from bottle import post, request, template, response
import os, inspect, json, time, sys
import random

from threading import Thread, RLock

#enable bottle debug
debug(True)

# WebApp route path
# get directory of WebApp (bottleJQuery.py's dir)
rootPath =os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

wifis = []
wifis_mutex = RLock()

IMAGEPATH = "/mnt/pictures"
IMAGEURLPREFIX="/image/"

def is_child():
  return 'BOTTLE_CHILD' in os.environ

def get_wifi_networks(): 
    print "scanning networks...",
    p=subprocess.Popen(["/usr/bin/connmanctl","scan","wifi"],stdout=subprocess.PIPE)
    print p.communicate()[0]
    
    print "getting devices...",
    p=subprocess.Popen(["/usr/bin/connmanctl","services"],stdout=subprocess.PIPE)
    output=p.communicate()[0]
    print "done"
    
    print "-"*50
    networks = {}
    for line in output.split('\n'):
        wifi_id=line[line.rfind(' ')+1:]
        wifi_name=line[4:line.rfind(' ')].rstrip()
        wifi_type=wifi_id[wifi_id.rfind('_managed')+1:]
        if(len(wifi_name)):
            networks[wifi_name]={ 'id': wifi_id, 'type': wifi_type, 'name': wifi_name }
            print networks[wifi_name]
    print "-"*50
    print networks    
    print "-"*50
    return networks

def wifi_update_thread():
  countxx=0
  while True:
    global wifis
    global wifis_mutex
    if(wifis_mutex.acquire(blocking=0)):
      wifis=get_wifi_networks()
      wifis_mutex.release()
      print "scan # %d completed"%countxx
      countxx+=1
    
    time.sleep(5)
##    for w in wifis:
##      print w 

@route('/')
def rootHome():
  if os.path.isdir(IMAGEPATH):
    dirs = os.listdir( IMAGEPATH  )
    dirs.sort(reverse=True)
    dirs=[ IMAGEURLPREFIX + d for d in dirs ] 
  else:
    dirs = []
    for i in range(0,10):
      h=random.randint(20,48) * 10
      w=int(4.0/3.0 * h)
      dirs.append('https://placekitten.com/g/%d/%d'%(w,h))

  return template('images', files=dirs)
      
#    return redirect('/setup')

@route(IMAGEURLPREFIX+'<name:re:gif_[0-9]{4}.gif>')
def callback(name):
    return static_file(name, root=IMAGEPATH)

@route('/assets/<filename:re:.*svg>')
def static_svg(filename):
    return static_file(filename, mimetype='image/svg+xml', root=rootPath + '/assets/' )

@route('/assets/<filename:re:.*woff2>')
def static_svg(filename):
    return static_file(filename, mimetype='application/font-woff2', root=rootPath + '/assets/' )

@route('/assets/<filename:re:.*>')
def static_assets(filename):
    return static_file(filename, root=rootPath + '/assets/' )
 
#@route('/<filename:re:.*>')
#def html_file(filename):
#    print 'root=%s' % rootPath
#    return static_file(filename, root=rootPath + '/assets/' )

@route('/setup')
def setup():
    print '/setup root=%s' % rootPath
    wifis_mutex.acquire(blocking=1)
    r=template('setup', wifis=wifis, root=rootPath)
    wifis_mutex.release()
    return r

@route('/api/v1/wifis')
def setup():
    response.content_type = 'application/json'
    wifis=get_wifi_networks()
    return json.dumps(wifis)

@post('/api/v1/setup')
def jsonPost():
    global wifis_mutex
    print "POST Header : \n %s" % dict(request.headers) #for debug header
    data = request.json
    print "data : %s" % data 
    if data == None:
        return "Invalid input data. please try again..."
    else:
        try:
          wifis_mutex.acquire(blocking=1)
          print "Writing connman configuration...",
          f=open("/var/lib/connman/wifi.config","w")
          f.write('[service_'+data['id']+']\n')
          f.write('Type = wifi\n')
          f.write('Name = '+data['network']+'\n')
          if len(data['password']):
            f.write('Passphrase = '+data['password']+"\n")
          f.close()
          print "DONE"
          print "connmanctl connect "+data['id']
          p=subprocess.Popen(["/usr/bin/connmanctl","connect",data['id']],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
          (out,err)=p.communicate()
          already_connected = ('Already connected' in err)
 
          if out.startswith('Connected') or already_connected:
            p=subprocess.Popen(["/sbin/ifconfig","wlan0"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            (out,err)=p.communicate()
            pos=out.find("inet addr:")
            ip='?.?.?.?'
            if(pos>=0):
              ip=out[pos+10:].split(' ')[0]

            if already_connected:
              r="Already connected to "+data['network']+', IP: '+ip
            else:  
              r="Connected to "+data['network']+', IP: '+ip
          else:
            print "out=%s\nerr=%s\n" %(out,err)
            r="Error, could not connect to "+data['network']+" - please try again!"
        except:
          r="Connecting failed. please try again..."
        finally:
          wifis_mutex.release()
          print r
          return r

if __name__ == "__main__":
  if len(sys.argv)>1:
    rootPath=sys.argv[1] 

  print bottle.TEMPLATE_PATH
  bottle.TEMPLATE_PATH.append(rootPath + "/views")
  print bottle.TEMPLATE_PATH
  print "using %s as root path" % rootPath

  #only start thread in child process
  #if is_child():
  #  thread = Thread(target=wifi_update_thread)
  #  thread.start()
  
  run(host='0.0.0.0', port=80, reloader=True)
