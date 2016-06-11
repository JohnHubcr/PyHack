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

def clientSender(buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client.connect((target, port))
        
        if len(buffer):
            client.send(buffer)

        while True:
            recvLen = 1
            response = ""
            
            while recvLen:
                data = client.recv(4096)
                recvLen = len(data)
                response += data

                if recvLen < 4096:
                    break

            print response,

            buffer = raw_input("")
            buffer += "\n"

            client.send(buffer)

    except:
        print "[*] Exception! Exiting."
        client.close()

def runCommand(command):
    command = command.rstrip()
    
    try:
        output = subprocess.check_output(command, stderr = subprocess, STDOUT, shell = True)
    except:
        output = "Failed to execute command.\r\n"

    return output

def clientHandler(clientSocket):
    global upload
    global execute
    global command

    if len(uploadDest):
        fileBuffer = ""
        
        while True:
            data = clientSocket.recv(1024)
            
            if not data:
                break
            else:
                fileBuffer += data

        try:
            fileDescriptor = open(uploadDest, "wb")
            fileDescriptor.write(fileBuffer)
            fileDescriptor.close()

            clientSocket.send("Successfully saved file to %s\r\n" % uploadDest)
        except:
            clientSocket.send("Failed to save file to %s\r\n" % uploadDest)

    if len(execute):
        output = runCommand(execute)
        clientSocket.send(output)

    if command:
        while True:
            clientSocket.send("<BHP:#> ")
            cmdBuffer = ""
            while "\n" not in cmdBuffer:
                cmdBuffer += clientSocket.recv(1024)
                response = runCommand(cmdBuffer)
                clientSocket.send(response)

def serverLoop():
    global target
    
    if not len(target):
        target = "0.0.0.0"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))

    server.listen(5)

    while True:
        clientSocket, addr = server.accept()
        
        clientThread = threading.Thread(target = clientHandler, args = (clientSocket, ))
        clientThread.start()

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
