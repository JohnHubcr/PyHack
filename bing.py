from burp import IBurpExtender
from burp import IContextMenuFactory

from javax.swing import JMenuItem
from java.util import List, ArrayList
from java.net import URL

import socket
import urllib
import json
import re
import base64

bingAPIKey = ""

class BurpExtender(IBurpExtender, IContextMenuFactory):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        self.context = None

        callbacks.setExtensionName("Bing")
        callbacks.registerContextMenuFactory(self)

        return 

    def createMenuItems(self, contextMenu):
        self.context = contextMenu
        menuList = ArrayList()
        menuList.add(JMenuItem("Send to Bing", actionPerformed = self.bingMenu))
        
        return menuList

    def bingMenu(self, event):
        httpTraffic = self.context.getSelectedMessage()
        print "%d requests highlighted" % len(httpTraffic)
        
        for traffic in httpTraffic:
            httpService = traffic.getHttpService()
            host = httpService.getHost()
            
            print "User selected host: %s" % host
            
            self.bingSearch(host)

        return 

    def bingSearch(self, host):
        isIP = re.math("[0-9]+(?:\.[0-9]+){3}", host)

        if isIP:
            IPAddr = host
            domain = False
        else:
            IPAddr = socket.gethostbyname(host)
            domain = True

        bingQueryString = "'ip:%s'" % ipAddr
        self.bingQuery(bingQueryString)
        
        if domain:
            bingQueryString = "'domain:%s'" % host
            self.bingQuery(bingQueryString)

    def bingQuery(self, bingQueryString):
        print "Performing Bing Search: %s" % bingQueryString

        quotedQuery = urllib.quote(bingQueryString)
        httpRequest = "GET https://api.datamarket.azure.com/Bing/Search/Web?$format=json&$Query=%s HTTP/1.1\r\n" % quotedQuery
        httpRequest += "Host: api.datamarket.azure.com\r\n"
        httpRequest += "Connection: close\r\n"
        httpRequest += "Authorization: Basic %s\r\n" % base64.b64encode("%s" % bingAPIKey)
        httpRequest += "User-Agent: Python\r\n\r\n"

        jsonBody = self._callbacks.makeHttpRequest("api.datamarket.azure.com", 443, True, httpRequest).tostring()
        try:
            r = json.loads(jsonBody)
            
            if len(r["d"]["results"]):
                for site in r["d"]["results"]:
                    print "*" * 100
                    print site["Title"]
                    print site["Url"]
                    print site["Description"]
                    print "*" * 100

                    jUrl = URL(site['Url'])
                    
                    if not self._callbacks.isInScope(jUrl):
                        print "Adding to Burp scope"
                        self._callbacks.includeInScope(jUrl)

        except:
            print "No results from Bing"
            pass

        return

