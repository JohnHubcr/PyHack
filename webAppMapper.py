import Queue
import threading
import os
import urllib2

threads = 10

target = "http://www.test.com"
directory = "/home/neo/something"
filters = [".jpg", ".gif", ".png", ".css"]

os.chdir(directory)

webPaths = Queue.Queue()

for r, d, f in os.walk("."):
    for files in f:
        remotePath = "%s/%s" % (r, files)

        if remotePath.startswith("."):
            remotePath = remotePath[1:]

        if os.path.splitext(files)[1] not in filters:
            webPaths.put(remotePath)

def testRemote():
    while not webPaths.empty():
        path = webPaths.get()
        url = "%s%s" % (target, path)
        request = urllib2.Request(url)

        try:
            response = urllib2.urlopen(request)
            content = response.read()

            print "[%d] => %s" % (response.code, path)

            response.close()

        except urllib2.HTTPError as error:
            pass

for i in range(threads):
    print "Spawning thread: %d" % i
    t = threading.Thread(target = testRemote)
    t.start()
