import sys
import socket
import getopt
import threading
import subprocess

listen = False
command = False
upload = False
execute = ""
target = ""
uploadDest = ""
port = 0

def usage():
    print "BHP Net Tool"
    print
    print "Usage: netcat.py -t target host -p port"

    print "-l --listen - listen on [host]:[port] for 
    incoming connections"

    print "-e --execute = file to run - execute the given file 
    upon a receiving a connection"

    print "-c --command - initialize a command shell"
    
    print "-u --upload = destination - upon receiving connection
    upload a file and write to [destination]"

    print
    print

    print "Examples:"
    print "netcat.py -t 192.168.0.1 -p 5555 -l -c"
    print "netcat.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe"
    print "netcat.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\""
    print "echo 'ABCDEFGHI' | ./netcat.py -t 192.168.11.12 -p 135"
    
    sys.exit(0)

def main():
    global listen
    global port
    global execute
    global command
    global uploadDest
    global target

    if not len(sys.argv[1:]):
        usage()

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu",
                                   ["help", "listen", "execute", "target", "port", "command", "upload"])
    except getopt.GetoptError as err:
        print str(err)
        usage()

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-c", "--command"):
            command = True
        elif o in ("-u", "--upload"):
            uploadDest = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert Fasle, "Unhandled Option"

    if not listen and len(target) and port > 0:
        buffer = sys.stdin.read()
        clientSender(buffer)

    if listen:
        serverLoop()
