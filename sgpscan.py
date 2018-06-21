#!/usr/bin/env python
'''
MultiThreading Tcp Port Scanner
author:piaox,2018-03-21
'''

import socket
import sys,subprocess,threading
from threading import Thread
from datetime import datetime

class myThread(threading.Thread):
	def __init__(self,threadName,ip,port_start,port_end,c):
		threading.Thread.__init__(self)
		self.threadName = threadName
		self.ip=ip
		self.port_start=port_start
		self.port_end=port_end
		self.c=c
	def run(self):
		scantcp(self.threadName,self.ip,self.port_start,self.port_end,self.c)

def scantcp(threadName,ip,port_start,port_end,c):
	try :
		for port in range(port_start,port_end):
			x=port
			sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			socket.setdefaulttimeout(c)
			result=sock.connect_ex((ip,port))
			if result==0:
				print '[+] %s PORT:%d is open' %(ip,x)
			sock.close()
	except KeyboardInterrupt:
		print "Keyboard Interrupt Detected"
		sys.exit()
	except socket.gaierror:
		print "Hostname coudlnt be resolved"
		sys.exit()
	except socket.error:
		print "Couldnt connect to the host"
        sys.exit()

def main(singeip):
    ip = singeip
    c = 0.5
    print "*" * 60
    t1 = datetime.now()
    print 'Scanning the host now: ', ip
    port_start = 1
    port_end = 50000
    tot_port = port_end - port_start
    tot_port_thread = 100  # total port handled by one thread
    tnum = tot_port / tot_port_thread  # tnum number of threads
    if (tot_port % tot_port_thread != 0):
        tnum = tnum + 1

    threads = []
    try:
        for i in range(tnum):
            port_end = port_start + tot_port_thread - 1 # per 100 port
            thread = myThread("T1", ip, port_start, port_end, c)
            thread.start()
            port_start = port_end + 1
            threads.append(thread)
    except:
        print "Problem with starting Thread"

    for t in threads:
        t.join()

    t2 = datetime.now()
    total = t2 - t1
    total = str(total)
    print 'Finished scan total used time:%s'%(total)

if __name__ == '__main__':
    ips = ['x.x.x.x','y.y.y.y']
    map(main,ips)
