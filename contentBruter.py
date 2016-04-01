import urllib2
import urllib
import threading
import Queue

threads = 5
targetUrl = "http://testphp.vulnweb.com"
wordListFile = "/tmp/all.txt"
resume = None
userAgent = "Mozilla/5.0 (X11; Linux x86_64; rv:19.0) Gecko/20100101 FireFox/19.0"

def buildWordList(worldListFile):
    fd = open(wordListFile, "rb")
    rawWords = fd.readlines()
    fd.close()

    foundResume = False
    words = Queue.Queue()

    for word in rawWords:
        word = word.rstrip()
        if resume is Not None:
            if foundResume:
                words.put(word)
            else:
                if word == resume:
                    foundResume = True
                    print "Resuming wordlist from: %s" % resume
        else:
            words.put(word)

    return words

def dirBruter(extensions = None):
    while not wordQueue.empty():
        attempt = wordQueue.get()
        attemptList = []

        if '.' not in attempt:
            attemptList.append("/%s/" % attempt)
        else:
            attemptList.append("/%s" % attempt)

        if extensions:
            for extension in extensions:
                attemptList.append("/%s%s" % (attempt, extension))

        for brute in attemptList:
            url = "%s%s" % (targetUrl, urllib.quote(brute))

            try:
                headers = {}
                headers["User-Agent"] = userAgent
                r = urllib2.Request(url, headers = headers)

                response = urllib2.urlopen(r)

                if len(response.read()):
                    print "[%d] => %s" % (response.code, url)
                    
            except urllib2.HTTPError, e:
                if e.code != 404:
                    print "!!! %d => %s" % (e.code, url)

                pass


wordQueue = buildWordList(wordListFile)
extensions = [".php", ".bak", ".orig", ".inc"]

for i in range(threads):
    t = threading.Thread(target = dirBruter, args = (extensions, ))
    t.start()
