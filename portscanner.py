# coding=utf-8
import optparse
import socket

from socket import *
from threading import *


def connect(targethost, targetports):
    """Connect function"""

    # A simple semaphore provides us a lock to prevent other threads from printing on stdout
    screenLock = Semaphore(value=1)

    try:
        c = socket(AF_INET, SOCK_STREAM)
        c.connect((targethost, targetports))
        banner = c.recv(1024)
        # Prior printing an output we grabs a hold of the lock
        screenLock.acquire()
        print '[+] %d/TCP open | ' % targetports + str(banner).strip('\n')
        c.close()
    except:
        print '[-] %d/TCP closed' % targetports


def portscan(targethost, targetports):
    """Multithreading Portscan function"""

    global ip
    try:
        ip = gethostbyname(targethost)
    except:
        print "[-] Cannot resolve '%s': Unknown host" % targethost

    try:
        hostname = gethostbyaddr(ip)
        print '\n[*] Scan Results for: ' + hostname[0]
    except:
        print '\n[*] Scan Results for: ' + ip

    setdefaulttimeout(2)

    # Convert string to list, splitting by commas
    portlist = str(targetports).split(",")

    for port in portlist:
        t = Thread(target=connect, args=(targethost, int(port)))
        t.start()


def main():
    """Tool usage"""

    print """\
    
                                                                                                                        
,------.        ,--.,--.,--------. ,-----.,------.     ,------.                 ,--.                                
|  .---',--.,--.|  ||  |'--.  .--''  .--./|  .--. '    |  .--. ' ,---. ,--.--.,-'  '-. ,---.  ,---. ,--,--.,--,--,  
|  `--, |  ||  ||  ||  |   |  |   |  |    |  '--' |    |  '--' || .-. ||  .--''-.  .-'(  .-' | .--'' ,-.  ||      \ 
|  |`   '  ''  '|  ||  |   |  |   '  '--'\|  | --'     |  | --' ' '-' '|  |     |  |  .-'  `)\ `--.\ '-'  ||  ||  | 
`--'     `----' `--'`--'   `--'    `-----'`--'         `--'      `---' `--'     `--'  `----'  `---' `--`--'`--''--' 
                                                                                                                 

                                     ._ o o
                                   \_`-)|_
                                ,""       \ 
                              ,"  ## |   ಠ ಠ.        A fast full TCP Multithreading Port scanner
                            ," ##   ,-\__    `.      developed by calfcrusher@inventati.org
                          ,"       /     `--._;)     example: ./portscanner.py –H localhost -P 21,80,443
                        ,"     ## /
                      ,"   ##    /                                                                                                           
    """

    parser = optparse.OptionParser('./portscanner.py –H <host> -P <ports>\n')
    parser.add_option('-H', dest='host', type='string', help='set target host')
    parser.add_option('-p', dest='port', type='string', help='set target ports separated by commas')
    (options, args) = parser.parse_args()
    host = options.host
    port = options.port

    if host is None or port is None:
        print "Usage: " + parser.usage
        exit(0)

    portscan(host, port)


if __name__ == "__main__":
    main()

