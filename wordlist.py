from burp import IBurpExtender
from burp import IContextMenuFactory

from javax.swing import JMenuItem
from java.util import List, ArrayList
from java.net import URL

import re
from datetime import datetime
from HTMLParser import HTMLParser

class TagStripper(HTMLParser):
    
    def __init__(self):
        HTMLParser.__init__(self)
        self.pageText = []

    def handle_data(self, data):
        self.pageText.append(data)

    def handle_comment(self, data):
        self.handle_data(data)

    def strip(self, html):
        self.feed(html)
        return " ".join(self.pageText)

class BurpExtender(IBurpExtender, IContextMenuFactory):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        self.context = None
        self.hosts = set()

        self.wordlist = set(["password"])
        callbacks.setExtensionName("passworld list")
        callbacks.registerContextMenuFactory(self)

        return 

    def createMenuItems(self, contextMenu):
        self.context = contextMenu
        menuList = ArrayList()
        menuList.add(JMenuItem("Create Worldlist", actionPerformed = self.wordlistMenu))
        
        return menuList

    def bingMenu(self, event):
        httpTraffic = self.context.getSelectedMessage()
        
        for traffic in httpTraffic:
            httpService = traffic.getHttpService()
            host = httpService.getHost()

            self.hosts.add(host)
            httpResponse = traffic.getResponse()
            
            if httpResponse:
                self.getWords(httpResponse)
            
        self.displayWordlist()
        return

    def getWords(self, httpResponse):
        headers, body = httpResponse.tostring().split('\r\n\r\n', 1)
        if headers.lower().find('content-type: text') == -1:
            return
        
        tagStripper = TagStripper()
        pageText = tagStripper.strip(body)
        
        words = re.findall("[a-zA-Z]\w{2,}", pageText)
        
        for word in words:
            if len(word) <= 12:
                self.wordlist.add(word.lower())

        return

    def mangle(self, word):
        year = datetime.now().year
        suffixes = ["", "1", "!", year]

        mangled = []

        for password in (word, word.capitalize()):
            for suffix in suffixes:
                mangled.append("%s%s" % (password, suffix))

        return mangled

    def displayWordlist(self):
        print "#comment: worldlist %s" % ", ".join(self.hosts)

        for word in sorted(self.wordlist):
            for password in self.mangle(word):
                print password

        return 
